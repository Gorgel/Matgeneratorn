from django.conf.urls import url
from matgeneratorn import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'show_recipes/(?P<recipe_type_slug>[\w\-]+)/$',
        views.show_recipes, name='show_recipes'),
    url(r'recipe/(?P<recipe_slug>[\w\-]+)/$',
        views.recipe, name='recipe'),
    url(r'^generator/$', views.generator, name='generator'),
]