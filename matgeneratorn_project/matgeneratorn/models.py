from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.conf import settings


# Create your models here.

class RecipeType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    picture = models.ImageField(upload_to='images/types')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(RecipeType, self).save(*args,**kwargs)

    def __unicode__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    food_type = models.ForeignKey(RecipeType)
    picture = models.ImageField(upload_to='images/recipes')
    instructions = models.TextField()
    alternative = models.CharField(max_length=1024)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    public = models.BooleanField(default=False)
    fast = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args,**kwargs)

    def __unicode__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class Unit(models.Model):
    unit = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.unit

class RecipeIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipe)
    ingredient_id = models.ForeignKey(Ingredient)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit)

    def __unicode__(self):
        return unicode(self.pk)


