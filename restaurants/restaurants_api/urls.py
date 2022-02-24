from django.urls import path

from .views import database_update, get_restaurants_list


urlpatterns = [
    path('update/', database_update, name='update'),
    path('burger_king/', get_restaurants_list, name='restaurants_list'),
]
