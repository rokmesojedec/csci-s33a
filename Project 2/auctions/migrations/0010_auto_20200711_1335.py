# Generated by Django 3.0.3 on 2020-07-11 13:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_bids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='bids', through='auctions.Bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
