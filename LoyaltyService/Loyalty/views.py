from django.shortcuts import render
from .serializers import UserLoyaltySerializer
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import UserLoyalty
import json
from django.http import JsonResponse
from django.core import serializers
class LoyaltyViewSet(viewsets.ViewSet):
    def __init__(self):
        if UserLoyalty.objects.count()==0:
            user=UserLoyalty(username="Test Max",reservationCount=25,status="GOLD",discount=10)
            user.save()

    def Loyalties(self,request):
        try:
            loyalties=UserLoyalty.objects.all()
            serializer=UserLoyaltySerializer(loyalties,many=True)
            return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def DecrementLoyalty(self,request,pk=None):
        try:
            userloyalty=UserLoyalty.objects.get(id=pk)
            print(userloyalty.reservationCount)
            userloyalty.reservationCount-=1
            if(userloyalty.reservationCount>=10):
                userloyalty.status="SILVER"
            if(userloyalty.reservationCount>=20):
                userloyalty.status="GOLD"
            if(userloyalty.reservationCount<10):
                userloyalty.status="BRONZE"
            if(userloyalty.reservationCount<0):
                userloyalty.status="BRONZE"
            seriailzer=UserLoyaltySerializer(userloyalty)
            return JsonResponse(seriailzer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        try:
            status_list = {"BRONZE": 5, "SILVER": 7, "GOLD": 10}
            status_key = list(status_list.keys())
            loyalty=UserLoyalty.objects.get(id=pk)
            if request.data['status'] in status_list:
                serializer=UserLoyaltySerializer(loyalty,data=request.data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return JsonResponse(serializer.data,status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

