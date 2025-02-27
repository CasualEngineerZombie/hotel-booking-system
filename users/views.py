from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from core.decorators import redirect_authenticated_user
from .forms import LoginForm, RegistrationForm
from django.core.mail import send_mail
from django.contrib.auth import logout, login
from django.http import HttpResponse 
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str



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
                    from_email=settings.DEFAULT_FROM_EMAIL,
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
                from_email=settings.DEFAULT_FROM_EMAIL,
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

 

@login_required
def reset_email_page(request):
    """
    Displays a form for the authenticated user to enter a new email address.
    On POST, it saves the new email in the session and redirects to the
    'send_confirmation_email_view' to send the email.
    """
    if request.method == "POST":
        new_email = request.POST.get("email")
        if not new_email:
            return render(
                request,
                "pages/auth/reset_email.html",
                {"error": "Email address is required."},
            )
        # Store the new email in session so the send_confirmation_email_view can retrieve it
        request.session["new_email"] = new_email
        return redirect("send_confirmation_email")  # URL name for send_confirmation_email_view
    return render(request, "pages/auth/reset_email.html")




@require_POST
def send_confirmation_email_view(request):
    """
    Sends a confirmation email. If the user is authenticated and has
    a 'new_email' in session, that address is used. Otherwise, the user's
    current email or a POSTed email is used.
    """
    now = timezone.now()
    last_sent_iso = request.session.get("last_confirmation_email_sent")

    # Optional: Check if 10 minutes have elapsed since the last email
    # if last_sent_iso:
    #     try:
    #         last_sent = timezone.datetime.fromisoformat(last_sent_iso)
    #         if timezone.is_naive(last_sent):
    #             last_sent = timezone.make_aware(last_sent, timezone.utc)
    #         if (now - last_sent).total_seconds() < 600:
    #             return HttpResponse(
    #                 "A confirmation email was sent recently. Please wait a few minutes before trying again.",
    #                 status=429,
    #             )
    #     except Exception:
    #         pass

    # Determine which email to use
    if request.user.is_authenticated:
        # If the user visited reset_email_page, we store the new email in session
        new_email = request.session.pop("new_email", None)
        if new_email:
            recipient = new_email
        else:
            recipient = request.user.email
    else:
        # Fallback: for unauthenticated users, get email from POST
        recipient = request.POST.get("email")
        if not recipient:
            return HttpResponse("Email address is required.", status=400)

    # Send the confirmation email (example uses a plain text message).
    # To use an HTML template, see the "HTML Email Template" section below.
    html_content = render_to_string("emails/email_reset_confirmation.html", {
        # "some_token": some_token_you_generate_for_email_confirmation
    })
    send_mail(
        subject="Email Confirmation",
        message="Please confirm your new email address.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
        html_message=html_content
    )

    # Save the current time in the session
    request.session["last_confirmation_email_sent"] = now.isoformat()

    # Render a success page letting the user know an email was sent
    return render(request, "pages/auth/email_reset_sent.html", {"email": recipient})



@require_POST
def send_password_reset_email_view(request):
    """
    Processes the forgot password form. Sends a password reset email if the email exists.
    """
    email = request.POST.get("email")
    if not email:
        return HttpResponse("Email address is required.", status=400)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # For security, we show the same confirmation page even if the email isn’t found.
        return render(request, "pages/auth/password_reset_email_sent.html", {"email": email})
    
    # Generate a uid and token for password reset.
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    # Build the absolute URL for password reset.
    reset_url = request.build_absolute_uri(f"/reset-password/{uid}/{token}/")
    
    # Render the HTML email template.
    html_message = render_to_string("emails/password_reset_email.html", {
        "user": user,
        "reset_url": reset_url,
    })
    
    send_mail(
        subject="Password Reset Request",
        message=f"Reset your password using this link: {reset_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
        html_message=html_message,
    )
    
    return render(request, "pages/auth/password_reset_email_sent.html", {"email": email})


def reset_password_page(request, uidb64, token):
    """
    Validates the password reset link and displays a form for entering a new password.
    On POST, it updates the user's password.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return HttpResponse("The reset password link is invalid or has expired.", status=400)
    
    context = {"uidb64": uidb64, "token": token}
    
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        if not password1 or not password2:
            context["error"] = "Both password fields are required."
            return render(request, "pages/auth/reset_password.html", context)
        if password1 != password2:
            context["error"] = "Passwords do not match."
            return render(request, "pages/auth/reset_password.html", context)
        
        user.set_password(password1)
        user.save()
        
        # Optionally, log the user in after password reset.
        login(request, user)
        return redirect("login")
    
    return render(request, "pages/auth/reset_password.html", context)