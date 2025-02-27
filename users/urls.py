from django.urls import path 
from . import views

urlpatterns = [
    path("login", views.login_page, name="login"),
    path("register", views.register_page, name="register"),
    path("forgot-password", views.forgot_password_page, name="forgot_password"),
    path("logout", views.logout_view, name="logout"),
    path("registration-success/<user_email>", views.registrtion_success_view, name="registration_success"),
    path("forgot-password", views.forgot_password_page, name="forgot_password"),
    path("send-password-reset-email/", views.send_password_reset_email_view, name="send_password_reset_email"),
    path("reset-password/<uidb64>/<token>/", views.reset_password_page, name="reset_password"),
]
