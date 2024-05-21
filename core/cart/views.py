from django.views.generic import View, ListView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from shop.models import ProductModel, ProductStatus
from .cart import CartSession
from .models import CartModel

class CartSummaryView(ListView):
    template_name = 'cart/cart-summary.html'
    template_name_anonymous = 'cart/cart-summary-anonymous.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'get':
            if request.user.is_authenticated:
                handler = getattr(
                    self, 'get', self.http_method_not_allowed
                )
            else:
                return render(request, self.template_name_anonymous)
        elif request.method.lower() == 'head':
            handler = getattr(
                self, 'head', self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_queryset(self):
        return CartModel.objects.prefetch_related('cartitemmodel_set__product__category').get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['cart_total_price'] = self._calculate_total_price(self.object_list)
        return self.render_to_response(context)

    def _calculate_total_price(self, cart_qs):
        total_price = 0
        cart_items = cart_qs.cartitemmodel_set.all()
        for cart_item in cart_items:
            total_price += cart_item.quantity * cart_item.product.get_price()
        return total_price

class SessionAddProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        overide_quantity = True if (request.POST.get('overide_quantity', False)).lower() == 'true' else False
        if product_id:
            try:
                product = get_object_or_404(ProductModel, status=ProductStatus.publish.value, id=product_id)
                cart.add(product_id, product.stock, quantity, overide_quantity)
                if request.user.is_authenticated:
                    cart.update_db(request.user, product)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse(cart.to_json())

class SessionRemoveProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get('product_id')
        if product_id:
            product = get_object_or_404(ProductModel, status=ProductStatus.publish.value, id=product_id)
            cart.remove(product_id)
            if request.user.is_authenticated:
                cart.update_db(request.user, product)
        return HttpResponse(status=200)

class SessionClearProductView(View):

    def post(self, request, *args, **kwargs):
        pass
