from django.urls import path
from . import views


urlpatterns = [
    path('user/list/', views.UserList.as_view(), name='user-list'),
    path('user/create/', views.UserCreate.as_view(), name='user-create'),
]