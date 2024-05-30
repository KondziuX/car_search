# Generated by Django 3.2.5 on 2023-02-22 17:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0018_pricereminder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricereminder',
            name='advert_id',
        ),
        migrations.AlterField(
            model_name='pricereminder',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
