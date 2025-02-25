from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from core.decorators import redirect_authenticated_user
from .forms import LoginForm, RegistrationForm
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.http import HttpResponse 
from django.utils import timezone
from django.views.decorators.http import require_POST

@redirect_authenticated_user
def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # Using email as username; ensure your registration view sets username = email.
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                send_mail(
                    subject="Login Confirmation",
                    message="You have successfully logged in to your account.",
                    from_email="noreply@hotelxyz.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                return redirect("bookings")
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, "pages/auth/login.html", {"form": form})


@redirect_authenticated_user
def register_page(request):
    user_email = None
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = False
            user_email = user.email
            user.save()
            # Send confirmation email (will appear in the console)
            send_mail(
                subject="Registration Confirmation",
                message="Thank you for registering! Your account has been created.",
                from_email="noreply@hotelxyz.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
            return redirect("registration_success", user_email=user_email)

    else:
        form = RegistrationForm()
    return render(request, "pages/auth/register.html", {"form": form})



@redirect_authenticated_user
def forgot_password_page(request):
    return render(request, "pages/auth/forgot_password.html")
 
def logout_view(request):
    logout(request)
    return redirect("home")

@redirect_authenticated_user
def registrtion_success_view(request, user_email):
    request.session["last_confirmation_email_sent"] = timezone.now().isoformat()
    context = {
        "email" : user_email,
    }
    return render(request, "pages/auth/registration_success.html", context)


@redirect_authenticated_user
@require_POST
def send_confirmation_email_view(request):
    """
    Sends a confirmation email if 10 minutes have elapsed since the last email.
    The timestamp is stored in the session under the key 'last_confirmation_email_sent'.
    """
    now = timezone.now()
    last_sent_iso = request.session.get("last_confirmation_email_sent")
    
    if last_sent_iso:
        try:
            # Convert the ISO string back to a datetime object.
            last_sent = timezone.datetime.fromisoformat(last_sent_iso)
            # Ensure the datetime is timezone aware (assumes UTC if naive)
            if timezone.is_naive(last_sent):
                last_sent = timezone.make_aware(last_sent, timezone.utc)
        except Exception:
            last_sent = None

        if last_sent and (now - last_sent).total_seconds() < 600:
            return HttpResponse(
                "A confirmation email was sent recently. Please wait a few minutes before trying again.",
                status=429,
            )
    
    # Determine the recipient's email.
    # If the user is authenticated, use the user's email.
    # Otherwise, expect an 'email' POST parameter.
    if request.user.is_authenticated:
        recipient = request.user.email
    else:
        recipient = request.POST.get("email")
        if not recipient:
            return HttpResponse("Email address is required.", status=400)

    # Send the confirmation email (using the console email backend)
    send_mail(
        subject="Email Confirmation",
        message="Thank you for registering! Please confirm your email address by clicking the provided link.",
        from_email="noreply@hotelxyz.com",
        recipient_list=[recipient],
        fail_silently=False,
    )
    
    # Save the current time in the session.
    request.session["last_confirmation_email_sent"] = now.isoformat()
    
    return HttpResponse("Confirmation email sent!")
