from rest_framework.views import APIView
from rest_framework.response import Response

from django.db import connection
import datetime

from .chatbot_script import chatbot_response
from .models import (
    Product,
    Location,
    LocationAndProduct,
    BestDeals
)


from .serializers import (
    ProductCreateSerializer,
    LocationCreateSerializer,
    LinkCreateSerializer,
    BestDealsCreateSerializer
)

from django.db.models import Q

class ProductAddView(APIView):
    
    def get(self, request):
        queryset = Product.objects.all()
        search = request.GET.get('query')
        price = request.GET.get('price')
        if price:
            print(price)
            queryset = queryset.filter(
                price__gte=float(price)
            )
            print(queryset)
        elif search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                |Q(description__icontains=search) 
            )
        else:
            print("Invalid search parameter supplied")
        
        serializer = ProductCreateSerializer(queryset, many=True)
        Response.status_code = 200
        return Response({
            "status": "success",
            "message" : "Products found",
            "payload" : serializer.data
            })
    
    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Response.status_code = 201
            return Response({
                "status": "success",
                "messsage" : "Product successfully created",
                "payload" : serializer.data
            })
            
        else:
            Response.status_code = 400
            return Response({
                "status": "success",
                "message": serializer.errors,
                "payload" : ""
            })


class LocationAddView(APIView):
    
    def get(self, request):
        queryset = Location.objects.all()
        search = request.data.get('query')
        stock = request.data.get('stock')
        if stock:
            queryset = queryset.filter(
                stock__lte=int(stock)
            )
        elif search:
            queryset = queryset.filter(
                Q(location_name__icontains=search)
                |Q(landmark__icontains=search) 
            )
        else:
            print("Invalid search parameter supplied")
        
        serializer = LocationCreateSerializer(queryset, many=True)
        Response.status_code = 200
        return Response({
            "status": "success",
            "message" : "Location found",
            "payload" : serializer.data
            })
    
    def post(self, request):
        serializer = LocationCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Response.status_code = 201
            return Response({
                "status": "success",
                "messsage" : "Location successfully created",
                "payload" : serializer.data
            })
            
        else:
            Response.status_code = 400
            return Response({
                "status": "errors",
                "message": serializer.errors,
                "payload" : ""
            })

class LinkingProductAndLocationView(APIView):

    def get(self, request):
        queryset = LocationAndProduct.objects.all()
        discount = request.data.get('discount')
        if discount:
            queryset = queryset.filter(
                discount__lte=float(discount)
            )
        else:
            print("Invalid discount parameter supplied")
        
        serializer = LinkCreateSerializer(queryset, many=True)
        Response.status_code = 200
        return Response({
            "status": "success",
            "message" : "Link found",
            "payload" : serializer.data
            })
    
    def post(self, request):
        serializer = LinkCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Response.status_code = 201
            return Response({
                "status": "success",
                "messsage" : "Link successfully created between product and location",
                "payload" : serializer.data
            })
            
        else:
            Response.status_code = 400
            return Response({
                "status": "errors",
                "message": serializer.errors,
                "payload" : ""
            })

class BestDealView(APIView):
    
    def get(self, request):
        queryset = BestDealView.objects.all()
        
        expires_at = request.data.get('expires')
        starts_at = request.data.get('starts')
        deal = request.data.get('deal')
        if deal:
            queryset = queryset.filter(
                deal__icontains=float(deal)
            )
        elif starts_at:
            queryset = queryset.filter(
                valid_from__lte=datetime.date.today()
            )
        elif expires_at:
            queryset = queryset.filter(
                expires_at__gte=datetime.date.today()
            )
        else:
            print("Invalid discount parameter supplied")
        
        serializer = LinkCreateSerializer(queryset, many=True)
        Response.status_code = 200
        return Response({
            "status": "errors",
            "message" : "Link found",
            "payload" : serializer.data
            })
    
    def post(self, request):
        serializer = LinkCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Response.status_code = 201
            return Response({
                "status": "success",
                "messsage" : "Link successfully created between product and location",
                "payload" : serializer.data
            })
            
        else:
            Response.status_code = 400
            return Response({
                "status": "errors",
                "message": serializer.errors,
                "payload" : ""
            })


class ChatBot(APIView):
    
    def post(self, request):
        queryset = Product.objects.all()
        client_request = request.data.get('chat')
        if client_request == ' ':
            return Response({"status": "success", 
                             "message": "Quitting chatbot, have a nice day",
                             "payload": " "
                                 })
        
        response = chatbot_response(client_request)
        sentence = ["Please enter the name of the product,you are looking for: ", "Please enter the description of the product,you are looking for: "]
        sentence_1 = ["I hope these items will make you buy them: ", "Hope you find what you are looking for in these:","Here are some of things you maybe interested in: "]
        if response in sentence:
            search = request.data.get('search')
            if not search:
                Response.status_code = 400
                return Response({
                    "status": "error",
                    "message": "Need a search parameter",
                    "payload" :""
                })
            queryset = queryset.filter(
                Q(name__icontains=search)
                |Q(description__icontains=search) 
            )
        elif response in sentence_1:
            pass
        serializer = ProductCreateSerializer(queryset, many=True)
        return Response(
            {
                "status" :"success",
                "message":response,
                "payload": serializer.data
            }
        )
            