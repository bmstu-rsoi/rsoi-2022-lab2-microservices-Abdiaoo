import json
from django.shortcuts import render
import requests
from django.core.paginator import Paginator
from django.core import serializers
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.http import JsonResponse
import json
from datetime import datetime
from time import sleep
from django.shortcuts import redirect
import time
class GatewayViewSet(viewsets.ViewSet):
    
    def list_loyalty(self,request):
        username=request.headers['X-User-Name']
        loyalties=requests.get('http://localhost:8050/api/v1/loyalty')
        time.sleep(10)
        for loyalty in loyalties.json():
            if loyalty['username']==username:
                userLoyalty=loyalty
                break
        
        if loyalties.status_code != 200:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(userLoyalty,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
    def bookaHotel(self,request):
        try:
            username=request.headers['X-User-Name']
            hotels=requests.get('http://localhost:8070/api/v1/hotels')
            time.sleep(5)
            for hotel in hotels.json():
                if hotel['hotelUid']==request.data['hotelUid']:
                    choosedHotel=hotel
                    break
            loyalties=requests.get('http://localhost:8050/api/v1/loyalty')
            time.sleep(5)
            for loyalty in loyalties.json():
                if loyalty['username']==username:
                    userLoyalty=loyalty
                    break
            d1 = datetime.strptime(request.data['endDate'], "%Y-%m-%d")
            d2 = datetime.strptime(request.data['startDate'], "%Y-%m-%d")
            days=d1-d2
            price=hotel['price']*days.days
            cost=price-(price*userLoyalty['discount']/100)
            payment=requests.post('http://localhost:8060/api/v1/Payment',json={'status':'PAID','price':cost})
            time.sleep(5)
            numberReservation=userLoyalty['reservationCount']+1
            status_loyalty="BRONZE"
            if(numberReservation>=10):
                status_loyalty="SILVER"
            if(numberReservation>=20):
                status_loyalty="GOLD"
            updateloyalty=requests.patch('http://localhost:8050/api/v1/loyalty/{}'.format(userLoyalty['id']),data={'status':status_loyalty,'reservationCount':numberReservation})
            time.sleep(5)
            data={'username':userLoyalty['username'],'paymentUid':payment.json()['paymentUid'],'hotel_id':choosedHotel['id'],'status':'PAID','startDate':request.data['startDate'],'endDate':request.data['endDate']}
            reservation=requests.post('http://localhost:8070/api/v1/reservations',data=data)
            time.sleep(5)
            data={'reservationUid':reservation.json()['reservationUid'],'hotelUid':choosedHotel['hotelUid'],'startDate':reservation.json()['startDate'],'endDate':reservation.json()['endDate'],'discount':userLoyalty['discount'],'status':reservation.json()['status'],'payment':payment.json()}
            return JsonResponse(data,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def GetInfoUser(self,request):
        try:
            
            username=request.headers['X-User-Name']
            loyalties=requests.get('http://localhost:8050/api/v1/loyalty')
            time.sleep(5)
            for loyalty in loyalties.json():
                if loyalty['username']==username:
                    userLoyalty=loyalty
                    break
            reservations=requests.get('http://localhost:8070/api/v1/reservations')
            time.sleep(5)
            userReservations=[reservation for reservation in reservations.json() if reservation['username']==username]
            
            hotels=requests.get('http://localhost:8070/api/v1/hotels')
            time.sleep(5)
            payments=requests.get('http://localhost:8060/api/v1/Payment')
            time.sleep(5)
            infosUser=[]
            for reservation in userReservations:
                for hotel in hotels.json():
                    if hotel['id']==reservation['hotel_id']:
                        reservedHotel=hotel
                        break
                for paymen in payments.json():
                    if paymen['paymentUid']==reservation['paymentUid']:
                        payment=paymen
                        break
                reservedHotel['fullAddress']=reservedHotel['country']+', '+reservedHotel['city']+', '+reservedHotel['address']
                data={'reservationUid':reservation['reservationUid'],'hotel':reservedHotel,'startDate':reservation['startDate'],'endDate':reservation['endDate'],'status':reservation['status'],'payment':payment}
                infosUser.append(data)
            return JsonResponse({'reservations':infosUser,"loyalty":userLoyalty},status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def UserSpecificReservation(self,request,reservationUid=None):
        username=request.headers['X-User-Name']
        reservation=requests.get('http://localhost:8070/api/v1/reservations/{}'.format(reservationUid))
        time.sleep(5)
        hotel=requests.get('http://localhost:8070/api/v1/hotels/{}'.format(reservation.json()['hotel_id']))
        time.sleep(5)
        payment=requests.get('http://localhost:8060/api/v1/Payment/{}'.format(reservation.json()['paymentUid']))
        time.sleep(5)
        hoteldict=hotel.json()
        hoteldict['fullAddress']=hotel.json()['country']+', '+hotel.json()['city']+', '+hotel.json()['address']
        if reservation.json()['username']!=username:
            return JsonResponse({'message':'je sais pas'},status=status.HTTP_400_BAD_REQUEST)
        data={'reservationUid':reservation.json()['reservationUid'],'hotel':hoteldict,'hotelUid':hotel.json()['hotelUid'],'startDate':reservation.json()['startDate'],'endDate':reservation.json()['endDate'],'status':reservation.json()['status'],'payment':payment.json()}
        return JsonResponse(data,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
    def hotels(self,request):
        
        hotels=requests.get('http://localhost:8070/api/v1/hotels')
        time.sleep(5)
        paginator = Paginator(hotels.json(), request.GET.get('size'))
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if hotels.status_code != 200:
            return JsonResponse({'message':'je sais pas'},status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'items':hotels.json(),"totalElements":len(hotels.json()),"page":request.GET.get('page'),"pageSize":int(request.GET.get('size'))},status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
    
        
    def UserReservations(self,request):
        try:
            username=request.headers['X-User-Name']
            reservations=requests.get('http://localhost:8070/api/v1/reservations')
            time.sleep(5)
            userReservations=[reservation for reservation in reservations.json() if reservation['username']==username]
            infoUserReservations=[]
            hotels=requests.get('http://localhost:8070/api/v1/hotels')
            time.sleep(5)
            payments=requests.get('http://localhost:8060/api/v1/Payment')
            time.sleep(5)
            for reservation in userReservations:
                for hotel in hotels.json():
                    if hotel['id']==reservation['hotel_id']:
                        reservedHotel=hotel
                        break
                for paymen in payments.json():
                    if paymen['paymentUid']==reservation['paymentUid']:
                        payment=paymen
                reservedHotel['fullAddress']=reservedHotel['country']+', '+reservedHotel['city']+', '+reservedHotel['address']
                data={'reservationUid':reservation['reservationUid'],'hotel':reservedHotel,'startDate':reservation['startDate'],'endDate':reservation['endDate'],'status':reservation['status'],'payment':payment}
                infoUserReservations.append(data)
            return JsonResponse(infoUserReservations,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def cancelReservation(self,request,reservationUid=None):
        try:
            username=request.headers['X-User-Name']
            reservation=requests.patch('http://localhost:8070/api/v1/reservations/{}'.format(reservationUid),data={'status':'CANCELED'})
            time.sleep(5)
            if reservation.json()['username']==username:
                payment=requests.patch('http://localhost:8060/api/v1/Payment/{}'.format(reservation.json()['paymentUid']),data={'status':'CANCELED'})
                time.sleep(5)
                loyalties=requests.get('http://localhost:8050/api/v1/loyalty')
                time.sleep(5)
                for loyalty in loyalties.json():
                    if loyalty['username']==username:
                        userLoyalty=loyalty
                        break
                updateloyalty=requests.get('http://localhost:8050/api/v1/loyalty/{}'.format(userLoyalty['id']))
                time.sleep(5)
                if updateloyalty.status_code==200:
                    return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
