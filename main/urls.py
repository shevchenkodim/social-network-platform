from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', NewsView.as_view(), name='news_page'),
    path('u/<str:username>', UserPageView.as_view(), name='user_page'),
    path('posts/create', views.create_new_post, name='create_new_post'),
]
