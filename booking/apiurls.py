from django.urls import path
from . import views

urlpatterns = [
    path('cars/', views.car_operations, name='car_operations'),
    path('cars/<str:carId>/', views.specific_car_operations, name='specific_car_operations'),
    path('bookings/', views.booking_operations, name='booking_operations'),
]
