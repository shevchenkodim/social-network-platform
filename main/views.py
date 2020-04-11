from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from signup.models import UserProfile
from django.http import JsonResponse
from .models import *
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
        file = request.FILES
        f = file.get('file')
        if f != None:
            extension = os.path.splitext(f.name)[1][1:].lower()
            if extension in ALLOWED_TYPES_IMAGE:
                new_post = PostsModel.objects.create(user=request.user, text=text)
                files = PostFilesModel.objects.create(post=new_post, file=f, type='image', position=1)
            elif extension in ALLOWED_TYPES_VIDEO:
                new_post = PostsModel.objects.create(user=request.user, text=text)
                files = PostFilesModel.objects.create(post=new_post, file=f, type='video', position=1)
            else:
                response_data = {'_code' : 1, '_status' : 'no' }
                #return JsonResponse(response_data)
            response_data = {'_code' : 0, '_status' : 'ok' }
            #return JsonResponse(response_data)
        else:
            new_post = PostsModel.objects.create(user=request.user, text=text)
            response_data = {'_code' : 0, '_status' : 'ok' }
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    #return JsonResponse(response_data)


class UserPageView(TemplateView):
    """User page"""
    template_name = "user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
