# -*- coding: utf-8 -*-
from django.urls import path
from Api.views import UserLoginWeb, BlogListView, BlogDetailView, BlogAddView


urlpatterns = [
    path('user/', UserLoginWeb.as_view()),
    path('blog/', BlogListView.as_view()),
    path('blog/<int:id>', BlogDetailView.as_view()),
    path('blog/add/', BlogAddView.as_view())
]
