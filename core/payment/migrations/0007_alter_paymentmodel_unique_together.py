# Generated by Django 4.2.11 on 2024-05-07 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_rename_payment_paymentmodel'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='paymentmodel',
            unique_together={('client', 'authority_id')},
        ),
    ]
