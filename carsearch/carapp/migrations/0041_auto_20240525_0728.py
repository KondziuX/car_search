# Generated by Django 3.2.5 on 2024-05-25 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0040_auto_20240513_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='brand',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
    ]
