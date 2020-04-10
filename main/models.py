from django.db import models
from django.contrib.auth import get_user_model
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    text = models.TextField('Text posts', blank=True, max_length=2000)
    date_time_create = models.DateTimeField('Date and time created post', auto_now_add=True)
    hashtag = models.ManyToManyField(HashtagModel, verbose_name='hashtag', related_name='hashtags')
    likes_count = models.IntegerField('Likes count', default=0)
    comments_count = models.IntegerField('Comments count', default=0)

    def __str__(self):
        return self.user.username, self.text

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class PostFilesModel(models.Model):
    """Post files models"""
    post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, verbose_name='post')
    file = models.FileField('File', max_length=255, upload_to='posts/image/'+ str(User.id) + '/')
    type = models.CharField('Type file', max_length=100)

    def __str__(self):
        return self.file, self.type

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
