# Generated by Django 3.0.3 on 2020-08-03 13:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computedart', '0009_auto_20200802_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='color_chance',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
    ]
