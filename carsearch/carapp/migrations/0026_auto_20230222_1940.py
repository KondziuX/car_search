# Generated by Django 3.2.5 on 2023-02-22 19:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0025_alter_pricereminder_advert_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricereminder',
            name='advert_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='pricereminder',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
