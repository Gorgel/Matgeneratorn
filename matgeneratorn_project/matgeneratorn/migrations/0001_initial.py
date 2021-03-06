# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-17 11:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('picture', models.ImageField(upload_to='images/recipes')),
                ('instructions', models.TextField()),
                ('alternative', models.CharField(max_length=1024)),
                ('public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('ingredient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matgeneratorn.Ingredient')),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matgeneratorn.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('picture', models.ImageField(upload_to='images/types')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matgeneratorn.Unit'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='food_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matgeneratorn.RecipeType'),
        ),
    ]
