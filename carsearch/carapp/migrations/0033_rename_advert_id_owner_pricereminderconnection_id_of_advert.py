# Generated by Django 3.2.5 on 2023-02-23 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0032_rename_pricereminder_pricereminderconnection'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricereminderconnection',
            old_name='advert_id_owner',
            new_name='id_of_advert',
        ),
    ]
