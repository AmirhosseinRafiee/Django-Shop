from django.views.generic import View, TemplateView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from shop.models import ProductModel, ProductStatus
from.cart import CartSession

class CartSummaryView(TemplateView):
    template_name = 'cart/cart-summary.html'

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
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse(cart.to_json())

class SessionRemoveProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get('product_id')
        if product_id:
            cart.remove(product_id)
        return HttpResponse(status=200)

class SessionClearProductView(View):

    def post(self, request, *args, **kwargs):
        pass
