# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.utils import ReadNumExpand, ReadNumDay

# Create your models here.


class BlogType(models.Model):
    '''
    类型表
    '''
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '类型'
        verbose_name_plural = '类型'


class Blog(models.Model, ReadNumExpand):
    '''
    博文表
    '''
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    # 外键与 类型表 相关联，多对一模式：(采用的是一种类型对应多篇博文)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)

    # 使用contenttype的GenericRelation进行反向链接，链接到每日阅读表中
    read_day_key = GenericRelation(ReadNumDay)

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_id': self.id})

    def get_email(self):
        return self.user.email

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']
        verbose_name = '博客'
        verbose_name_plural = '博客'

