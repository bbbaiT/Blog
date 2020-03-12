# -*- coding: utf-8 -*-
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from notifications.signals import notify


@receiver(post_save, sender=User)
def register_send_message(sender, instance, **kwargs):
    if kwargs['created']:       # 用户注册携带进来的属性
        url = reverse('home')
        notify.send(instance, recipient=instance, verb='欢迎加入，一起努力。', url=url)
