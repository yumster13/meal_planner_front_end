# Generated by Django 4.2.11 on 2024-06-04 07:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0037_alter_camp_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='recipe',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='recipe'),
        ),
    ]
