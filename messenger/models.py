from django.db import models
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()

# Create your models here.

class UserChat(models.Model):
    """User chat uuid id"""
    date_create = models.DateTimeField(auto_now_add=True)
    chat_id = models.UUIDField(default=uuid.uuid4())

    def __str__(self):
        return f'User chat uuid = {self.chat_id}'


class UserMessages(models.Model):
    """User messages for chat"""
    to_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_id')
    from_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_id')
    content = models.CharField(max_length=1024, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class UsersInChat(models.Model):
    """Combines a chat table and a message table"""
    chat_id = models.ForeignKey(UserChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.chat_id}, {self.user}'
