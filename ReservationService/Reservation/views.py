from django.shortcuts import render
from .serializers import HotelSerializer, ReservationSerializer
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Reservation,Hotel
from django.http import JsonResponse
from pytz import timezone

class ReservationViewSet(viewsets.ViewSet):
    def __init__(self):
        if Hotel.objects.count()==0:
            hotel=Hotel(hotelUid="049161bb-badd-4fa8-9d90-87c9a82b0668",name="Ararat Park Hyatt Moscow",country="Россия",city="Москва",address="Неглинная ул., 4",stars=5,price=10000)
            hotel.save()        
    def Hotels(self,request):
        try:
            hotels=Hotel.objects.all()
            serializer=HotelSerializer(hotels,many=True)
            return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)  
    def aHotel(self,request,pk=None):
        try:       
            reservation=Hotel.objects.get(id=pk)
            serializer=HotelSerializer(reservation)
            return JsonResponse(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
    def Reservations(self,request):
        try:
            reservations=Reservation.objects.all()
            serializer=ReservationSerializer(reservations,many=True)
            return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    def createReservation(self,request):
        try:
            serializer=ReservationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print('created')
            return JsonResponse(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
    def getAReservation(self,request,reservationUid=None):
        try:       
            reservation=Reservation.objects.get(reservationUid=reservationUid)
            serializer=ReservationSerializer(reservation)
            return JsonResponse(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
    def cancelReservation(self,request,reservationUid=None):
        try:
            reservation=Reservation.objects.get(reservationUid=reservationUid)
            serializer=ReservationSerializer(reservation,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
