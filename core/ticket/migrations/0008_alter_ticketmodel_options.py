# Generated by Django 4.2.11 on 2024-06-06 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_alter_ticketmodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketmodel',
            options={'ordering': ('-created_date',)},
        ),
    ]