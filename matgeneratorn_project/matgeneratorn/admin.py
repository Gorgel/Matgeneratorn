from django.contrib import admin
from matgeneratorn.models import *
from django_summernote.admin import SummernoteModelAdmin

class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    inlines = (IngredientInline,)

class RecipeTypeAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

# Register your models here.

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Ingredient)
admin.site.register(Unit)
admin.site.register(RecipeType, RecipeTypeAdmin)


