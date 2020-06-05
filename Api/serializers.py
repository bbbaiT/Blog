# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog
from likes.models import LikeSum
from comment.models import Comment
from Api.untils import to_time_stamp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class BlogSerializers(serializers.ModelSerializer):

    blog_type = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    last_update_time = serializers.SerializerMethodField()
    like_num = serializers.SerializerMethodField()
    comment_num = serializers.SerializerMethodField()

    def get_blog_type(self, obj):
        return obj.blog_type.type_name

    def get_create_time(self, obj):
        return to_time_stamp(obj.create_time)

    def get_last_update_time(self, obj):
        return to_time_stamp(obj.last_update_time)

    def get_like_num(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        like_obj, created = LikeSum.objects.get_or_create(content_type=content_type, object_id=obj.id)
        return like_obj.like_num

    def get_comment_num(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Comment.objects.filter(content_type=content_type, object_id=obj.id).count()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'read_num', 'blog_type', 'like_num', 'comment_num', 'create_time', 'last_update_time']
        read_only_fields = ["id", "create_time", "last_update_time"]


class BlogAddSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content']



