# Generated by Django 4.2 on 2024-02-04 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='author_id',
            new_name='author',
        ),
    ]
