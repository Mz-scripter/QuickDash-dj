# Generated by Django 5.1.2 on 2024-12-04 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_restaurant_latitude_restaurant_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
