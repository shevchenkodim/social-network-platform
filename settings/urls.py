from django.urls import path
from .views import SettingsGeneralView, SettingsLanguageView
from . import views

app_name = 'settings'
urlpatterns = [
    path('general', SettingsGeneralView.as_view(), name='settings_general_view'),
    path('language', SettingsLanguageView.as_view(),
         name='settings_language_view'),
]
