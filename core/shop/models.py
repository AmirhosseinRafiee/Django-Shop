from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.utils import IntegrityError
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from decimal import Decimal
from review.models import ReviewStatusType

User = get_user_model()


class ProductStatus(models.IntegerChoices):
    draft = 1, _('draft')
    publish = 2, _('publish')


class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=254)
    slug = models.SlugField(allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product-grid') + f'?category={self.slug}'


class ProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategoryModel)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, allow_unicode=True)
    image = models.ImageField(
        default='defaults/product-image.png', upload_to='product/image/')
    description = models.TextField()
    brief_description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(
        choices=ProductStatus.choices, default=ProductStatus.draft.value)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    average_rate = models.FloatField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # Handle duplicate slug by modifying it
            suffix = 0
            while True:
                try:
                    self.slug = slugify(self.title, allow_unicode=True)
                    if suffix > 0:
                        self.slug += f'-{suffix}'
                    super().save(*args, **kwargs)
                    break
                except IntegrityError:
                    suffix += 1

    def __str__(self):
        return self.title

    def get_price(self):
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        discounted_price = self.price - discount_amount
        return round(discounted_price)

    def is_discounted(self):
        return self.discount_percent != 0

    def is_published(self):
        return self.status == ProductStatus.publish.value

    def calculate_average_rating(self):
        return round(self.reviewproductmodel_set.filter(status=ReviewStatusType.accepted.value).aggregate(Avg('rate'))['rate__avg'] or 0, 1)


class ProductImageModel(models.Model):
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='product/extra-img/')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]


class WishlistProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ('-id',)


class FeaturedProductModel(models.Model):
    product = models.OneToOneField('ProductModel', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Featured: {self.product.title}"
