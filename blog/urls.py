# -*- coding: utf-8 -*-
from django.urls import path
from blog.views import BlogList, BlogTypeList, BlogDateList, BlogDetails


urlpatterns = [
    path('', BlogList.as_view(), name="blog_list"),
    path('type/<int:blog_type_id>', BlogTypeList.as_view(), name='blog_type'),
    path('date/<int:date>', BlogDateList.as_view(), name='blog_date'),
    path('<int:blog_id>/', BlogDetails.as_view(), name='blog_detail'),
]
