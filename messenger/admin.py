from django.contrib import admin
from .models import UserChat, UserMessages, UsersInChat

# Register your models here.

@admin.register(UserChat)
class UserChatAdmin(admin.ModelAdmin):
    list_display = ('date_create', 'chat_id')


@admin.register(UserMessages)
class UserMessagesAdmin(admin.ModelAdmin):
    list_display = ('from_id', 'content', 'created_at')


@admin.register(UsersInChat)
class UsersInChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user')
