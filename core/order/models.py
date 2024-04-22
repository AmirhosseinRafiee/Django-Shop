from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

User = get_user_model()


class OrderStatusType(models.IntegerChoices):
    pending = 1, _("در انتظار پرداخت")
    processing = 2, _("در حال پردازش")
    shipped = 3, _("ارسال شده")
    delivered = 4, _("تحویل شده")
    canceled = 5, _("لغو شده")


class UserAddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10, validators=[RegexValidator(
        r'^\d{10}$', message=_("کد پستی باید ده رقمی باشد"))])

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_date', )


class CuponModel(models.Model):
    code = models.CharField(max_length=100)
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_discount_amount = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True)
    max_limit_usage = models.IntegerField(default=10)
    used_by = models.ManyToManyField(User, blank=True)

    expiration_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def calculate_discount_amount(self, total_price):
        if self.max_discount_amount:
            return min(round(total_price * Decimal(self.discount_percent / 100)), self.max_discount_amount)
        return round(total_price * Decimal(self.discount_percent / 100))


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # address information
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)

    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=0)
    cupon = models.ForeignKey(
        CuponModel, on_delete=models.PROTECT, null=True, blank=True)
    status = models.IntegerField(
        choices=OrderStatusType.choices, default=OrderStatusType.pending.value
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.id}"

class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.ProductModel', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.order.id}"
