from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from . forms import UserRegisterForm, UserLoginForm
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout
from django.contrib import messages
from . models import UserProfile


class SignIn(TemplateView):
    """Sign in"""
    template_name = 'sign_in.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = UserLoginForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form_aut = UserLoginForm(data=request.POST)
            if form_aut.is_valid():
                username = form_aut.cleaned_data.get('username')
                password = form_aut.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect(reverse('news_page'))
            else:
                messages.error(request, _('Error! Please check your details or try again later!'))
                return redirect(reverse('signup:sign_in_login'))


class SignUp(TemplateView):
    """Sign up"""
    template_name = 'sign_up.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = UserRegisterForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form_aut = UserRegisterForm(data=request.POST)
            if form_aut.is_valid():
                form_aut.save()
                username = form_aut.cleaned_data.get('username')
                password = form_aut.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                UserProfile.objects.create(user=user)
                login(request, user)
                return redirect(reverse('news_page'))
            else:
                messages.error(request, _('Error! Please check your details or try again later!'))
                return redirect(reverse('signup:sign_up_register'))


def user_logout(request):
    logout(request)
    return redirect(reverse('news_page'))
