# Generated by Django 3.2.5 on 2023-02-22 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0023_rename_advert_id_pricereminder_advert'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricereminder',
            old_name='advert',
            new_name='advert_id',
        ),
    ]
