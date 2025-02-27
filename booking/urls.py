from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("bookings", views.booking_list, name="bookings"),
    path("booking/<booking_id>/detail", views.booking_detail, name="booking_detail"),
    path("booking/<booking_id>/update", views.booking_update, name="booking_update"),
    path("booking/<booking_id>/delete", views.booking_delete, name="booking_delete"),
    path("booking/new/<room_uuid>", views.booking_add, name="booking_add"),
    # ROOM LIST
    path("rooms", views.room_list, name="rooms"),
    # Checkout
    path("checkout/<room_uuid>/<booking_uuid>", views.checkout_page, name="checkout"),
    path(
        "checkout/<uuid:room_uuid>/<uuid:booking_uuid>/create-checkout-session/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    path("booking/success/", views.payment_success, name="payment_success"),
    path("booking/cancel/", views.payment_cancel, name="payment_cancel"),
    # ADMIN Page
    path("user-admin", views.admin_page, name="admin_page"),
    path("user-admin/room/new", views.admin_add_room, name="admin_add_room"),
    path(
        "user-admin/room/<room_uuid>/update",
        views.admin_update_room,
        name="admin_update_room",
    ),
    path(
        "user-admin/room/<room_uuid>/delete",
        views.admin_delete_room,
        name="admin_delete_room",
    ),
    path(
        "user-admin/booking/<booking_uuid>/update",
        views.admin_update_booking,
        name="admin_update_booking",
    ),
    path(
        "user-admin/booking/<booking_uuid>/delete",
        views.admin_delete_booking,
        name="admin_delete_booking",
    ),
    # Stripe Webhook
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
]
