import json
from django.shortcuts import render
import requests
from django.core.paginator import Paginator,EmptyPage
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.http import JsonResponse
import json
from datetime import datetime
from time import sleep
from django.shortcuts import redirect
import time
class GatewayViewSet(viewsets.ViewSet):
    def GetInfoUser(self,request):
        try:
            headers={
            'X-User-Name':request.headers['X-User-Name']
            }
            username=request.headers['X-User-Name']
            user_loyalty=requests.get('http://loyaltyservice:8050/api/v1/loyalty',headers=headers).json()
            reservations=requests.get('http://reservationservice:8070/api/v1/reservations')
            userReservations=[reservation for reservation in reservations.json() if reservation['username']==username]
            infosUser=[]
            for reservation in userReservations:
                hotel=requests.get('http://reservationservice:8070/api/v1/hotels/{}'.format(reservation['hotel_id'])).json()
                payment=requests.get('http://paymentservice:8060/api/v1/Payment/{}'.format(reservation['paymentUid'])).json()
                hotel['fullAddress']=hotel['country']+', '+hotel['city']+', '+hotel['address']
                data={'reservationUid':reservation['reservationUid'],'hotel':hotel,'startDate':reservation['startDate'],'endDate':reservation['endDate'],'status':reservation['status'],'payment':payment}
                infosUser.append(data)
            return JsonResponse({'reservations':infosUser,"loyalty":user_loyalty},status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
    def userLoyalties(self,request):
        headers={
            'X-User-Name':request.headers['X-User-Name']
        }
        loyalties=requests.get('http://loyaltyservice:8050/api/v1/loyalty',headers=headers)
        if loyalties.status_code != 200:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(loyalties.json(),status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
    def bookaHotel(self, request):
        headers = {'X-User-Name': request.headers['X-User-Name']}
        try:
            hotel = requests.get('http://reservationservice:8070/api/v1/hotel/{}'.format(request.data['hotelUid'])).json()
            user_loyalty = requests.get('http://loyaltyservice:8050/api/v1/loyalty', headers=headers).json()
            start_date = datetime.strptime(request.data['startDate'], "%Y-%m-%d")
            end_date = datetime.strptime(request.data['endDate'], "%Y-%m-%d")
            days = (end_date - start_date).days
            price = hotel['price'] * days
            cost = price - (price * user_loyalty['discount'] / 100)
            payment_data = {'status': 'PAID', 'price': cost}
            payment = requests.post('http://paymentservice:8060/api/v1/Payment', json=payment_data).json()
            reservation_count = user_loyalty['reservationCount'] + 1
            status_loyalty = "BRONZE"
            if reservation_count >= 10:
                status_loyalty = "SILVER"
            if reservation_count >= 20:
                status_loyalty = "GOLD"
            loyalty_data = {'status': status_loyalty, 'reservationCount': reservation_count}
            update_loyalty = requests.patch('http://loyaltyservice:8050/api/v1/loyalty/{}'.format(user_loyalty['id']), data=loyalty_data).json()
            reservation_data = {'username': user_loyalty['username'], 'paymentUid': payment['paymentUid'], 'hotel_id': hotel['id'],
                            'status': 'PAID', 'startDate': request.data['startDate'], 'endDate': request.data['endDate']}
            reservation = requests.post('http://reservationservice:8070/api/v1/reservations', data=reservation_data).json()
            data = {'reservationUid': reservation['reservationUid'], 'hotelUid': hotel['hotelUid'], 'startDate': reservation['startDate'],
            'endDate': reservation['endDate'], 'discount': user_loyalty['discount'], 'status': reservation['status'], 'payment': payment}
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def UserSpecificReservation(self,request,reservationUid=None):
        username=request.headers['X-User-Name']
        reservation=requests.get('http://reservationservice:8070/api/v1/reservations/{}'.format(reservationUid))
        hotel=requests.get('http://reservationservice:8070/api/v1/hotels/{}'.format(reservation.json()['hotel_id']))
        payment=requests.get('http://paymentservice:8060/api/v1/Payment/{}'.format(reservation.json()['paymentUid']))
        hoteldict=hotel.json()
        hoteldict['fullAddress']=hotel.json()['country']+', '+hotel.json()['city']+', '+hotel.json()['address']
        if reservation.json()['username']!=username:
            return JsonResponse({'message':'user is not matched'},status=status.HTTP_400_BAD_REQUEST)
        data={'reservationUid':reservation.json()['reservationUid'],'hotel':hoteldict,'hotelUid':hotel.json()['hotelUid'],'startDate':reservation.json()['startDate'],'endDate':reservation.json()['endDate'],'status':reservation.json()['status'],'payment':payment.json()}
        return JsonResponse(data,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
    def hotels(self,request):
        hotels=requests.get('http://reservationservice:8070/api/v1/hotels')
        if hotels.status_code != 200:
            return JsonResponse({'message': 'Erreur lors de la récupération des hôtels'}, status=status.HTTP_400_BAD_REQUEST)
        paginator = Paginator(hotels.json(), request.GET.get('size', 10))
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            return JsonResponse({'message': 'Page demandée est vide'}, status=status.HTTP_400_BAD_REQUEST)
        print(page_obj.object_list)
        return JsonResponse({'items':page_obj.object_list,"totalElements":paginator.count,"page":page_obj.number,"pageSize":paginator.per_page},status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
    def UserReservations(self,request):
        try:
            username=request.headers['X-User-Name']
            reservations=requests.get('http://reservationservice:8070/api/v1/reservations')
            userReservations=[reservation for reservation in reservations.json() if reservation['username']==username]
            infoUserReservations=[]
            for reservation in userReservations:
                hotel=requests.get('http://reservationservice:8070/api/v1/hotels/{}'.format(reservation['hotel_id'])).json()
                payment=requests.get('http://paymentservice:8060/api/v1/Payment/{}'.format(reservation['paymentUid'])).json()
                hotel['fullAddress']=hotel['country']+', '+hotel['city']+', '+hotel['address']
                data={'reservationUid':reservation['reservationUid'],'hotel':hotel,'startDate':reservation['startDate'],'endDate':reservation['endDate'],'status':reservation['status'],'payment':payment}
                infoUserReservations.append(data)
            return JsonResponse(infoUserReservations,status=status.HTTP_200_OK,safe=False,json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
    def cancelReservation(self,request,reservationUid=None):
        try:
            headers={
            'X-User-Name':request.headers['X-User-Name']
            }
            username=request.headers['X-User-Name']
            reservation=requests.patch('http://reservationservice:8070/api/v1/reservations/{}'.format(reservationUid),data={'status':'CANCELED'})
            if reservation.json()['username']==username:
                payment=requests.patch('http://paymentservice:8060/api/v1/Payment/{}'.format(reservation.json()['paymentUid']),data={'status':'CANCELED'})
                user_loyalty=requests.get('http://loyaltyservice:8050/api/v1/loyalty',headers=headers)
                updateloyalty=requests.get('http://loyaltyservice:8050/api/v1/loyalty/{}'.format(user_loyalty.json()['id']))
                if updateloyalty.status_code==200:
                    return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
