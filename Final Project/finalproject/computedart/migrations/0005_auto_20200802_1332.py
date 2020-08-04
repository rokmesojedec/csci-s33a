# Generated by Django 3.0.3 on 2020-08-02 13:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computedart', '0004_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuration',
            old_name='grid',
            new_name='square_size',
        ),
        migrations.AddField(
            model_name='configuration',
            name='grid_height',
            field=models.PositiveSmallIntegerField(default=16, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuration',
            name='grid_width',
            field=models.PositiveSmallIntegerField(default=16, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)]),
            preserve_default=False,
        ),
    ]