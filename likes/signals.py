# -*- coding: utf-8 -*-
'''
实现点赞提醒通知
'''
from django.dispatch import receiver        # 监听信号
from django.db.models.signals import post_save  # 发生保存信号触发(监听保存信号)
from notifications.signals import notify        # 发送消息通知
from django.utils.html import strip_tags        # 将html转为字符
from likes.models import LikeEveryOne


@receiver(post_save, sender=LikeEveryOne)
def send_notification(sender, instance, **kwargs):
    '''
    监听保存信号，并发送站内消息
    :param sender: 发送者，谁发送的这条消息
    :param instance:模型实例
    :param kwargs:
    :return:
    '''
    if instance.content_type.model == 'blog':
        blog_title = instance.content_object.title
        verb = '{}点赞了你的博客：<{}>'.format(instance.user.nickname_or_username, blog_title)
        url = instance.content_object.get_url()
    elif instance.content_type.model == 'comment':
        comment_text = instance.content_object.text
        verb = '{}点赞了你的评论："{}"'.format(instance.user.nickname_or_username, strip_tags(comment_text))
        url = instance.content_object.content_object.get_url()
    # 通知
    recipient = instance.content_object.user
    notify.send(instance.user, recipient=recipient, verb=verb, url=url)
