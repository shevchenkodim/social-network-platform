from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class MessengerView(TemplateView):
    """Messenger page View"""
    template_name = "messenger.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        return context


class ChatView(TemplateView):
    """Chat page View"""
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        context['chat_id'] = self.kwargs['uuid']
        return context
