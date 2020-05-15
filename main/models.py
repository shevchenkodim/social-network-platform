from django.db import models
from django.contrib.auth import get_user_model
import uuid
import os
from django.conf import settings
from django.utils.translation import gettext_lazy as _
User = get_user_model()


class HashtagModel(models.Model):
    """Hashtag post model"""
    name = models.CharField('Name hashtag', max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hashtag'
        verbose_name_plural = 'Hashtags'


class PostsModel(models.Model):
    """Posts user model"""
    page_id = models.UUIDField(default=uuid.uuid4, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    text = models.TextField(_('Text posts'), blank=True, max_length=2000)
    date_time_create = models.DateTimeField(_('Date and time created post'), auto_now_add=True)
    hashtag = models.ManyToManyField(HashtagModel, blank=True, verbose_name=_('hashtag'), related_name='hashtags')
    likes_count = models.IntegerField(_('Likes count'), default=0)
    comments_count = models.IntegerField(_('Comments count'), default=0)

    def __str__(self):
        return f'{self.user.username} - {self.text}'

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class PostFilesModel(models.Model):
    """Post files models"""
    post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, verbose_name=_('post'))
    file = models.FileField(_('File'), max_length=255, upload_to='posts/image/')
    type = models.CharField(_('Type file'), max_length=100)
    position = models.IntegerField(_('Position in post'), default=0)
    video_gif = models.ImageField(_('video_gif'), upload_to='posts/gif/', blank=True, null=True)

    def __str__(self):
        return f'{self.file} - {self.type}'

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')


class CommentModel(models.Model):
    """Comment models"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, verbose_name=_('post'))
    text = models.CharField(_('Text'), max_length=300)
    date_time_add = models.DateTimeField(_('Date and time created comment'), auto_now_add=True)
    likes_count = models.IntegerField(_('Likes count'), default=0)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.post.text} - {self.text}'

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class LikesModel(models.Model):
    """Post likes model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostsModel, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=True)


class Bookmarks(models.Model):
    """User saved posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostsModel, on_delete=models.CASCADE)
    date_time_add = models.DateTimeField(_('Date and time add'), auto_now_add=True)
