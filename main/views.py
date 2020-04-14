from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from signup.models import UserProfile
from django.http import JsonResponse
from .services import image_processing
from django.conf import settings
from .models import *
import uuid
import os
User = get_user_model()


class NewsView(TemplateView):
    """News user page"""
    template_name = "news_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = UserProfile.objects.get(user=self.request.user)
        news_posts = PostsModel.objects.filter(user__in=profile.folowing.all()).order_by('-date_time_create')
        files_list = PostFilesModel.objects.filter(post__in=news_posts)
        count_files_in_post = {}
        for post in news_posts:
            files_count = files_list.filter(post=post).count()
            count_files_in_post[post.id] = files_count
        context['count_files_in_post'] = count_files_in_post
        context['news_posts'] = news_posts
        context['files_list'] = files_list
        return context


def create_new_post(request):
    """Create new user post"""
    ALLOWED_TYPES_IMAGE = ['jpg', 'jpeg', 'png']
    ALLOWED_TYPES_VIDEO = ['mp4', 'avi']
    if request.method == 'POST':
        text = request.POST.get('text', '')
        files_list = request.FILES.getlist('file')

        if text == '' and len(files_list) == 0:
            response_data = {'_code' : 1, '_status' : 'no' }
            return JsonResponse(response_data)

        if len(files_list) == 0:
            new_post = PostsModel.objects.create(user=request.user, text=text)
            response_data = {'_code' : 0, '_status' : 'ok' }
            return JsonResponse(response_data)
        else:
            new_post = PostsModel.objects.create(user=request.user, text=text)
            position = 1
            for file in request.FILES.getlist('file'):
                if position > 5:
                    break
                extension = os.path.splitext(file.name)[1][1:].lower()
                if extension in ALLOWED_TYPES_IMAGE:
                    new_post_file = PostFilesModel.objects.create(post=new_post, file=file, type='image', position=position)
                    #new_file_name = uuid.uuid4()
                    #new_image = image_processing(str(settings.MEDIA_ROOT)+ '/' + str(new_post_file.file), new_file_name)
                    #new_post_file.file = new_image
                    #new_post_file.save()

                elif extension in ALLOWED_TYPES_VIDEO:
                    PostFilesModel.objects.create(post=new_post, file=file, type='video', position=position)
                position += 1

            response_data = {'_code' : 0, '_status' : 'ok' }
            return JsonResponse(response_data)
    else:
        response_data = {'_code' : 1, '_status' : 'no' }
        return JsonResponse(response_data)


class UserPageView(TemplateView):
    """User page"""
    template_name = "user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
