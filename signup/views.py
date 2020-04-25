from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from . forms import UserRegisterForm, UserLoginForm
from django.http import HttpResponse, JsonResponse


class SignIn(TemplateView):
    """Sign in"""
    template_name = "sign_in.html"

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
                return redirect('/')
            else:
                return HttpResponse('Error')


class SignUp(TemplateView):
    """Sign up"""
    template_name = "sign_up.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
