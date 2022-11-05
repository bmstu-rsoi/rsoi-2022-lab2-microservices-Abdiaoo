from django.db import models
import uuid

class Reservation(models.Model): 
    reservationUid=models.UUIDField(default=uuid.uuid4,unique=True,editable=True)
    username=models.CharField(max_length=200)
    paymentUid=models.UUIDField(default=uuid.uuid4,unique=True,editable=True)
    hotel_id=models.ForeignKey("Hotel",on_delete=models.CASCADE)
    status=models.CharField(max_length=10)
    startDate=models.DateField(auto_now=False)
    endDate=models.DateField(auto_now=False)
    


class Hotel(models.Model):
    hotelUid=models.UUIDField(default=uuid.uuid4,unique=True,editable=True)
    name=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    stars=models.IntegerField()
    price=models.IntegerField()
    
    def __str__(self):
        return self.name