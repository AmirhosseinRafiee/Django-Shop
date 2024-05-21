from django.db.models import F, Case, When
from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import ProductModel
from .models import OrderModel, OrderItemModel, OrderStatusType


@receiver(post_save, sender=OrderModel)
def add_user_to_cupon_used_by(sender, instance, created, **kwargs):
    if created:
        if instance.cupon:
            instance.cupon.used_by.add(instance.user)
    elif instance.status == OrderStatusType.canceled.value:
        # Get the order items related to this order
        order_items = OrderItemModel.objects.filter(order=instance)

        # Prepare the stock update cases
        stock_updates = []
        for order_item in order_items:
            stock_updates.append(
                When(id=order_item.product.id, then=F('stock') + order_item.quantity))

        # Perform the stock update
        ProductModel.objects.filter(id__in=[item.product.id for item in order_items]).update(
            stock=Case(*stock_updates)
        )
