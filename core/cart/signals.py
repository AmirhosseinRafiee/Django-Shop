from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .cart import CartSession

@receiver(user_logged_in)
def login_sync_cart(sender, user, request, **kwargs):
    cart = CartSession(request.session)
    cart.sync_cart_items_from_db(user)

@receiver(user_logged_out)
def logout_update_db(sender, user, request, **kwargs):
    cart= CartSession(request.session)
    cart.merge_session_cart_in_db(user)
