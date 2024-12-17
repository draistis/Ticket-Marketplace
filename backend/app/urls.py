from django.urls import path
from . import views


urlpatterns = [
    path('user/list/', views.UserList, name='user-list'),
    path('user/create/', views.UserCreate, name='user-create'),
    path('auth/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', views.CustomTokenVerifyView.as_view(), name='token_verify'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('location/', views.LocationList, name='location-list'),
    path('location/<int:pk>/', views.LocationDetail, name='location-detail'),
    path('event/', views.EventList, name='event-list'),
    path('event/<int:pk>/', views.EventDetail, name='event-detail'),
    path('event/<int:pk>/tickets/', views.EventTickets, name='event-tickets'),
    path('ticket/', views.TicketList, name='ticket-list'),
    path('ticket/<int:pk>/reserve/', views.TicketReserve, name='ticket-reserve'),
    path('event/<int:pk>/reservation/', views.EventReservation, name='event-reservation'),

    path('test/', views.test, name='test'),
]