# Generated by Django 4.2.11 on 2024-06-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_newslettersubscribermodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketmodel',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'در انتظار'), (2, 'در حال پاسخ دهی'), (3, 'پاسخ داده شده')], default=1),
        ),
    ]
