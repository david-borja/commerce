# Generated by Django 4.2 on 2024-06-03 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='icons',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
