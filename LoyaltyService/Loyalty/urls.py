from django.urls import path
from django.contrib import admin
from .views import LoyaltyViewSet

urlpatterns=[
    path('loyalty',LoyaltyViewSet.as_view({
        'get':'Loyalties'
    })),
    path('loyalty/<str:pk>',LoyaltyViewSet.as_view({
        'patch':'update',
        'get':'DecrementLoyalty'
    })),
]