# Generated by Django 3.0.7 on 2020-07-21 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default='foo'),
            preserve_default=False,
        ),
    ]