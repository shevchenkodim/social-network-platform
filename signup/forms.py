from django import forms
from . models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
User = get_user_model()

class RegisterForm(UserCreationForm):
    password1  = forms.CharField(max_length=64, required=True)
    password2  = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',)


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
