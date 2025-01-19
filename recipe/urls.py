from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_recipe, name ="home"),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('main/', views.recommend_recipe, name ="main"),
    path('menu/', views.liked_recipes, name ="menu"),
    path('item/', views.item, name ="item"),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('test/', views.Testitem, name ="test"),
]

