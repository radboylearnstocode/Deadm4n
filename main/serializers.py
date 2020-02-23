from rest_framework import serializers
from . models import (
    Product,
    Location,
    LocationAndProduct,
    BestDeals
)


class ProductCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"

class LocationCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        fields = "__all__"

class LinkCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LocationAndProduct
        fields = "__all__"
        
class BestDealsCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BestDeals
        fields = "__all__"

