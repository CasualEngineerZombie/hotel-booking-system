# Hotel Booking System

A Django-based hotel booking application with Stripe integration, room management, booking creation, and admin dashboard.

## Features

- **Room Management**: Add, update, and delete rooms (with amenities, capacity, etc.).
- **Booking Flow**: Create and update bookings, including check-in/out dates, number of guests, and special requests.
- **Stripe Payment**: Secure checkout process with Stripe integration.
- **Admin Dashboard**: Manage rooms and bookings in an admin panel.
- **Filters & Client-Side Features**: (Optional) Alpine.js client-side filters for rooms, etc.

---

## 1. Prerequisites

- **Python** 3.8+
- **pip** (comes with Python)
- **Git** (to clone the repository)
- **Virtual Environment** tool (e.g. `venv`) recommended
- **SQLite** (installed by default on most systems) or another database
- **Stripe** account (if you want to test real payments)

---

## 2. Clone the Repository

```bash
git clone https://github.com/CasualEngineerZombie/hotel-booking-system.git
cd hotel-booking-system
```

---

## 3. Create and Activate a Virtual Environment (Optional but Recommended)

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note**: Make sure you have a `requirements.txt` file listing all necessary packages (e.g., `Django`, `stripe`, etc.).

---

## 5. Configure Environment Variables

Create a `.env` file or set environment variables as needed:

```bash
# Example .env
SECRET_KEY="your-django-secret-key"
DEBUG=True

# Stripe Keys
STRIPE_SECRET_KEY="sk_test_xxx"
STRIPE_PUBLISHABLE_KEY="pk_test_xxx"
STRIPE_WEBHOOK_SECRET="whsec_xxx"

# Domain (used in Stripe success/cancel URLs)
YOUR_DOMAIN="http://localhost:8000"

# Email settings (optional)
EMAIL_HOST="smtp.your-email-provider.com"
EMAIL_HOST_USER="youremail@example.com"
EMAIL_HOST_PASSWORD="your-email-password"
EMAIL_PORT=587
DEFAULT_FROM_EMAIL="noreply@hotelxyz.com"
```

> **Make sure** your `settings.py` reads these environment variables to configure Django, Stripe, and other services.

---

## 6. Run Database Migrations

```bash
python manage.py migrate
```

---

## 7. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

This allows you to log into Django’s built-in admin panel at `/admin`.

---

## 8. Collect Static Files (Production Only)

If you’re deploying to production, you’ll need to collect static files:

```bash
python manage.py collectstatic
```

---

## 9. Run the Server

```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) in your browser to see the application.

---

## 10. Usage

- **Home Page**: Lists available rooms, quick navigation.
- **Room List**: Displays all rooms with an option to “Book Now.”
- **Booking Flow**:
  1. Select a room and click **Book Now**.
  2. Fill in your booking details (guest name, dates, etc.).
  3. Proceed to checkout to pay via Stripe.
- **Admin Dashboard**: Visit `http://localhost:8000/admin` (or your custom admin page). Manage rooms, amenities, and bookings.

---

## 11. Testing Stripe Webhooks (Optional)

If you want to test Stripe’s webhook locally:

1. Install the [Stripe CLI](https://stripe.com/docs/stripe-cli).
2. Run `stripe listen --forward-to localhost:8000/stripe/webhook/`.
3. Test events: `stripe trigger checkout.session.completed`.

Ensure your `STRIPE_WEBHOOK_SECRET` matches the secret provided by the CLI or your Stripe dashboard.

---

## 12. Contributing

1. Fork the project and clone your fork.
2. Create a new branch for your feature: `git checkout -b feature/new-feature`.
3. Commit changes: `git commit -m 'Add new feature'`.
4. Push to your branch: `git push origin feature/new-feature`.
5. Create a Pull Request on GitHub.

---

## 13. License

This project is available under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

**Enjoy your Django Hotel Booking System!** If you have any questions or issues, feel free to open an issue or submit a pull request.
