from django.urls import path
from . import views


urlpatterns = [
    path('user/list/', views.UserList, name='user-list'),
    path('user/create/', views.UserCreate, name='user-create'),

    path('location/', views.LocationList, name='location-list'),
    path('location/<int:pk>/', views.LocationDetail, name='location-detail'),
    path('event/', views.EventList, name='event-list'),
    path('event/<int:pk>/', views.EventDetail, name='event-detail'),
]