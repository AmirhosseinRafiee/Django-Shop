# Generated by Django 4.2.11 on 2024-05-05 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_payment_ref_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='response_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
