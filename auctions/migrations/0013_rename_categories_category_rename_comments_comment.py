# Generated by Django 4.2 on 2024-07-23 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_categories_icons'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
