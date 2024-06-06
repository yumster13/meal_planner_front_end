# Generated by Django 4.2.11 on 2024-05-27 12:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0017_alter_ingredient_avg_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='moment',
            field=models.CharField(choices=[('MATIN', 'Matin'), ('MIDI', 'Midi'), ('GOUTER', 'Gouter'), ('SOUPER', 'Souper'), ('5EME', 'Cinqieme')], default='MATIN', max_length=10, verbose_name='Moment'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='nbr_anim',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name="nombre d'animés"),
        ),
        migrations.AlterField(
            model_name='menu',
            name='nbr_leaders',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name="nombre d'animateurs"),
        ),
        migrations.AlterField(
            model_name='menu',
            name='nbr_vege',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='nombre de vege'),
        ),
        migrations.CreateModel(
            name='IngredientXSU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=5, max_digits=5, verbose_name='Quantité')),
                ('su', models.BooleanField(default=False, verbose_name='SU ?')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='database.ingredient')),
            ],
        ),
    ]