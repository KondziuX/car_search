# Generated by Django 3.2.5 on 2023-01-07 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0013_alter_advert_featured_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advert',
            old_name='featured_image',
            new_name='featured_image1',
        ),
        migrations.AddField(
            model_name='advert',
            name='featured_image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='advert',
            name='featured_image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
