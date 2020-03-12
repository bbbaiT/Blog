# -*- coding: utf-8 -*-
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static     # 配置 存放上传的文件的静态文件夹
from mysite.views import SearchList, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('comment/', include('comment.urls')),
    path('like/', include('likes.urls')),
    path('user/', include('user.urls')),
    path('search', SearchList.as_view(), name="search"),

    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('notify/', include('notify.urls')),

    path('api/', include('Api.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
