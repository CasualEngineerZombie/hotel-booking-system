from django.contrib import admin

from booking.models import Booking, Room

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'room_number', 'room_type', 'price', 'is_available')
    search_fields = ('room_number', 'room_type')
    list_filter = ('room_type', 'is_available')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'guest_email', 'room', 'check_in', 'check_out', 'created_at')
    search_fields = ('guest_name', 'guest_email', 'room__room_number')
    list_filter = ('check_in', 'check_out')