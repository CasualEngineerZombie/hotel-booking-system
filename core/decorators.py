from functools import wraps
from django.shortcuts import redirect


def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and is an admin (staff)
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
