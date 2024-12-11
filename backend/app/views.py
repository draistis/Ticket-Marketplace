from django.http import JsonResponse
from rest_framework import generics, status, permissions
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework_simplejwt import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import *
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def UserCreate(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(status=status.HTTP_201_CREATED, data=serializer.data)
    else:
        return JsonResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=serializer.errors)

@api_view(['GET'])
@permission_classes([IsSuperUser]) 
def UserList(request):
    output = {}
    output["list"] = list(User.objects.values())
    return JsonResponse(output)

# api/location/
@api_view(['POST', 'GET'])
@permission_classes([IsSuperUserOrReadOnly])
def LocationList(request):
    if request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    elif request.method == 'GET':
        locations = Location.objects.all()
        # Filters
        city = request.query_params.get('city', None)
        country = request.query_params.get('country', None)
        name = request.query_params.get('name', None)
        if city:
            locations = locations.filter(city__icontains=city)
        if country:
            locations = locations.filter(country__icontains=country)
        if name:
            locations = locations.filter(name__icontains=name)
        # Sorting
        sort_by = request.query_params.get('sort_by', None)
        if sort_by:
            locations = locations.order_by(sort_by)
        # Serialize the data
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# api/location/<int:pk>/
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsSuperUserOrReadOnly])
def LocationDetail(request, pk):
    try:
        location = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':        
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    elif request.method == 'DELETE':        
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
