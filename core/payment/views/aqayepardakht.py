from django.views.generic import View
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from order.models import OrderModel, OrderStatusType
from order.permissions import HasCustomerAccessPermission
from ..models import PaymentModel, PaymentStatus, PaymentClient
from ..clients import AqayePardakhtSandbox


class AqayePardakhtPayView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        order = get_object_or_404(
            OrderModel, pk=pk, status=OrderStatusType.pending.value)
        price = order.total_price-order.discounted_amount

        aqayepardakht_obj = AqayePardakhtSandbox()
        res = aqayepardakht_obj.send_request(amount=price)

        status = res['status']
        if status == "error":
            return HttpResponseBadRequest()

        transid = res['transid']

        PaymentModel.objects.create(
            order=order,
            client=PaymentClient.aqayepardakht.value,
            authority_id=transid,
            amount=price,
        )

        return redirect(aqayepardakht_obj.generate_payment_url(transid))

@method_decorator(csrf_exempt, name='dispatch')
class AqayePardakhtVerifyView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def post(self, request, *args, **kwargs):
        transid = request.POST.get('transid')
        status = request.POST.get('status')
        try:
            payment = PaymentModel.objects.select_related(
                'order').get(authority_id=transid)
        except PaymentModel.DoesNotExist:
            raise Http404(_('پرداختی با این شناسه وجود ندارد!'))
        payment_obj = AqayePardakhtSandbox()
        res = payment_obj.verify_payment(
            authority=transid,
            amount=payment.amount,
        )
        if status == '1' and res['code'] in ['1', '2']:
            payment.status = PaymentStatus.success.value
            order = payment.order
            order.status = OrderStatusType.processing.value
            order.save()
            redirect_url = reverse('order:completed')
        else:
            payment.status = PaymentStatus.failed.value
            redirect_url = reverse('order:failed')
        payment.ref_id = request.POST.get('tracking_number')
        payment.response_code = res['code']
        payment.response_json = res
        payment.save()
        return redirect(redirect_url)
