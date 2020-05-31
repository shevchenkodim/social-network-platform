from django.urls import path
from .views import MessengerView, ChatView
from . import views

app_name = 'messenger'
urlpatterns = [
    path('', MessengerView.as_view(), name='messenger'),
    path('chat/<uuid>/', ChatView.as_view(), name='chat'),
    path('chat/load/messages/<uuid>', views.chat_load_messages, name='load_chat_messages')
]
