from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from PIL import Image, ImageDraw, ImageFilter
from django.core.exceptions import PermissionDenied
from signup.models import UserProfile
from django.http import JsonResponse
from django.conf import settings
from django.db.models import F
from .forms import UserProfileForm
from django.contrib import messages
from .models import Bookmarks, HashtagModel, PostsModel, PostFilesModel, CommentModel,\
LikesModel
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

    def post(self, request, *args, **kwargs):
        pass


class SettingsGeneralView(TemplateView):
    """Settings general page View"""
    template_name = "settings_general.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        context['form'] = UserProfileForm(instance=UserProfile.objects.get(user=self.request.user))
        context['menu_action'] = 'settings'
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form_aut = UserProfileForm(data=request.POST, instance=UserProfile.objects.get(user=self.request.user))
            if form_aut.is_valid():
                form_aut.save()
                messages.success(request, 'Your information has been successfully updated!')
                return redirect(reverse('settings_general_view'))
            else:
                messages.error(request, 'Error! Please try again later!')
                return redirect(reverse('settings_general_view'))
        else:
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
    ALLOWED_TYPES_IMAGE = ['jpg', 'jpeg']
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
                    PostFilesModel.objects.create(post=new_post, file=file, type='video', position=position)
                if extension in ALLOWED_TYPES_IMAGE:
                    new_post_file = PostFilesModel.objects.create(post=new_post, file=file, type='image', position=position)

                    img = Image.new('RGB', (1080, 1080), 'black')
                    img_to = Image.open(file)
                    (width, height) = img_to.size

                    if width > height:
                        new_width  = 1080
                        new_height = int(new_width * height / width)
                        img_to = img_to.resize((new_width, new_height), Image.ANTIALIAS)
                        (width, height) = img_to.size
                        new_height = int((1080 - height)/2)
                        img.paste(img_to, (0, new_height))

                        #top
                        (left, upper, right, lower) = (0, new_height, new_width, new_height*2)
                        im_crop = img.crop((left, upper, right, lower))
                        blurred_image = im_crop.filter(ImageFilter.GaussianBlur(10))
                        img.paste(blurred_image, (0, 0))

                        #botton
                        (left, upper, right, lower) = (0, 1080-new_height*2, new_width, 1080-new_height)
                        im_crop = img.crop((left, upper, right, lower))
                        blurred_image = im_crop.filter(ImageFilter.GaussianBlur(10))
                        img.paste(blurred_image, (0, 1080-new_height))
                        img.save(settings.MEDIA_ROOT + '/' + new_post_file.file.name)
                        new_post_file.file = str(settings.MEDIA_ROOT + '/' + new_post_file.file.name)
                        new_post_file.save()
                    else:
                        new_height = 1080
                        new_width = int(new_height * width / height)
                        img_to = img_to.resize((new_width, new_height), Image.ANTIALIAS)
                        (width, height) = img_to.size
                        new_width = int((1080 - width)/2)
                        img.paste(img_to, (new_width, 0))

                        #left
                        (left, upper, right, lower) = (new_width, 0, new_width*2, 1080)
                        im_crop = img.crop((left, upper, right, lower))
                        blurred_image = im_crop.filter(ImageFilter.GaussianBlur(10))
                        img.paste(blurred_image, (0, 0))

                        #right
                        (left, upper, right, lower) = (1080-new_width*2, 0, 1080-new_width, 1080)
                        im_crop = img.crop((left, upper, right, lower))
                        blurred_image = im_crop.filter(ImageFilter.GaussianBlur(10))
                        img.paste(blurred_image, (1080-new_width, 0))
                        img.save(settings.MEDIA_ROOT + '/' + new_post_file.file.name)
                        new_post_file.file = str(settings.MEDIA_ROOT + '/' + new_post_file.file.name)
                        new_post_file.save()
                position += 1

            response_data = {'_code' : 0, '_status' : 'ok' }
            return JsonResponse(response_data)
    else:
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
