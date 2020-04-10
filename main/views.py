from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from signup.models import UserProfile
from .models import *
User = get_user_model()


class NewsView(TemplateView):
    """News user page"""
    template_name = "news_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = UserProfile.objects.get(user=self.request.user)
        news_posts = PostsModel.objects.filter(user__in=profile.folowing.all()).order_by('-date_time_create')
        files_list = PostFilesModel.objects.filter(post__in=news_posts)
        context['news_posts'] = news_posts
        context['files_list'] = files_list
        return context


class UserPageView(TemplateView):
    """User page"""
    template_name = "user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
