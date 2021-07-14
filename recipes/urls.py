from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('profile/<str:username>/', views.profile, name='profile'),
     path('profile/<str:username>/<int:recipe_id>/edit/',
          views.create_or_update_recipe, name='edit'),
     path('create/', views.create_or_update_recipe, name='create'),
     path('favorites/', views.favorites, name='favorites'),
     path('follows/', views.follows, name='follows'),
     path('profile/<str:username>/<int:recipe_id>/', views.recipe_page,
          name='recipe'),
     path('profile/<str:username>/<int:recipe_id>/delete/',
          views.delete_recipe, name='delete'),
     path('purchases/', views.purchases, name='purchases'),
     path('purchases/download/', views.download_shopping_list, name='download')
]
