from django.urls import path
from .views import UserPageView, PostDetailView, NewsView, BookmarksView
from . import views


urlpatterns = [
    path('', NewsView.as_view(), name='news_page'),
    path('u/<str:username>', UserPageView.as_view(), name='user_page'),
    path('p/<uuid:uuid>', PostDetailView.as_view(), name='post_detail_view'),
    path('posts/create', views.create_new_post, name='create_new_post'),
    path('posts/likes', views.post_likes, name='post_likes'),
    path('comment/create/<int:pk>', views.create_comment, name='create_comment'),
    path('user/upload/avatar', views.user_upload_avatar, name='user_upload_avatar'),
    path('bookmarks', BookmarksView.as_view(), name='bookmarks_view'),
    path('bookmarks/<pk>/action', views.bookmarks_add_remove, name='bookmarks_add_remove'),
]
