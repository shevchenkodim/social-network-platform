from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from .models import Notification


class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = "notifications.html"
    extra_context = dict()

    def get(self, request):
        object_list = Notification.objects.filter(user_to=self.request.user).order_by('status', '-date')
        paginator = Paginator(object_list, 15)

        page = request.GET.get('page', 1)
        queryset = paginator.page(page)
        self.extra_context['list_notifications'] = queryset

        return super(NotificationsView, self).get(request)
