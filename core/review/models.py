from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from order.models import OrderItemModel

User = get_user_model()

class ReviewStatusType(models.IntegerChoices):
    pending = 1, "در انتظار تایید"
    accepted = 2, "تایید شده"
    rejected = 3, "رد شده"

class ReviewProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.ProductModel', on_delete=models.CASCADE)
    rate = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    is_buyer = models.BooleanField(default=False)
    status = models.IntegerField(
        choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.user.email} - {self.product.id} - {self.rate}"

    def is_user_buyer(self):
        return OrderItemModel.objects.filter(
            order__user=self.user,
            product=self.product
        ).exists()

    def get_status(self):
        return {
            'id': self.status,
            "title":ReviewStatusType(self.status).name,
            "label":ReviewStatusType(self.status).label,
        }