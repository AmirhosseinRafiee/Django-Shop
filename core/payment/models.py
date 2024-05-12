from django.db import models
from django.utils.translation import gettext_lazy as _
from order.models import OrderModel


class PaymentStatus(models.IntegerChoices):
    pending = 1, _("در انتظار پرداخت")
    success = 2, _("پرداخت موفق")
    failed = 3, _("پرداخت ناموفق")


class PaymentClient(models.IntegerChoices):
    zarinpal = 1, _("زرین پال")
    aqayepardakht = 2, _("آقای پرداخت")
    payping = 3, _("پی پینگ")


class PaymentModel(models.Model):
    order = models.OneToOneField(OrderModel, on_delete=models.PROTECT)
    client = models.IntegerField(choices=PaymentClient.choices)
    authority_id = models.CharField(max_length=124)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.IntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.pending.value)
    ref_id = models.CharField(max_length=60, null=True, blank=True)
    response_code = models.IntegerField(null=True, blank=True)
    response_json = models.JSONField(default=dict)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['client', 'authority_id']]
