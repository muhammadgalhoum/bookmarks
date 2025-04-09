from django.urls import path

from .views import *


app_name='images'

urlpatterns = [
    path('', image_list, name='list'),
    path('create/', image_create, name='create'),
    path('update/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         image_update, name='image_update'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         image_detail, name='image_detail'),
    path('like/', image_like, name='like'),
    path('ranking/', image_ranking, name='ranking'),
]
