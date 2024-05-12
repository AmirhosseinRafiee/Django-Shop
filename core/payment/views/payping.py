from django.views.generic import View
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from order.models import OrderModel, OrderStatusType
from ..models import PaymentModel, PaymentStatus, PaymentClient
from ..clients import PayPingSandbox


class PayPingPayView(View):

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
class PayPingVerifyView(View):

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
        if res.status_code == 200:
            payment.status = PaymentStatus.success.value
            order = payment.order
            order.status = OrderStatusType.processing.value
            order.save()
            redirect_url = reverse('order:completed')
        else:
            payment.status = PaymentStatus.failed.value
            redirect_url = reverse('order:failed')
        payment.ref_id = ref_id
        payment.response_code = res.status_code
        payment.response_json = res_json
        payment.save()
        return redirect(redirect_url)
