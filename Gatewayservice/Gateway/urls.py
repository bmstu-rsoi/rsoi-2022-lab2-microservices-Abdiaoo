from django.urls import path
from django.contrib import admin
from .views import GatewayViewSet

urlpatterns=[
    path('reservations',GatewayViewSet.as_view({
        'get':'UserReservations',
        'post':'bookaHotel'
    })),
     path('reservations/<str:reservationUid>',GatewayViewSet.as_view({
        'get':'UserSpecificReservation',
        'delete':'cancelReservation'
    })),
    path('hotels',GatewayViewSet.as_view({
        'get':'hotels'
    })),
    path('me',GatewayViewSet.as_view({
        'get':'GetInfoUser'
    })),
    path('loyalty',GatewayViewSet.as_view({
        'get':'list_loyalty'
    })),
]
