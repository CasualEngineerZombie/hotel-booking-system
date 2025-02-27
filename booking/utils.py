from decimal import Decimal
import datetime
import calendar
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def calculate_total_price(room_price, check_in, check_out):
    """
    Calculate the total price for a booking.

    Args:
        room_price (Decimal): The price per night (as a Decimal).
        check_in (date): The check-in date.
        check_out (date): The check-out date.

    Returns:
        Decimal: Total cost calculated as (number of nights * room_price).

    Note:
        - The check-out date is treated as exclusive.
        - If the calculated nights is less than 1 (e.g. same-day check-in/out), 
          it defaults to 1 night.
    """
    nights = (check_out - check_in).days
    if nights < 1:
        nights = 1
    return room_price * Decimal(nights)



def get_stripe_metrics():
    """
    Retrieves real metrics data from Stripe by listing checkout sessions.
    It calculates metrics for the current month versus the previous month.
    """
    now = datetime.datetime.utcnow()

    # Current month start and end
    current_month_start = datetime.datetime(now.year, now.month, 1)
    current_month_end = datetime.datetime(
        now.year, now.month, calendar.monthrange(now.year, now.month)[1], 23, 59, 59
    )
    current_start_ts = int(current_month_start.timestamp())
    current_end_ts = int(current_month_end.timestamp())

    # Previous month start and end
    if now.month == 1:
        prev_year = now.year - 1
        prev_month = 12
    else:
        prev_year = now.year
        prev_month = now.month - 1
    previous_month_start = datetime.datetime(prev_year, prev_month, 1)
    previous_month_end = datetime.datetime(
        prev_year, prev_month, calendar.monthrange(prev_year, prev_month)[1], 23, 59, 59
    )
    prev_start_ts = int(previous_month_start.timestamp())
    prev_end_ts = int(previous_month_end.timestamp())

    # List sessions for the current month (without filtering by payment_status)
    current_sessions = stripe.checkout.Session.list(
        created={"gte": current_start_ts, "lte": current_end_ts},
        limit=100,
    )
    # Filter for paid sessions
    current_paid_sessions = [s for s in current_sessions.data if s.payment_status == "paid"]
    current_bookings = len(current_paid_sessions)
    current_revenue = sum(s.amount_total for s in current_paid_sessions) / 100.0

    # List sessions for the previous month
    prev_sessions = stripe.checkout.Session.list(
        created={"gte": prev_start_ts, "lte": prev_end_ts},
        limit=100,
    )
    prev_paid_sessions = [s for s in prev_sessions.data if s.payment_status == "paid"]
    prev_bookings = len(prev_paid_sessions)
    prev_revenue = sum(s.amount_total for s in prev_paid_sessions) / 100.0

    # For demonstration, active_bookings equals current_bookings
    active_bookings = current_bookings

    def pct_change(new, old):
        if old == 0:
            return 0
        return round(((new - old) / old) * 100, 2)

    metrics = {
        "total_bookings": current_bookings,
        "active_bookings": active_bookings,
        "total_revenue": Decimal(current_revenue),
        "occupancy_rate": None,  # Not available from Stripe; calculate via your own data if needed
        "total_bookings_change": pct_change(current_bookings, prev_bookings),
        "active_bookings_change": pct_change(active_bookings, prev_bookings),
        "total_revenue_change": pct_change(current_revenue, prev_revenue),
        "occupancy_rate_change": 0,  # Placeholder
    }
    return metrics
