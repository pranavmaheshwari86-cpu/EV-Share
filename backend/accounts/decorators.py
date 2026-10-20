"""
Authentication & Authorization Decorators for MongoEngine documents.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

def login_required_mongo(view_func):
    """
    Ensures that an active MongoEngine User is present on request.current_user.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not getattr(request, 'current_user', None):
            messages.warning(request, "Please log in to access this page.")
            login_url = reverse('accounts:login')
            return redirect(f"{login_url}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required_mongo(required_role):
    """
    Ensures the user has the specified role (or is superuser).
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = getattr(request, 'current_user', None)
            if not user:
                messages.warning(request, "Please log in to continue.")
                login_url = reverse('accounts:login')
                return redirect(f"{login_url}?next={request.path}")
                
            if not user.has_role(required_role):
                messages.error(request, f"Access restricted. You need '{required_role}' privileges.")
                return redirect('home')
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
