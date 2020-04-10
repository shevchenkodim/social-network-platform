from django.contrib import admin
from .models import *


@admin.register(HashtagModel)
class HashtagModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(PostsModel)
class PostsModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'date_time_create', 'likes_count', 'comments_count')

    PostFilesModel

@admin.register(PostFilesModel)
class PostFilesModelAdmin(admin.ModelAdmin):
    list_display = ('post', 'file', 'type')
