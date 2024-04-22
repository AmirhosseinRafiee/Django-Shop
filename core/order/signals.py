from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderModel

@receiver(post_save, sender=OrderModel)
def add_user_to_cupon_used_by(sender, instance, created, **kwargs):
    if created and instance.cupon:
        instance.cupon.used_by.add(instance.user)
