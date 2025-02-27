from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from booking.forms import BookingUpdateForm, BookingCreateForm
from booking.models import Booking, Room
from core.decorators import admin_required
from django.conf import settings 
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


def home_page(request):
    rooms = Room.objects.filter(is_available=True)[:3]
    context = {
        "rooms": rooms,
    }
    return render(request, "pages/home/home.html", context)


@login_required(login_url="login")
def booking_list(request):
    bookings = Booking.objects.filter(guest_email=request.user.email)
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


def booking_add(request, room_uuid):
    room = get_object_or_404(Room, room_uuid=room_uuid)
    if request.method == "POST":
        form = BookingCreateForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.guest_email = request.user.email
            booking.save()
            return redirect(
                "checkout", room_uuid=room.room_uuid, booking_uuid=booking.booking_uuid
            )
    else:
        form = BookingCreateForm(initial={"room": room})
    context = {
        "form": form,
        "room": room,
    }
    return render(request, "pages/booking/booking_add.html", context)


def create_checkout_session(request, room_uuid, booking_uuid):
    room = get_object_or_404(Room, room_uuid=room_uuid)
    booking = get_object_or_404(Booking, booking_uuid=booking_uuid)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "php",
                    "product_data": {
                        # 'images': [room.photo.url],
                        "name": room.room_name,
                        "description": room.description,
                    },
                    "unit_amount": int(room.price * 100),
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        customer_email=request.user.email,
        success_url=settings.YOUR_DOMAIN
        + f"/booking/success/?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=settings.YOUR_DOMAIN
        + f"/booking/cancel/?session_id={{CHECKOUT_SESSION_ID}}",
        metadata={
            "total_guest": booking.total_guest,
            "booking_uuid": booking.booking_uuid,
            "room_uuid": room.room_uuid,
        },
    )

    return redirect(checkout_session.url)


def payment_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        # Optionally, you could also redirect or show an error message
        return render(request, "pages/checkout/payment_success.html", {"error": "Session ID missing."})

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        # Optionally log the error here
        return render(request, "pages/checkout/payment_success.html", {"error": "Could not retrieve session."})

    booking_uuid = session.get("metadata", {}).get("booking_uuid")
    booking = get_object_or_404(Booking, booking_uuid=booking_uuid)
    room = booking.room  # assuming Booking has a foreign key to Room
    payment_id = session.get("payment_intent")

    # Prepare and send a confirmation email to the guest
    subject = "Booking Confirmation"
    email_context = {
        "booking": booking,
        "room": room,
        "payment_id": payment_id,
    }
    message_html = render_to_string("emails/booking_confirmation_email.html", email_context)
    recipient_list = [booking.guest_email]
    send_mail(
        subject,
        message_html,  # Using the HTML content as the message body; you could also provide a plain text version
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        html_message=message_html,
    )

    context = {
        "booking": booking,
        "room": room,
        "payment_id": payment_id,
    }
    return render(request, "pages/checkout/payment_success.html", context)



def payment_cancel(request):
    session_id = request.GET.get("session_id")
    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        booking_uuid = session.get("metadata", {}).get("booking_uuid")
        booking = get_object_or_404(Booking, booking_uuid=booking_uuid)
        room = booking.room  # assuming Booking has a foreign key to Room
        payment_id = session.get("payment_intent")
        context = {
            "booking": booking,
            "room": room,
            "payment_id": payment_id,
        }
        return render(request, "pages/checkout/payment_cancel.html", context)
    # Optionally handle missing session_id
    return render(request, "pages/checkout/payment_cancel.html")



def room_list(request):
    rooms = Room.objects.filter(is_available=True)

    context = {
        "rooms": rooms,
    }
    return render(request, "pages/room/room_list.html", context)


@login_required
def checkout_page(request, room_uuid, booking_uuid):
    room = get_object_or_404(Room, room_uuid=room_uuid)
    booking = get_object_or_404(Booking, booking_uuid=booking_uuid)
    context = {
        "room": room,
        "booking": booking,
    }
    return render(request, "pages/checkout/checkout_booking.html", context)


@admin_required
def admin_page(request):
    rooms = Room.objects.all()
    bookings = Booking.objects.all()

    context = {
        "rooms": rooms,
        "bookings": bookings,
    }
    return render(request, "pages/admin/admin_page.html", context)


@admin_required
def admin_add_room(request):
    return render(request, "pages/admin/room/admin_add_room.html")


@admin_required
def admin_update_room(request, room_uuid):
    return render(request, "pages/admin/room/admin_update_room.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout session completed event
    if (
        event["type"] == "checkout.session.completed"
        or event["type"] == "payment_intent.succeeded"
        or event["type"] == "checkout.session.async_payment_succeeded"
    ):
        session = event["data"]["object"]
        # Retrieve the booking's UUID from the session metadata
        booking_uuid = session.get("metadata", {}).get("booking_uuid")
        if booking_uuid:
            booking = get_object_or_404(Booking, booking_uuid=booking_uuid)
            booking.paid = True
            booking.save()

    # Return a 200 response to acknowledge receipt of the event
    return HttpResponse(status=200)
