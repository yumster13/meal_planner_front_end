# Generated by Django 4.2.11 on 2024-05-31 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0033_alter_camp_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='number',
            field=models.CharField(max_length=5, verbose_name='Numéro'),
        ),
    ]