# Generated by Django 3.2.5 on 2023-02-23 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0031_auto_20230223_1651'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PriceReminder',
            new_name='PriceReminderConnection',
        ),
    ]
