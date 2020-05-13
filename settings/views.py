from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.http import JsonResponse
from .forms import UserProfileForm
from signup.models import UserProfile
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

class SettingsGeneralView(TemplateView):
    """Settings general page View"""
    template_name = "settings_general.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        context['form'] = UserProfileForm(instance=UserProfile.objects.get(user=self.request.user))
        context['menu_action'] = 'settings'
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form_aut = UserProfileForm(data=request.POST, instance=UserProfile.objects.get(user=self.request.user))
            if form_aut.is_valid():
                form_aut.save()
                messages.success(request, 'Your information has been successfully updated!')
                return redirect(reverse('settings:settings_general_view'))
            else:
                messages.error(request, 'Error! Please try again later!')
                return redirect(reverse('settings:settings_general_view'))
        else:
            response_data = {'_code' : 1, '_status' : 'no' }
            return JsonResponse(response_data)
