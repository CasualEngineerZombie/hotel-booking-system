from django.urls import path 
from . import views

urlpatterns = [
    path("login", views.login_page, name="login"),
    path("register", views.register_page, name="register"),
    path("forgot-password", views.forgot_password_page, name="forgot_password"),
    path("logout", views.logout_view, name="logout"),
    path("registration-success/<user_email>", views.registrtion_success_view, name="registration_success"),
    path("send_confirmation_email_view", views.send_confirmation_email_view, name="send_confirmation_email")
]
