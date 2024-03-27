from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from decimal import Decimal

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

class ProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategoryModel)
    title = models.CharField(max_length=254)
    slug = models.SlugField(unique=True, allow_unicode=True)
    image = models.ImageField(default='defaults/product-image.png', upload_to='product/image/')
    description = models.TextField()
    brief_description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=ProductStatus.choices, default=ProductStatus.draft.value)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # Handle duplicate slug by modifying it
            suffix = 1
            while True:
                try:
                    self.slug = f"{slugify(self.title)}-{suffix}"
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

class ProductImageModel(models.Model):
    proudct = models.ForeignKey('ProductModel', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='product/extra-img/')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
