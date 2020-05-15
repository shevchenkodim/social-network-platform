from django.urls import path
from .views import NotificationsView
from . import views

app_name = 'notification'
urlpatterns = [
    path('', NotificationsView.as_view(), name="notifications"),
]
