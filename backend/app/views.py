from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
