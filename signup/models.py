from django.db import models
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()


class UserProfile(models.Model):
    """User profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work = models.CharField('Work', max_length=100)
    studied = models.CharField('Studied', max_length=100)
    current_city = models.CharField('Current City', max_length=100)
    home_town = models.CharField('Home Town', max_length=100)
    relationship = models.CharField('Relationship', max_length=100)
    image = models.ImageField('Image user', upload_to='profile/', blank=True)
    folowers = models.ManyToManyField(User, verbose_name='folower', related_name='folowers', blank=True)
    folowing = models.ManyToManyField(User, verbose_name='folow', related_name='folows', blank=True)
    phone_number = models.CharField('Phone number', max_length=20)
    is_verified_phone = models.BooleanField('Verified phone number', default=False)
    verification_uuid = models.UUIDField('Unique Verification email UUID', default=uuid.uuid4)
    is_verified_email = models.BooleanField('Verified email', default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User_Profile'
        verbose_name_plural = 'User_Profiles'
