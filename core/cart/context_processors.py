from .cart import CartSession

def cart_items(request):
    cart = CartSession(request.session)
    return {"cart": cart}
