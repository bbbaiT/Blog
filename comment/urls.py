# -*- coding: utf-8 -*-
from django.urls import path
from comment.views import CommentSubmit


urlpatterns = [
    path('update/', CommentSubmit.as_view(), name='update_comment'),
]
