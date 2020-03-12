# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from likes.models import LikeSum, LikeEveryOne

register = template.Library()


@register.simple_tag
def like_num(obj):
    '''
    获取点赞总数
    :param obj:
    :return:
    '''
    content_type = ContentType.objects.get_for_model(obj)
    like_obj, create = LikeSum.objects.get_or_create(content_type=content_type, object_id=obj.id)
    return like_obj.like_num


@register.simple_tag(takes_context=True)
def get_init_active(context, obj):
    '''
    初始化用户点赞状态
    :param context:
    :param obj:
    :return:
    '''
    user = context['user']
    if not user.is_authenticated:
        return ''
    content_type = ContentType.objects.get_for_model(obj)
    if not LikeEveryOne.objects.filter(content_type=content_type, object_id=obj.id, user=user).exists():
        return ''
    return 'active'


@register.simple_tag
def get_content_type(obj):
    '''
    获得当前点赞对象的类型
    :param obj:
    :return:
    '''
    return ContentType.objects.get_for_model(obj).model
