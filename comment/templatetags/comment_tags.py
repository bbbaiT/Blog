# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForms

register = template.Library()


@register.simple_tag
def comment_list(obj):
    '''
    获取传入的没篇博文的评论
    :param obj:
    :return:
    '''
    content_type = ContentType.objects.get_for_model(obj)
    # 使用parent=None来筛选一级评论， 在这里使用排序是为了让一级评论时间倒序(后评论的在前)，而回复则是按时间正序进行排序(先回复的在前)
    comment_query_set = Comment.objects.filter(content_type=content_type, object_id=obj.id, parent=None)
    return comment_query_set.order_by('-comment_time')


@register.simple_tag
def comment_count(obj):
    '''
    获取传入的一篇博文的评论数量
    :param obj:
    :return:
    '''
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.id).count()


@register.simple_tag()
def comment_form(obj):
    '''
    评论框的form表单
    :param obj:
    :return:
    '''
    content_type = ContentType.objects.get_for_model(obj)
    # content_type.model:获取评论类型的名称
    comment_form = CommentForms(initial={'object_id': obj.id, 'content_type': content_type.model, 'replay_id': 0})
    return comment_form
