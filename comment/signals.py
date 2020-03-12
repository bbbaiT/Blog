# -*- coding: utf-8 -*-
'''
实现评论提醒通知
'''
from threading import Thread
from django.dispatch import receiver        # 监听信号
from django.db.models.signals import post_save  # 发生保存信号触发(监听保存信号)
from notifications.signals import notify        # 发送消息通知
from django.utils.html import strip_tags        # 将html转为字符
from django.core.mail import send_mail
from django.template.loader import render_to_string     # 将模板内容转化为字符
from comment.models import Comment
from mysite.settings.production import EMAIL_HOST_USER


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    '''
    监听保存信号，并发送站内消息
    :param sender: 发送者，谁发送的这条消息
    :param instance: 评论
    :param kwargs:
    :return:
    '''
    if instance.replay_to is None:
        # 评论
        recipient = instance.content_object.user       # 收件人
        verb = '{} 评论了你的文章：<{}>'.format(instance.user.nickname_or_username, instance.content_object.title)
    else:
        # 回复
        recipient = instance.replay_to
        verb = '{} 回复了你的评论："{}"'.format(instance.user.nickname_or_username, strip_tags(instance.parent.text))
    # 发送站内通知
    url = instance.content_object.get_url() + '#comment_{}'.format(instance.id)    # 获取评论对象的url
    notify.send(instance.user, recipient=recipient, verb=verb, url=url)


class SendMail(Thread):
    '''
    发送邮件
    '''
    def __init__(self, subject, message, email):
        self.subject = subject
        self.message = message
        self.email = email
        super(SendMail, self).__init__()

    def run(self):
        send_mail(
            subject=self.subject,
            message='',
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.email],
            fail_silently=False,
            html_message=self.message,
        )


@receiver(post_save, sender=Comment)
def send_mail_notification(sender, instance, **kwargs):
    '''
    监听保存信号发送邮件通知
    :param self:
    :return:
    '''
    if instance.parent is None:
        subject = '有人评论你的文章了，快去回复他/她吧'
        email = instance.content_object.get_email()
    else:
        subject = '有人评论你的评论了，快去回复他/她吧'
        email = instance.replay_to.email

    if email != '':
        context = {
            'comment_text': instance.text,
            'url': instance.content_object.get_url()
        }
        message = render_to_string('send_mail.html', context)
        send_mail_thread = SendMail(subject, message, email)
        send_mail_thread.start()
