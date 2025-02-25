from django.urls import path 
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("bookings", views.booking_list, name="bookings"),
    path("booking/<booking_id>/detail", views.booking_detail, name="booking_detail"),
    path("booking/<booking_id>/update", views.booking_update, name="booking_update"),
    path("booking/<booking_id>/delete", views.booking_delete, name="booking_delete"),
    path("booking/new", views.booking_add, name="booking_add"),
]
