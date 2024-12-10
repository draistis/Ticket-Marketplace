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


#@csrf_exempt
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#@csrf_exempt
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
@permission_classes([permissions.IsAuthenticated&IsSuperUser]) 
def UserList(request):
    output = {}
    output["list"] = list(User.objects.values())
    return JsonResponse(output)

# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS

# class ExampleView(APIView):
#     permission_classes = [IsAuthenticated|ReadOnly]

#     def get(self, request, format=None):
#         content = {
#             'status': 'request was permitted'
#         }
#         return Response(content)

# @api_view(['GET'])
# @authentication_classes([authentication.JWTAuthentication])
# @permission_classes([])
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# @api_view(['POST'])
# @authentication_classes([authentication.JWTAuthentication])
# @permission_classes([])
# class UserCreate(generics.CreateAPIView):
    