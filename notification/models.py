from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    status_choices = (
        ('new', 'new'),
        ('readed', 'readed'),
    )
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User to',
                                related_name='user_dest')
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name='User from', related_name='user_from')
    message = models.CharField(max_length=1024, verbose_name='Message')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=status_choices, default=status_choices[0][0],
                              verbose_name='Status')

    def __str__(self):
        return self.message
