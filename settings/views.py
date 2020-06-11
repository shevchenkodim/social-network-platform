from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from .forms import UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from signup.forms import UserForm
from signup.models import UserProfile
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate
from django.utils.translation import get_language
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


class SettingsGeneralView(TemplateView):
    """Settings general page View"""
    template_name = "settings_general.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        context['form'] = UserProfileForm(
            instance=UserProfile.objects.get(user=self.request.user))
        context['menu_action'] = 'settings'
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form_aut = UserProfileForm(
                data=request.POST, instance=UserProfile.objects.get(user=self.request.user))
            if form_aut.is_valid():
                form_aut.save()
                messages.success(request, _(
                    'Your information has been successfully updated!'))
                return redirect(reverse('settings:settings_general_view'))
            else:
                messages.error(request, _('Error! Please try again later!'))
                return redirect(reverse('settings:settings_general_view'))
        else:
            response_data = {'_code': 1, '_status': 'no'}
            return JsonResponse(response_data)


class SettingsLanguageView(TemplateView):
    """Settings language of the region"""
    template_name = "settings_language.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        context['language_code'] = get_language()
        context['menu_action'] = 'settings'
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            language = request.POST.get('language')
            if language == 'English':
                activate('en')
            elif language == 'Русский':
                activate('ru')
            elif language == 'Український':
                activate('ua')
            else:
                activate('en')

            messages.success(request, _(
                'Your language successfully updated!'))
            return redirect(reverse('settings:settings_language_view'))
        else:
            messages.error(request, _('Error! Please try again later!'))
            return redirect(reverse('settings:settings_language_view'))


class SettingsSecurityView(TemplateView):
    """Settings security"""
    template_name = "settings_security.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        context['user_form'] = UserForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(User, id=request.user.id)
        if request.method == 'POST':
            form = UserForm(request.POST or None, instance=instance)
            if form.is_valid():
                instance.username = form.cleaned_data.get('username')
                instance.first_name = form.cleaned_data.get('first_name')
                instance.last_name = form.cleaned_data.get('last_name')
                instance.email = form.cleaned_data.get('email')
                instance.save()

                logout(request)
                login(request, instance,
                      backend='django.contrib.auth.backends.ModelBackend')

                return redirect(reverse('settings:settings_security_view'))
            else:
                messages.error(request, form.errors)
                return redirect(reverse('settings:settings_security_view'))
        else:
            form = UserForm(request.POST or None, instance=instance)
        return render(request, 'settings_security.html', {'user_form': form})
