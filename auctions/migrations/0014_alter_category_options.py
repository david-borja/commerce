# Generated by Django 4.2 on 2024-07-23 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_rename_categories_category_rename_comments_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]
