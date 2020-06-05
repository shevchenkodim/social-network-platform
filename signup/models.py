from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid
User = get_user_model()


class UserProfile(models.Model):
    """User profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work = models.CharField(_('Work'), max_length=100, blank=True)
    is_show_work = models.BooleanField(
        _('Show info work in user page any user'), default=True)
    studied = models.CharField(_('Studied'), max_length=100, blank=True)
    is_show_studied = models.BooleanField(
        _('Show info studied in user page any user'), default=True)
    current_city = models.CharField(
        _('Current City'), max_length=100, blank=True)
    is_show_current_city = models.BooleanField(
        _('Show info current city in user page any user'), default=True)
    home_town = models.CharField(_('Home Town'), max_length=100, blank=True)
    is_show_home_town = models.BooleanField(
        _('Show info home town in user page any user'), default=True)
    relationship = models.CharField(
        _('Relationship'), max_length=100, blank=True)
    is_show_relationship = models.BooleanField(
        _('Show info relationship in user page any user'), default=True)
    image = models.ImageField(
        _('Image user'), upload_to='profile/', blank=True)
    folowers = models.ManyToManyField(
        User, verbose_name='folower', related_name='folowers', blank=True)
    folowing = models.ManyToManyField(
        User, verbose_name='folow', related_name='folows', blank=True)
    phone_number = models.CharField(
        _('Phone number'), max_length=20, blank=True)
    is_show_phone_number = models.BooleanField(
        _('Show info phone number in user page any user'), default=True)
    is_verified_phone = models.BooleanField(
        _('Verified phone number'), default=False)
    verification_uuid = models.UUIDField(
        _('Unique Verification email UUID'), default=uuid.uuid4)
    is_verified_email = models.BooleanField(_('Verified email'), default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('User_Profile')
        verbose_name_plural = _('User_Profiles')
