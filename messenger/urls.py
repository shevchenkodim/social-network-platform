from django.urls import path
from .views import MessengerView, ChatView
from . import views

app_name = 'messenger'
urlpatterns = [
    path('', MessengerView.as_view(), name='messenger'),
    path('chat/<uuid>/', ChatView.as_view(), name='chat'),
]
