# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import Blog, BlogType

# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'blog_type', 'read_num', 'create_time', 'last_update_time']


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name']

