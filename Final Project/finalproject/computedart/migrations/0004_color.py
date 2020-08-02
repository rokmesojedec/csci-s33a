# Generated by Django 3.0.3 on 2020-08-01 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('computedart', '0003_auto_20200731_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
                ('configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='config_color', to='computedart.Configuration')),
            ],
        ),
    ]
