# Generated by Django 3.0.3 on 2020-08-02 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computedart', '0007_configuration_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='topics/%Y/%m/%d/'),
        ),
    ]