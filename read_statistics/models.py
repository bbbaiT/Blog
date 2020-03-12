from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.


class ReadNumSum(models.Model):
    '''
    总的阅读数量，一个阅读数量对应一篇博文
    '''
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-object_id']
        verbose_name = '总阅读数量'
        verbose_name_plural = '总阅读数量'


class ReadNumDay(models.Model):
    '''
    每天的每个博文的阅读数量
    '''
    read_date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-read_date', '-read_num']
        verbose_name = '每天阅读数量'
        verbose_name_plural = '每天阅读数量'
