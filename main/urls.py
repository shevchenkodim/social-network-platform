from django.urls import path
from .views import *


urlpatterns = [
    path('', NewsView.as_view(), name='news_page'),
    path('u/<str:username>', UserPageView.as_view(), name='user_page'),
]
