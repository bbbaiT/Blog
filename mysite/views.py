# -*- coding: utf-8 -*-
from django.views.generic import ListView, RedirectView
from datetime import timedelta, datetime
from django.core.cache import cache
from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from blog.models import Blog
from read_statistics.utils import Get7ReadNumMixin
from blog.views import GetPageListMixin


class GetBlogMixin:
    def get_before_hot_blog(self, days):
        '''
        获取指定天(days)内最多点击博文
        :param
        :return:
        '''
        today = datetime.now().date()
        before_days = today - timedelta(days=days)
        hot_blog = Blog.objects.filter(read_day_key__read_date__gte=before_days) \
                       .values('id', 'title') \
                       .annotate(sum_num=Sum('read_day_key__read_num')) \
                       .order_by('-sum_num')[:5]
        return hot_blog


class UseCacheMixin(GetBlogMixin):
    def use_cache_get_hot_blog(self, key, days):
        '''
        使用缓存获取热门博文
        :param key:
        :param days:
        :return:
        '''
        if key is None:
            raise Exception('Cache Key is None')
        hot_blog = cache.get(key)
        if hot_blog is None:
            hot_blog = self.get_before_hot_blog(days=days)
            cache.set(key, hot_blog, 86400)
        return hot_blog


class HomeView(RedirectView, UseCacheMixin, Get7ReadNumMixin):
    '''
    首页
    '''
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        date_list, read_num_list = self.get_7_days_read_num(Blog)
        context = {
            'date_list': date_list,
            'read_num_list': read_num_list,
            'today_hot_blog': self.get_before_hot_blog(days=0),
            'week_hot_blog': self.use_cache_get_hot_blog(key='week_hot_blog', days=7),
            'month_hot_blog': self.use_cache_get_hot_blog(key='month_hot_blog', days=30),
            'year_hot_blog': self.use_cache_get_hot_blog(key='year_hot_blog', days=365),
        }
        return render(request, self.template_name, context)


class SearchList(ListView, GetPageListMixin):
    '''
    搜索
    '''
    model = Blog                        # 链接的模型名称
    template_name = 'search.html'       # 返回的模板名称
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.search = self.request.GET.get('wd', '').strip()
        refere = self.request.META.get('HTTP_REFERER') if self.request.META.get('HTTP_REFERER') is not None else '/'
        if self.search == "":
            return redirect(refere)
        return super(SearchList, self).get(request)

    def get_queryset(self):
        '''
        获取queryset集
        :return:
        '''
        search_list = self.search.split(' ')
        # 多词搜索 分词
        Q_objects = None
        for wd in search_list:
            if Q_objects:
                Q_objects = Q_objects | Q(title__icontains=wd) | Q(content__icontains=wd)
            else:
                Q_objects = Q(title__icontains=wd) | Q(content__icontains=wd)

        return self.model.objects.filter(Q_objects)

    def get_context_data(self, **kwargs):
        '''
        自定义返回前端的数据
        :param kwargs:
        :return:
        '''
        context = super(SearchList, self).get_context_data()
        context['count'] = self.get_queryset().count()
        context['search'] = self.search
        context['page_list'] = self.get_page_list(page_obj=context['page_obj'], paginator=context['paginator'])
        return context

