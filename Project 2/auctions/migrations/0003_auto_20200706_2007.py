# Generated by Django 3.0.3 on 2020-07-06 20:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
            ],
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='description',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
        migrations.AddField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bid_listing', to='auctions.Listing'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_listing', to='auctions.Listing'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='intial_bid',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='listing',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlist_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AddField(
            model_name='listing',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='category_items', to='auctions.Category'),
        ),
    ]
