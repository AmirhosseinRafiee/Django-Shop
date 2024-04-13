from django.urls import reverse
from shop.models import ProductModel, ProductStatus

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
        self._validate_quantity(product_id, product_stock, quantity, overide_quantity)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
            }
        if overide_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        if self.cart[product_id]["quantity"] == 0:
            self.remove(product_id)
        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductModel.objects.filter(status=ProductStatus.publish.value, id__in=product_ids).prefetch_related('category')
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
            cart[str(product.id)]["total_price"] = product.get_price() * cart[str(product.id)]["quantity"]
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

    def to_json(self):
        product_ids = self.cart.keys()
        products = ProductModel.objects.filter(status=ProductStatus.publish.value, id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product_id"] = product.id
            cart[str(product.id)]["image_url"] = product.image.url
            cart[str(product.id)]["title"] = product.title
            cart[str(product.id)]["product_url"] = reverse('shop:product-detail', kwargs={'slug': product.slug})
            cart[str(product.id)]["total_price"] = product.get_price() * cart[str(product.id)]["quantity"]
        cart_json = {'cart': cart}
        cart_json["cart_total_price"] = self.get_cart_total_price()
        cart_json["cart_total_quantity"] = len(self)
        return cart_json

    def _validate_quantity(self, product_id, product_stock, quantity, overide_quantity):
        if overide_quantity:
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
            elif quantity > product_stock:
                raise ValueError("Quantity exceeds available stock")
        else:
            product_quantity = self.cart.get(product_id, {'quantity': 0})['quantity']
            if quantity + product_quantity < 0:
                raise ValueError("Quantity cannot be negative")
            elif quantity + product_quantity > product_stock:
                raise ValueError("Quantity exceeds available stock")
