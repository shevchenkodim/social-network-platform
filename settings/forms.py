from django import forms
from signup.models import UserProfile


class UserProfileForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #         super(UserProfileForm, self).__init__(*args, **kwargs)
    #         for field_name, field in self.fields.items():
    #             field.widget.attrs['class'] = 'form-control'
    #             field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = UserProfile
        fields = ('work', 'is_show_work', 'studied', 'is_show_studied', 'current_city', 'is_show_current_city', \
        'home_town', 'is_show_home_town', 'relationship', 'is_show_relationship', 'phone_number', 'is_show_phone_number')

    # def as_smarty(self):
    #     return self._html_output(
    #         normal_row = '<div class="form-label-group mb-3"> %(errors)s %(field)s %(label)s %(help_text)s </div>',
    #         error_row = '<div class="alert-danger" role="alert">%s</div>',
    #         row_ender = '</div>',
    #         help_text_html = '',
    #         errors_on_separate_row = True)
