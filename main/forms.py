from django import forms
from signup.models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('work', 'is_show_work', 'studied', 'is_show_studied', 'current_city', 'is_show_current_city', \
        'home_town', 'is_show_home_town', 'relationship', 'is_show_relationship', 'phone_number', 'is_show_phone_number')
