from django.shortcuts import render
from .serializers import PaymentSerializer
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Payment
import json
from django.core import serializers
from django.http import JsonResponse

class PaymentViewSet(viewsets.ViewSet):
    def listePayment(self,requets):
        try:
            payments=Payment.objects.all()
            serializer=PaymentSerializer(payments,many=True)
            return JsonResponse(serializer.data,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
    def getPayment(self,request,paymentUid):
        try:
            payment=Payment.objects.get(paymentUid=paymentUid)
            serializer=PaymentSerializer(payment)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def cancelPayment(self,request,paymentUid):
        try:
            payment=Payment.objects.get(paymentUid=paymentUid)
            serializer=PaymentSerializer(payment,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
    def createPayment(self,request):
        try:
            serializer=PaymentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message':'payment ne pas creer'},status=status.HTTP_400_BAD_REQUEST)
    