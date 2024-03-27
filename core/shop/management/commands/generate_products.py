from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext as _
from pathlib import Path
from faker import Faker
from django.core.files import File
from shop.models import ProductModel, ProductCategoryModel, ProductStatus
from accounts.models import UserType
import os
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate 20 fake products'

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories = list(ProductCategoryModel.objects.all())
        user = User.objects.get(type=UserType.admin.value)
        base_path = Path(__file__).resolve().parent
        default_image_paths = [
            'images/img1.png',
            'images/img2.png',
            'images/img3.png',
            'images/img4.png',
        ]

        for _ in range(20):
            user = user
            num_categories = random.randint(1, 4)
            selected_categories = random.sample(categories, num_categories)
            title = fake.word()
            slug = slugify(title)
            image_path = os.path.join(base_path, random.choice(default_image_paths))
            image = File(open(image_path, 'rb'), name=Path(image_path).name)
            description = fake.text()
            stock = fake.random_int(min=0, max=1000)
            status = fake.random_element(ProductStatus.choices)[0]
            price = fake.random_int(min=10**4, max=10**7)
            discount_percent = fake.random_int(min=0, max=50)

            product = ProductModel.objects.create(
                user=user,
                title=title,
                slug=slug,
                image=image,
                description=description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent
            )
            product.category.set(selected_categories)

        self.stdout.write(self.style.SUCCESS('Successfully generated 20 fake data for ProductsModel'))
