# Generated by Django 3.2.5 on 2024-05-13 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0039_auto_20240512_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_image1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
