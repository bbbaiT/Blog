# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Blog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'user', 'content', 'read_num', 'blog_type', 'create_time', 'last_update_time']


class BlogAddSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content']
