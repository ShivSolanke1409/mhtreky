from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def organizer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if not request.user.is_organizer:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view
