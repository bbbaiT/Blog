from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=15)

    def __str__(self):
        return '{}:{}'.format(self.nick_name, self.user)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    # 动态绑定自定义属性
    @property
    def nick_name(self):
        '''
        获取昵称，不存在返回None
        :return:
        '''
        if MyUser.objects.filter(user=self).exists():
            return MyUser.objects.get(user=self).nickname
        else:
            return None

    @nick_name.setter
    def nick_name(self, value):
        '''
        设置nickname的值
        :param value:
        :return:
        '''
        myuser, create = MyUser.objects.get_or_create(user=self)
        myuser.nickname = value
        myuser.save()

    @property
    def nickname_or_username(self):
        '''
        获取昵称， 不存在返回用户名
        :return:
        '''
        if MyUser.objects.filter(user=self).exists():
            return MyUser.objects.get(user=self).nickname
        else:
            return self.username


# 把MyUser模型的属性帮到User模型中
User.nickname = MyUser.nick_name
User.nickname_or_username = MyUser.nickname_or_username

