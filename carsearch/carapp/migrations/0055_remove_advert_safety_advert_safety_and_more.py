# Generated by Django 4.0.1 on 2024-06-07 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0054_safety_tuning_remove_advert_tuning_advert_safety_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advert',
            name='safety',
        ),
        migrations.AddField(
            model_name='advert',
            name='safety',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.RemoveField(
            model_name='advert',
            name='tuning',
        ),
        migrations.AddField(
            model_name='advert',
            name='tuning',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Safety',
        ),
        migrations.DeleteModel(
            name='Tuning',
        ),
    ]
