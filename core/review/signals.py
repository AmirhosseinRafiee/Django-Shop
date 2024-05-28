from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import ReviewProductModel, ReviewStatusType

@receiver(pre_save, sender=ReviewProductModel)
def store_previous_status(sender, instance, update_fields, **kwargs):
    if instance.pk:
        instance._pre_save_status = ReviewProductModel.objects.get(pk=instance.pk).status
    else:
        instance._pre_save_status = None

@receiver(post_save, sender=ReviewProductModel)
def update_product_average_rating_on_save(sender, instance, created, **kwargs):
    if not created:
        previous_status = getattr(instance, '_pre_save_status', None)
        if previous_status != instance.status:
            if previous_status == ReviewStatusType.accepted.value or instance.status == ReviewStatusType.accepted.value:
                product = instance.product
                product.average_rate = product.calculate_average_rating()
                product.save()

@receiver(post_delete, sender=ReviewProductModel)
def update_product_average_rating_on_delete(sender, instance, **kwargs):
    if instance.status == ReviewStatusType.accepted.value:
        product = instance.product
        product.average_rate = product.calculate_average_rating()
        product.save()