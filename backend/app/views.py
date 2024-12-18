from django.http import JsonResponse
import jwt
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
import stripe

from ticketing_system import settings
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
    #serializer_class = CustomTokenVerifySerializer
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        if(access_token):
            data = request.data.copy()
            data['token'] = access_token
            request._full_data = data

        #return super().post(request, *args, **kwargs)
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            id = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])['user_id']
            response.data['is_superuser'] = User.objects.get(id=id).is_superuser
            response.data['is_organizer'] = User.objects.get(id=id).is_organizer
            response.data['email'] = User.objects.get(id=id).email
            response.data['name'] = User.objects.get(id=id).name
            response.data['id'] = id

        return response
    
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
@permission_classes([IsOrganizerOrReadOnly])
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
            events = events.filter(start_datetime__gte=start_datetime)
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
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def TicketReserve(request, pk):
    if request.method == 'POST':
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if ticket.is_reserved:
            return Response({"error": "Ticket is already reserved"}, status=status.HTTP_400_BAD_REQUEST)
        
        reservation = Reservation.objects.filter(user=request.user, is_finalized=False).first()
        if reservation:
            if reservation.tickets.count() > 4:
                return Response({"error": "Reservation limit exceeded"}, status=status.HTTP_400_BAD_REQUEST)
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
    if request.method == 'GET':
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        
        reservation = Reservation.objects.filter(user=request.user, is_finalized=False).first()
        if reservation and ticket in reservation.tickets.all():
            reservation.tickets.remove(ticket)
            ticket.is_reserved = False
            ticket.save()
            return Response({"message": "Ticket removed from reservation"}, status=status.HTTP_200_OK)
        return Response({"error": "Ticket not found in reservation"}, status=status.HTTP_404_NOT_FOUND)

# api/event/<int:pk>/reservation/
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def EventReservation(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    reservations = Reservation.objects.filter(tickets__event=event, is_finalized=False)
    for reservation in reservations:
        reservation.release()

    reservation = Reservation.objects.filter(tickets__event=event, is_finalized=False, user=request.user)
    tickets = Ticket.objects.filter(id__in=reservation.values_list('tickets', flat=True))
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def PaymentCreate(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        reservation = Reservation.objects.get(user=request.user, is_finalized=False)
        if Reservation.objects.filter(user=request.user, is_finalized=False).count() == 0:
            return Response({"error": "No active reservation found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            reservation.is_finalized = True
            reservation.save()
        tickets = reservation.tickets.all()
        #total = sum(tickets.values_list('price', flat=True))
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = [
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": ticket.event.name,
                            "description": f"Row {ticket.row}, Seat {ticket.seat}",
                        },
                        "unit_amount": int(ticket.price * 100),
                    },
                    "quantity": 1,
                }
                for ticket in tickets
            ],
            mode='payment',
            success_url='http://localhost:5173/success',
            cancel_url='http://localhost:5173/cancel',
        )
        return Response({"id": checkout_session.id}, status=status.HTTP_200_OK)
    except Exception as e:
        reservation.is_finalized = False
        reservation.save()
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)






# test
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def test(request):
    return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)