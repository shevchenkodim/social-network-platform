from django.shortcuts import render
from django.views.generic import TemplateView
from .models import UserChat, UserMessages, UsersInChat
from django.http import HttpResponse

# Create your views here.


class MessengerView(TemplateView):
    """Messenger page View"""
    template_name = "messenger.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        user_in_chat = UsersInChat.objects.filter(user=self.request.user).values_list('chat_id_id', flat=True)
        chats = UserChat.objects.filter(id__in=user_in_chat)
        context['chats'] = chats
        return context


class ChatView(TemplateView):
    """Chat page View"""
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        user_in_chat = UsersInChat.objects.filter(user=self.request.user).values_list('chat_id_id', flat=True)
        chats = UserChat.objects.filter(id__in=user_in_chat)
        chat = UserChat.objects.get(chat_id=self.kwargs['uuid'])
        messages = UserMessages.objects.filter(chat_id=chat).reverse()[::-1][:20][::-1]
        context['messages'] = messages
        context['chat_page'] = chat
        context['chats'] = chats

        return context


def chat_load_messages(request, uuid):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            raise PermissionDenied
        page = request.GET.get('page')
        page = int(page)
        if page in [0, 1, None]:
            return HttpResponse('')
        start = page - 1
        user_in_chat = UsersInChat.objects.filter(user=request.user).values_list('chat_id_id', flat=True)
        chats = UserChat.objects.filter(id__in=user_in_chat)
        chat = UserChat.objects.get(chat_id=uuid)
        messages = UserMessages.objects.filter(chat_id=chat).reverse()[::-1][start*20:page*20][::-1]
        if not messages:
            return HttpResponse('')
        return render(request, 'load_chat_messages.html', {'messages': messages})
    else:
        return HttpResponse('')
