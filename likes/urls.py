# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.urls import path
from likes.views import LikeUpdate


urlpatterns = [
    path('update/', LikeUpdate.as_view(), name='update_like_num'),
]
