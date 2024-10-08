# Generated by Django 4.0.1 on 2024-06-21 09:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0065_alter_advert_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='advanced_safety_systems',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='comfortable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='durable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='dynamic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='intelligent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='low_maintenance_costs',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='off_road',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='practical',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='premium',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='roomy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='spacious',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advert',
            name='urban',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='advert',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 21, 9, 27, 41, 201962, tzinfo=utc)),
        ),
    ]
