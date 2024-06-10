# Generated by Django 4.2.11 on 2024-06-09 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_productmodel_average_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productmodel')),
            ],
        ),
    ]
