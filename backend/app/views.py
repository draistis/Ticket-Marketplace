from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import *
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if(response.status_code == 200):
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                httponly=True,
                path='/',
                secure=True,
                samesite='None'
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                httponly=True,
                path='/',
                secure=True,
                samesite='None'
            )

        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        if(refresh_token):
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if(response.status_code == 200):
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                httponly=True,
                path='/',
                secure=True,
                samesite='None'
            )

        return response
    
class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        if(access_token):
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie(
            'access',
            '',
            httponly=True,
            path='/',
            secure=True,
            samesite='None'
        )
        response.set_cookie(
            'refresh',
            '',
            httponly=True,
            path='/',
            secure=True,
            samesite='None'
        )

        return response

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
    
# api/event/
@api_view(['POST', 'GET'])
@permission_classes([IsSuperUserOrReadOnly])
def EventList(request):
    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    elif request.method == 'GET':
        events = Event.objects.all()
        # Query
        query = request.query_params.get('query', None)
        if query:
            events = events.filter(name__icontains=query) | events.filter(description__icontains=query)
        # Filters
        category = request.query_params.get('category', None)
        start_datetime = request.query_params.get('start_datetime', None)
        city = request.query_params.get('city', None)
        country = request.query_params.get('country', None)
        if category:
            events = events.filter(category__icontains=category)
        if start_datetime:
            events = events.filter(start_datetime >= start_datetime)
        if city:
            events = events.filter(location__city__icontains=city)
        if country:
            events = events.filter(location__country__icontains=country)
        # Sorting
        sort_by = request.query_params.get('sort_by', None)
        if sort_by:
            events = events.order_by(sort_by)
        # Serialize the data
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# api/event/<int:pk>/
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsSuperUserOrReadOnly])
def EventDetail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':        
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    elif request.method == 'DELETE':        
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# api/event/<int:pk>/tickets/
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def EventTickets(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    reservations = Reservation.objects.filter(tickets__event=event, is_finalized=False)
    for reservation in reservations:
        reservation.release()

    tickets = Ticket.objects.filter(event=event, is_reserved=False)
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# api/ticket/
@api_view(['POST', 'GET'])
@permission_classes([IsSuperUser])
def TicketList(request):
    if request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    elif request.method == 'GET':
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# api/ticket/<int:pk>/reserve/
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def TicketReserve(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if ticket.is_reserved:
        return Response({"error": "Ticket is already reserved"}, status=status.HTTP_400_BAD_REQUEST)
    
    reservation = Reservation.objects.filter(user=request.user, is_finalized=False).first()
    if reservation:
        reservation.tickets.add(ticket)
        ticket.is_reserved = True
        ticket.save()
    else:
        reservation = Reservation(user=request.user)
        reservation.save()
        reservation.tickets.add(ticket)
        ticket.is_reserved = True
        ticket.save()
    
    return Response({"message": "Ticket reserved successfully"}, status=status.HTTP_200_OK)









# test
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def test(request):
    return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)