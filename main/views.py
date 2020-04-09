from django.shortcuts import render
from django.views.generic import TemplateView


class NewsView(TemplateView):
    """News user page"""
    template_name = "news_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserPageView(TemplateView):
    """User page"""
    template_name = "user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
