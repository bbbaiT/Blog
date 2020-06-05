# -*- coding: utf-8 -*-
from django.urls import path
from Api.views import UserLoginWeb, BlogListView, BlogDetailView, BlogAddView, BlogTypeView, BlogDateView, BlogSearchView


urlpatterns = [
    path('user/login', UserLoginWeb.as_view()),
    path('blog/', BlogListView.as_view()),                  # 文章列表
    path('blog/<int:id>', BlogDetailView.as_view()),        # 文章详情
    path('blog/type/<int:id>', BlogTypeView.as_view()),     # 分类查询
    path('blog/date/<int:year>', BlogDateView.as_view()),   # 年份查询
    path('blog/', BlogAddView.as_view()),

    path('blog/search', BlogSearchView.as_view()),
]
