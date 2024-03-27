import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from shop.models import ProductCategoryModel

class Command(BaseCommand):
    help = 'Generate fake data for ProductCategoryModel'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(10):
            title = fake.word()
            slug = slugify(title, allow_unicode=True)
            ProductCategoryModel.objects.get_or_create(title=title, slug=slug)
        self.stdout.write(self.style.SUCCESS('Successfully generated 10 fake data for ProductCategoryModel'))
