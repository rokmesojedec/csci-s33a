# Generated by Django 3.0.3 on 2020-07-06 20:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200706_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image_URL',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlist_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
