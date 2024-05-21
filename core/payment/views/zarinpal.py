from django.views.generic import View
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from order.models import OrderModel, OrderStatusType
from order.permissions import HasCustomerAccessPermission
from ..models import PaymentModel, PaymentStatus, PaymentClient
from ..clients import ZarinPalSandbox


class ZarinpalPayView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        order = get_object_or_404(
            OrderModel, pk=pk, status=OrderStatusType.pending.value)
        price = order.total_price-order.discounted_amount

        zarinpal_obj = ZarinPalSandbox()
        res = zarinpal_obj.send_request(amount=price)
        authority = res['Authority']

        PaymentModel.objects.create(
            order=order,
            client=PaymentClient.zarinpal.value,
            authority_id=authority,
            amount=price,
        )

        return redirect(zarinpal_obj.generate_payment_url(authority))


class ZarinpalVerifyView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def get(self, request, *args, **kwargs):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')
        try:
            payment = PaymentModel.objects.select_related(
                'order').get(authority_id=authority)
        except PaymentModel.DoesNotExist:
            raise Http404(_('پرداختی با این شناسه وجود ندارد!'))
        payment_obj = ZarinPalSandbox()
        res = payment_obj.verify_payment(
            authority=authority,
            amount=payment.amount,
        )
        order = payment.order
        if status == 'OK' and res['Status'] in [100, 101]:
            payment.status = PaymentStatus.success.value
            order.status = OrderStatusType.processing.value
            redirect_url = reverse('order:completed')
        else:
            payment.status = PaymentStatus.failed.value
            order.status = OrderStatusType.canceled.value
            redirect_url = reverse('order:failed')
        payment.ref_id = res['RefID']
        payment.response_code = res['Status']
        payment.response_json = res
        payment.save()
        order.save()
        return redirect(redirect_url)
