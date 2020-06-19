from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('go/', views.go, name='go'),
    path('export/<str:room_name>/', views.exportcsv, name='exportcsv'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/moderate', views.moderate, name='moderate'),
]
