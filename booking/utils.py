from decimal import Decimal

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
