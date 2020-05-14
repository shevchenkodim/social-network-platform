from django.db import models
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()

# Create your models here.

class UserChat(models.Model):
    """User chat uuid id"""
    director = models.ForeignKey(User, on_delete=models.CASCADE, related_name='director')
    date_create = models.DateTimeField(auto_now_add=True)
    chat_name = models.CharField(max_length=128, blank=False, default='default_chat')
    image = models.ImageField(upload_to='chats/', blank=True)
    chat_id = models.UUIDField(default=uuid.uuid4())

    def __str__(self):
        return f'User chat {self.chat_name}, uuid = {self.chat_id}'


class UserMessages(models.Model):
    """User messages for chat"""
    chat_id = models.ForeignKey(UserChat, on_delete=models.CASCADE)
    from_id = models.ForeignKey(User, on_delete=models.CASCADE)
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
