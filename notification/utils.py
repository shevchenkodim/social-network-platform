from .models import Notification
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model


def notify_user(user_to, message):
    Notification.objects.create(user_to=user_to, message=message)


def notify_myself(request, message):
    if request.user.is_authenticated:
        Notification.objects.create(user_to=request.user, message=message)
    else:
        raise PermissionDenied
