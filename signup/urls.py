from django.urls import path
from .views import *
from . import views

app_name = 'signup'
urlpatterns = [
    path('login', SignIn.as_view(), name='sign_in_login'),
    path('register', SignUp.as_view(), name='sign_up_register'),
]
