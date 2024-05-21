from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.db.models import F, Case, When, Value
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from order.models import UserAddressModel
from cart.models import CartModel, CartItemModel
from cart.cart import CartSession
from payment.models import PaymentModel, PaymentClient
from payment.clients import ZarinPalSandbox
from shop.models import ProductModel
from .permissions import HasCustomerAccessPermission
from .models import OrderModel, OrderItemModel, CuponModel
from .forms import CheckOutForm


class OrderCheckoutView(LoginRequiredMixin, HasCustomerAccessPermission, FormView):
    template_name = 'order/order-checkout.html'
    form_class = CheckOutForm

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

        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                messages.error(self.request, _(f"موجودی کالای {cart_item.product.title} کمتر از درخواست شماست"))
                return redirect(reverse('cart:session-cart-summary'))

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
        stock_updates = []
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

            stock_updates.append(
                When(id=cart_item.product.id, then=F('stock') - cart_item.quantity))

        cupon: CuponModel = cleaned_data['cupon']
        if cupon:
            cupon_discount_amount = cupon.calculate_discount_amount(
                total_price - discounted_amount)
            total_price -= cupon_discount_amount
            discounted_amount += cupon_discount_amount
            order.cupon = cupon
        order.total_price = total_price
        order.discounted_amount = discounted_amount

        try:
            with transaction.atomic():
                # Update products stock in one query
                ProductModel.objects.filter(id__in=[item.product.id for item in cart_items]).update(
                    stock=Case(*stock_updates)
                )

                # Save order and order items
                order.save()
                OrderItemModel.objects.bulk_create(order_item_list)

                # Clear the cart
                cart_items.delete()
            CartSession(self.request.session).clear()
        except Exception as e:
            # logger.error(f"An error occurred while processing the order: {e}")
            messages.error(self.request, _(
                "خطایی در هنگام پردازش درخواست شما رخ داد. لطفاً مجدداً امتحان کنید"))
            return redirect(reverse('cart:session-cart-summary'))

        payment_url_pattern = self._get_payment_pattern(
            cleaned_data['payment'])
        return redirect(reverse(payment_url_pattern, kwargs={'pk': order.pk}))

    def _get_payment_pattern(self, payment_val):
        if payment_val == 1:
            return 'payment:zarinpal-pay'
        elif payment_val == 2:
            return 'payment:aqayepardakht-pay'
        elif payment_val == 3:
            return 'payment:payping-pay'


class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/order-completed.html'


class OrderFailedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/order-failed.html'


class OrderValidateCuponView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        message, status = _('کد تخفیف با موفقیت اعمال شد'), 200
        data = dict()
        try:
            cupon_obj = CuponModel.objects.get(code=code)
        except CuponModel.DoesNotExist:
            message, status = _('کد تخفیف وجود ندارد'), 404
        else:
            if cupon_obj.used_by.all().count() >= cupon_obj.max_limit_usage:
                message, status = _('تعداد کد تخفیف تمام شده است'), 403

            elif cupon_obj.expiration_date > timezone.now():
                message, status = _('کد تخفیف منقصی شده'), 403

            elif request.user in cupon_obj.used_by.all():
                message, status = _('کد تخفیف قبلا استفاده شده'), 403

            else:
                price = request.POST.get('price')
                if price:
                    data['discount_amount'] = cupon_obj.calculate_discount_amount(
                        int(price))
        data['message'] = message
        return JsonResponse(data=data, status=status)
