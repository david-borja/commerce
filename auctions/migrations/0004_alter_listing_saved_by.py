# Generated by Django 4.2 on 2024-02-04 16:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_winner_id_listing_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='saved_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]