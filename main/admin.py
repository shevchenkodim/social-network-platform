from django.contrib import admin
from .models import Bookmarks, HashtagModel, PostsModel, PostFilesModel


@admin.register(HashtagModel)
class HashtagModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(PostsModel)
class PostsModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'date_time_create', 'likes_count', 'comments_count')


@admin.register(PostFilesModel)
class PostFilesModelAdmin(admin.ModelAdmin):
    list_display = ('post', 'file', 'type')


@admin.register(Bookmarks)
class BookmarksAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
