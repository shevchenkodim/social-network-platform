from django.urls import path
from .views import SettingsGeneralView
from . import views

app_name = 'settings'
urlpatterns = [
    path('general', SettingsGeneralView.as_view(), name='settings_general_view'),
]
