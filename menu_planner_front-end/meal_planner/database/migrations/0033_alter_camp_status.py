# Generated by Django 4.2.11 on 2024-05-30 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0032_remove_ingredient_vege_recipexengredient_vege'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camp',
            name='status',
            field=models.CharField(choices=[('En Cours', 'C'), ('Fini', 'F'), ('Pas commencé', 'N')], default='En Cours', max_length=20, verbose_name='Status'),
        ),
    ]
