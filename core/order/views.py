from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from order.models import UserAddressModel
from cart.models import CartModel, CartItemModel
from cart.cart import CartSession
from .permissions import HasCustomerAccessPermission
from .models import OrderModel, OrderItemModel
from .forms import CheckOutForm


class OrderCheckoutView(LoginRequiredMixin, HasCustomerAccessPermission, FormView):
    template_name = 'order/order-checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('order:completed')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = UserAddressModel.objects.filter(
            user=self.request.user)
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        address = cleaned_data['address']
        total_price = 0
        discounted_amount = 0
        cart = CartModel.objects.get(user=self.request.user)
        cart_items = cart.cartitemmodel_set.all().select_related('product')

        # Check if cart_items is empty
        if not cart_items.exists():
            messages.error(self.request, _("سبد خرید شما خالیست!"))
            return redirect(reverse('shop:product-grid'))

        # Create the order object
        order = OrderModel(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )

        # Create order items and calculate total price and discounted amount
        order_item_list = []
        for cart_item in cart_items:
            order_item = OrderItemModel(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                discount_percent=cart_item.product.discount_percent,
            )
            order_item_list.append(order_item)
            discounted_amount += cart_item.product.price * \
                cart_item.quantity * cart_item.product.discount_percent / 100
            total_price += cart_item.product.price * cart_item.quantity

        order.total_price = total_price
        order.discounted_amount = discounted_amount

        try:
            with transaction.atomic():
                # Save order and order items
                order.save()
                OrderItemModel.objects.bulk_create(order_item_list)

                # Clear the cart
                cart_items.delete()
            CartSession(self.request.session).clear()
        except Exception as e:
            # logger.error(f"An error occurred while processing the order: {e}")
            messages.error(self.request, _("خطایی در هنگام پردازش درخواست شما رخ داد. لطفاً بعداً مجدداً امتحان کنید"))
            return redirect(reverse('order:checkout'))

        return super().form_valid(form)


class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/order-completed.html'
