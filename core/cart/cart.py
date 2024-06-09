from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from shop.models import ProductModel, ProductStatus
from cart.models import CartModel, CartItemModel


class CartSession:
    def __init__(self, session):
        self.session = session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product_id, product_stock, quantity=1, overide_quantity=False):
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
            }
        self._validate_quantity(product_stock, self.cart[product_id]['quantity'],
                                quantity, overide_quantity)
        if overide_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] = min(self.cart[product_id]["quantity"] + quantity, product_stock)
        if self.cart[product_id]["quantity"] == 0:
            self.remove(product_id)
        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductModel.objects.filter(
            status=ProductStatus.publish.value, id__in=product_ids).prefetch_related('category')
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
            cart[str(product.id)]["total_price"] = product.get_price() * \
                cart[str(product.id)]["quantity"]
        for item in cart.values():
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_cart_total_price(self):
        return sum(item["total_price"] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session['cart']
        self.save()

    def get_product_quantity(self, product_id):
        return self.cart.get(product_id, {'quantity': 0})['quantity']

    def to_json(self):
        product_ids = self.cart.keys()
        products = ProductModel.objects.filter(
            status=ProductStatus.publish.value, id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product_id"] = product.id
            cart[str(product.id)]["image_url"] = product.image.url
            cart[str(product.id)]["title"] = product.title
            cart[str(product.id)]["product_url"] = reverse(
                'shop:product-detail', kwargs={'slug': product.slug})
            cart[str(product.id)]["total_price"] = product.get_price() * \
                cart[str(product.id)]["quantity"]
        cart_json = {'cart': cart}
        cart_json["cart_total_price"] = self.get_cart_total_price()
        cart_json["cart_total_quantity"] = len(self)
        return cart_json

    def sync_cart_items_from_db(self, user):
        cart, _ = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(
            cart=cart).select_related('product')
        bulk_updates_cart_items = list()
        for cart_item in cart_items:
            # add to session if not exists
            if str(cart_item.product.id) not in self.cart.keys():
                self.cart[str(cart_item.product.id)] = {
                    'quantity': cart_item.quantity
                }
            # update quantity in db if exists in both
            elif cart_item.quantity != self.cart[str(cart_item.product.id)]['quantity']:
                cart_item.quantity = self.cart[str(cart_item.product.id)]['quantity']
                bulk_updates_cart_items.append(cart_item)
        if bulk_updates_cart_items:
            CartItemModel.objects.bulk_update(
                bulk_updates_cart_items,
                fields=['quantity'],
            )
        self.save()

        # add to db if not exists
        cart_items_id = [str(cart_item.product.id) for cart_item in cart_items]
        new_product_ids = [
            item for item in self.cart.keys() if item not in cart_items_id]
        products = ProductModel.objects.filter(
            status=ProductStatus.publish.value, id__in=new_product_ids)
        new_cart_items = [
            CartItemModel(
                cart=cart,
                product=product,
                quantity=self.cart[str(product.id)]['quantity']
            )
            for product in products
        ]
        CartItemModel.objects.bulk_create(new_cart_items)

    def merge_session_cart_in_db(self, user):
        cart, _ = CartModel.objects.get_or_create(user=user)
        products = ProductModel.objects.filter(
            status=ProductStatus.publish.value, id__in=self.cart.keys())
        # add to db if not exists or update quantity if exists
        for product in products:
            CartItemModel.objects.update_or_create(
                cart=cart,
                product=product,
                defaults={
                    'quantity': self.cart[str(product.id)]['quantity']
                }
            )
        # delete from db if not exists in session
        CartItemModel.objects.filter(cart=cart).exclude(
            product__id__in=self.cart.keys()).delete()

    def update_db(self, user, product):
        cart, _ = CartModel.objects.get_or_create(user=user)
        new_quantity = self.cart.get(str(product.id), {'quantity': 0})['quantity']
        if new_quantity == 0:
            CartItemModel.objects.filter(cart=cart, product=product).delete()
        else:
            # CartItemModel.objects.filter(cart=cart, product=product_id).update(quantity=new_quantity)
            CartItemModel.objects.update_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': new_quantity}
            )

    def _validate_quantity(self, product_stock, cart_quantity, quantity, overide_quantity):
        new_quantity = quantity + cart_quantity if not overide_quantity else quantity
        if new_quantity < 0:
            raise ValueError(_('موجودی کالا نمی تواند منفی باشد'))
        elif new_quantity > product_stock and quantity > 0:
            if product_stock == 0:
                raise ValueError(_('موجودی کالای مورد نظر به پایان رسیده است'))
            else:
                raise ValueError(_('تعداد درخواستی بیشتر از تعداد موجود می باشد'))

