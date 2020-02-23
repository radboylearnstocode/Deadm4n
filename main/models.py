from django.db import models
import uuid


class Location(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    location_name = models.CharField(max_length=100)
    landmark = models.CharField(max_length=500)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField() 

class LocationAndProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    stock = models.IntegerField()
    discount = models.FloatField()
    
class BestDeals(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    deal = models.CharField(max_length = 500)
    valid_from = models.DateField()
    valid_till = models.DateField()
    


    