# Generated by Django 4.2.11 on 2024-04-22 09:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0004_alter_cuponmodel_max_discount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuponmodel',
            name='used_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
