from dataclasses import fields
from rest_framework import serializers
from .models import Hotel, Reservation
import uuid

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields='__all__'

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hotel
        fields='__all__'
