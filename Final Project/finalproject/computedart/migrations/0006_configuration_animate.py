# Generated by Django 3.0.3 on 2020-08-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computedart', '0005_auto_20200802_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='animate',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
