from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications_count = Notification.objects.filter(user_to=request.user, status='new').order_by('-date').count()
    else:
        notifications_count = 0

    kwargs = {
        'notifications_count': notifications_count,
    }
    return kwargs
