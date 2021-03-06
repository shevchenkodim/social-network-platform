from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',         admin.site.urls),

    path('',               include('main.urls')),
    path('signup/',        include('signup.urls')),
    path('settings/',      include('settings.urls')),
    path('messenger/',     include('messenger.urls')),
    path('notifications/', include('notification.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
