# Generated by Django 4.2 on 2024-05-22 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_rename_highest_bid_id_listing_highest_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='slug',
            field=models.SlugField(default='', max_length=64, unique=True),
        ),
    ]
