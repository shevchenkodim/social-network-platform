from django.shortcuts import render
from django.views.generic import TemplateView


class SignIn(TemplateView):
    """Sign in"""
    template_name = "sign_in.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SignUp(TemplateView):
    """Sign up"""
    template_name = "sign_up.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
