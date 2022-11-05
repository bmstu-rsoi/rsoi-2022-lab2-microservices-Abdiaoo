from django.urls import path
from django.contrib import admin
from .views import ReservationViewSet

urlpatterns=[
    path('reservations',ReservationViewSet.as_view({
        'get':'Reservations',
        'post':'createReservation'
    })),
    path('reservations/<str:reservationUid>',ReservationViewSet.as_view({
        'get':'getAReservation',
        'patch':'cancelReservation'
    })),
    path('hotels',ReservationViewSet.as_view({
        'get':'Hotels'
    })),
     path('hotels/<str:pk>',ReservationViewSet.as_view({
        'get':'aHotel'
    })),
]