from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class LikeSum(models.Model):
    '''
    每篇博文点赞的总数量
    '''
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    like_num = models.IntegerField(default=0)

    def __str__(self):
        return self.like_num

    class Meta:
        ordering = ['-like_num']
        verbose_name = '点赞数量'
        verbose_name_plural = '点赞数量'


class LikeEveryOne(models.Model):
    '''
    记录每个人对那篇博文点赞过
    用于判断他是要点赞还是要取消点赞
    '''
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content_object

    class Meta:
        verbose_name = '用户点赞记录'
        verbose_name_plural = '用户点赞记录'
