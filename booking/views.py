from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from booking.forms import BookingUpdateForm, BookingCreateForm
from booking.models import Booking, Room
from core.decorators import admin_required

 
def home_page(request):
    return render(request, "pages/home/home.html")


@login_required(login_url="login")
def booking_list(request):
    bookings = Booking.objects.all()
    context = {
        "bookings": bookings,
    }
    return render(request, "pages/booking/booking_list.html", context)


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "pages/booking/booking_detail.html", {"booking": booking})


def booking_update(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        form = BookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect("bookings")  # Change to your booking list view
    else:
        form = BookingUpdateForm(instance=booking)

    return render(request, "pages/booking/booking_update.html", {"form": form})


def booking_delete(request, booking_id):
    if request.method == "POST":
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return redirect("bookings")


def booking_add(request):
    if request.method == "POST":
        form = BookingCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bookings")
    else:
        form = BookingCreateForm()
    return render(request, "pages/booking/booking_add.html", {"form": form})


def room_list(request):
    rooms = Room.objects.filter(is_available=True)
    
    context = {
        "rooms": rooms,
    }
    return render(request, "pages/room/room_list.html", context)


def checkout_page(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    context = {
        "room" : room,
    }
    return render(request, "pages/checkout/checkout_booking.html", context)

def checkout_success(request):
    return render(request, "pages/checkout/checkout_succes.html")

@admin_required
def admin_page(request):
    return render(request, "pages/admin/admin_page.html")