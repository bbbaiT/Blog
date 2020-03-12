# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNumSum, ReadNumDay


class ReadNumExpand:
    @property
    def read_num(self):
        '''
        返回每一篇博文的阅读数量
        :return:
        '''
        try:
            # 使用ContentType找到当前模型
            content_type = ContentType.objects.get_for_model(self)
            object_id = self.id
            # 在这里找到对应的模型中的那条博文
            read_num = ReadNumSum.objects.get(content_type=content_type, object_id=object_id)
            return read_num.read_num
        except ObjectDoesNotExist:
            return 0


class UpdateReadNumMixin:
    def update_read_num(self, obj):
        '''
        找到对应博文的阅读数量并做自增操作
        :param content_type_obj: 外键链接的模型
        :param object_id_obj:   模型中的具体哪一个对象
        :return:
        '''
        content_type = ContentType.objects.get_for_model(obj)
        object_id = obj.id

        # 检测是否有对应那条博文的总阅读数量并+1操作
        blog_read_num_sum, created_sum = ReadNumSum.objects.get_or_create(content_type=content_type, object_id=object_id)
        blog_read_num_sum.read_num += 1
        blog_read_num_sum.save()
        # 检测是否有对应那条博文的每天的阅读记录并+1操作
        blog_read_num_day, created_day = ReadNumDay.objects.get_or_create(content_type=content_type, object_id=object_id, read_date=datetime.now().date())
        blog_read_num_day.read_num += 1
        blog_read_num_day.save()


class Get7ReadNumMixin:
    def get_7_days_read_num(self, content_type_obj):
        '''
        统计前7天每天的总的阅读数量
        :param content_type_obj: 找那个模型对象的阅读数量
        :return: date_7_days_list：前7天日期列表
                 read_nums_7_days_list：前7天对应的阅读数量
        '''
        content_type = ContentType.objects.get_for_model(content_type_obj)
        today = datetime.now().date()
        date_7_days_list = []
        read_nums_7_days_list = []
        for day in range(7, -1, -1):
            date_day = today - timedelta(days=day)      # 利用今天减去几天就是前几天(利用了datetime模块的timedelta类)
            read_nums_list = ReadNumDay.objects.filter(content_type=content_type, read_date=date_day)   # 找到对应模型的那一天的所有的阅读数量
            read_nums = read_nums_list.aggregate(read_sums=Sum('read_num'))  # 统计那一天的所有阅读数量的总数
            date_7_days_list.append(date_day.strftime('%m-%d'))
            read_nums_7_days_list.append(read_nums['read_sums'] or 0)
        return date_7_days_list, read_nums_7_days_list
