from django.views.generic import View
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from order.models import OrderModel, OrderStatusType
from order.permissions import HasCustomerAccessPermission
from ..models import PaymentModel, PaymentStatus, PaymentClient
from ..clients import PayPingSandbox


class PayPingPayView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        order = get_object_or_404(
            OrderModel, pk=pk, status=OrderStatusType.pending.value)
        price = order.total_price-order.discounted_amount
        # snadbox limitation
        if price > 2000:
            price = 1000

        zarinpal_obj = PayPingSandbox()
        res = zarinpal_obj.send_request(amount=price).json()
        code = res['code']

        PaymentModel.objects.create(
            order=order,
            client=PaymentClient.zarinpal.value,
            authority_id=code,
            amount=price,
        )

        return redirect(zarinpal_obj.generate_payment_url(code))


@method_decorator(csrf_exempt, name='dispatch')
class PayPingVerifyView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        ref_id = request.POST.get('refid')
        try:
            payment = PaymentModel.objects.select_related(
                'order').get(authority_id=code)
        except PaymentModel.DoesNotExist:
            raise Http404(_('پرداختی با این شناسه وجود ندارد!'))
        payment_obj = PayPingSandbox()
        res = payment_obj.verify_payment(
            ref_id=ref_id,
            amount=payment.amount,
        )
        res_json = res.json()
        order = payment.order
        if res.status_code == 200:
            payment.status = PaymentStatus.success.value
            order.status = OrderStatusType.processing.value
            redirect_url = reverse('order:completed')
        else:
            payment.status = PaymentStatus.failed.value
            order.status = OrderStatusType.canceled.value
            redirect_url = reverse('order:failed')
        payment.ref_id = ref_id
        payment.response_code = res.status_code
        payment.response_json = res_json
        payment.save()
        order.save()
        return redirect(redirect_url)
