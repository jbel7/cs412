from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='restaurant_home'),      # /restaurant/
    path('main/', views.main, name='main'),            # /restaurant/main/
    path('order/', views.order, name='order'),         # /restaurant/order/
    path('confirmation/', views.confirmation, name='confirmation'),
]

