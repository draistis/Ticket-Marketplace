from django.urls import path
from . import views


urlpatterns = [
    path('user/list/', views.UserList, name='user-list'),
    path('user/create/', views.UserCreate, name='user-create'),
]