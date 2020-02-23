from django.urls import path
from . import views

urlpatterns = [
    path('product/add/', views.ProductAddView.as_view()),
    path('location/add/', views.LocationAddView.as_view()),
    path('link/add/', views.LinkingProductAndLocationView.as_view()),
    path('best_deals/add/', views.BestDealView.as_view()),
    path('chat/', views.ChatBot.as_view()),
]
