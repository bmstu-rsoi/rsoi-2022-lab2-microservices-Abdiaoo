from django.urls import path
from django.contrib import admin
from .views import PaymentViewSet

urlpatterns=[
    path('Payment/<str:paymentUid>',PaymentViewSet.as_view({
        'get':'getPayment',
        'patch':'cancelPayment'
    })),
    path('Payment',PaymentViewSet.as_view({
        'get':'listePayment',
        'post':'createPayment'
    })),
]