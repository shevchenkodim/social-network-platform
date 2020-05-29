from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from PIL import Image, ImageDraw, ImageFilter
from django.core.exceptions import PermissionDenied
from signup.models import UserProfile
from django.http import JsonResponse
from django.conf import settings
from django.db.models import F
from django.contrib import messages
from .models import Bookmarks, HashtagModel, PostsModel, PostFilesModel, CommentModel,\
LikesModel
from .services import processingImagesAndVideos
import threading
import uuid
import os
User = get_user_model()


class BookmarksView(TemplateView):
    """Bookmarks page View"""
    template_name = "bookmarks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        list_bookmarks = Bookmarks.objects.filter(user=self.request.user).order_by('-date_time_add').values_list('post_id', flat=True)
        posts = PostsModel.objects.filter(id__in=list_bookmarks)

        queryset = PostFilesModel.objects.none()
        for post in posts:
            queryset |= PostFilesModel.objects.filter(post_id=post.id)[:1]

        context['news_posts'] = posts
        context['files_list'] = queryset
        context['menu_action'] = 'bookmarks'
        return context


def bookmarks_add_remove(request, pk):
    """Create and delate Bookmarks posts"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied
        try:
            bookmarks = Bookmarks.objects.get(user=request.user, post_id=pk)
            bookmarks.delete()
            class_icon = 'fa fa-bookmark-o mx-2'
        except Bookmarks.DoesNotExist:
            bookmarks = Bookmarks.objects.create(user=request.user, post_id=pk)
            class_icon = 'fa fa-bookmark mx-2'
            # messages.success(request, 'Your successfully add post to Bookmarks!')

        response_data = {'_code' : 0, '_status' : 'ok', '_class_icon': class_icon }
        return JsonResponse(response_data)
    else:
        # messages.error(request, 'Error! Please try again later!')
        response_data = {'_code' : 1, '_status' : 'no' }
        return JsonResponse(response_data)


class PostDetailView(TemplateView):
    """Post Detail View"""
    template_name = "post_detail_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        post_obj = PostsModel.objects.get(page_id=self.kwargs['uuid'])
        files_list = PostFilesModel.objects.filter(post=post_obj)
        comment_list = CommentModel.objects.filter(post=post_obj)
        user_likes_post = LikesModel.objects.filter(post=post_obj, user=self.request.user, is_liked=True)
        context['bookmark_list'] = [post.post.id for post in Bookmarks.objects.filter(user=self.request.user)]
        context['count_files_in_post'] = files_list.count()
        context['user_likes_post'] = user_likes_post
        context['comment_list'] = comment_list
        context['files_list'] = files_list
        context['post_obj'] = post_obj
        return context


class NewsView(TemplateView):
    """News user page"""
    template_name = "news_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        profile = UserProfile.objects.get(user=self.request.user)
        news_posts = PostsModel.objects.filter(user__in=profile.folowing.all()).order_by('-date_time_create')
        files_list = PostFilesModel.objects.filter(post__in=news_posts)
        comment_list = CommentModel.objects.none()
        for post in news_posts:
            comment_list |= CommentModel.objects.filter(post=post.id)[:3]
        count_files_in_post = { post.id: files_list.filter(post=post.id).count() for post in news_posts}
        count_comments_in_post = { post.id: CommentModel.objects.filter(post=post.id).count() for post in news_posts}
        user_likes_posts = LikesModel.objects.filter(post__in=news_posts, user=self.request.user, is_liked=True).values_list('post_id', flat=True)
        context['bookmark_list'] = [post.post.id for post in Bookmarks.objects.filter(user=self.request.user)]
        context['user_likes_posts'] = user_likes_posts
        context['count_comments_in_post'] = count_comments_in_post
        context['count_files_in_post'] = count_files_in_post
        context['news_posts'] = news_posts
        context['files_list'] = files_list
        context['comment_list'] = comment_list
        context['menu_action'] = 'news'
        return context


def create_comment(request, pk):
    """Create new comment"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied
        text = request.POST.get('text', '')
        if text == '':
            response_data = {'_code' : 1, '_status' : 'no' }
            return JsonResponse(response_data)
        user = request.user
        post = PostsModel.objects.get(id=pk)
        comment = CommentModel.objects.create(user=user, post=post, text=text)
        response_data = {'_code' : 0, '_status' : 'ok' }
        return JsonResponse(response_data)
    else:
        response_data = {'_code' : 1, '_status' : 'no' }
        return JsonResponse(response_data)


def create_new_post(request):
    """Create new user post"""
    ALLOWED_TYPES_IMAGE = ['jpg', 'jpeg', 'png', 'gif']
    ALLOWED_TYPES_VIDEO = ['mp4', 'avi']
    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied
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
                if extension in ALLOWED_TYPES_VIDEO:
                    video = PostFilesModel.objects.create(post=new_post, file=file, type='video', position=position)
                if extension in ALLOWED_TYPES_IMAGE:
                    postFile = PostFilesModel.objects.create(post=new_post, file=file, type='image', position=position)
                position += 1

            my_thread = threading.Thread(target=processingImagesAndVideos, name=new_post.id, args=(request, new_post.id))
            my_thread.start()

            # processingImagesAndVideos(request, new_post.id)
            messages.success(request, 'Your successfully add new post! :)')
            response_data = {'_code' : 0, '_status' : 'ok' }
            return JsonResponse(response_data)
    else:
        messages.error(request, 'Error! Please try again later!')
        response_data = {'_code' : 1, '_status' : 'no' }
        return JsonResponse(response_data)


def post_likes(request):
    """Add or remove likes"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied
        pk = request.POST.get('post_id')
        try:
            post = PostsModel.objects.get(id=pk)
        except PostsModel.DoesNotExist:
            post = None
        try:
            likes = LikesModel.objects.get(user=request.user, post=post)
        except LikesModel.DoesNotExist:
            likes = None


        if likes == None:
            likes = LikesModel.objects.create(user=request.user, post=post)
            post.likes_count = F('likes_count') + 1
            post.save(update_fields=["likes_count"])
            class_likes = 'fa fa-heart mx-2'
        else:
            if likes.is_liked == True:
                likes.is_liked = False
                likes.save()
                post.likes_count = F('likes_count') - 1
                post.save(update_fields=["likes_count"])
                class_likes = 'fa fa-heart-o mx-2'
            elif likes.is_liked == False:
                likes.is_liked = True
                likes.save()
                post.likes_count = F('likes_count') + 1
                post.save(update_fields=["likes_count"])
                class_likes = 'fa fa-heart mx-2'
        post.refresh_from_db()
        response_data = {'_code' : 0, '_status' : 'ok', '_likes': post.likes_count, '_class_likes': class_likes}
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)


class UserPageView(TemplateView):
    """User page"""
    template_name = "user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        user_obj = User.objects.get(username=self.kwargs['username'])
        news_posts = PostsModel.objects.filter(user=user_obj).order_by('-date_time_create')
        queryset = PostFilesModel.objects.none()
        for post in news_posts:
            queryset |= PostFilesModel.objects.filter(post_id=post.id)[:1]
        if self.request.user == user_obj:
            context['menu_action'] = 'user_page'
        context['news_posts'] = news_posts
        context['files_list'] = queryset
        context['owner_page'] = user_obj
        return context


def user_upload_avatar(request):
    """Upload user avatar"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied
        file = request.FILES
        f = file.get('file')
        if f == None:
            response_data = {'_code' : 1, '_status' : 'no' }
            return JsonResponse(response_data)
        profile = UserProfile.objects.get(user=request.user)
        profile.image = f
        profile.save()
        response_data = {'_code' : 0, '_status' : 'ok'}
    else:
        response_data = {'_code' : 1, '_status' : 'no' }

    return JsonResponse(response_data)


def permission_denied(request):
    """Rerurn page 403"""
    data = {}
    return render(request, '403.html', data, status=403)
