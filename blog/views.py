# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404

from Environmental_Public.environmental import PAGINATOR_PAGE
from blog.models import Blog, BlogType
from read_statistics.utils import UpdateReadNumMixin


# Create your views here.

def get_page_list(request, blogs_obj):
    '''
    分页处理(始终显示10页，参考谷歌、百度的分页)
    :param request: request请求
    :param blogs_obj:  要分页的对象
    :return:page_obj：当前页的对象
            page_list：页码列表
    '''
    paginator = Paginator(blogs_obj, PAGINATOR_PAGE)
    page_num = request.GET.get('page', 1)     # 获取页码
    page_obj = paginator.get_page(page_num)  # 获取指定页码的对象

    now_page = page_obj.number     # 当期页码
    if now_page < 7:
        start_page = 1
        if paginator.num_pages > 10:
            end_page = 10
        else:
            end_page = paginator.num_pages
    elif now_page > paginator.num_pages - 4:
        start_page = paginator.num_pages - 9
        end_page = paginator.num_pages
    else:
        start_page = now_page - 5
        end_page = now_page + 4
    page_list = range(start_page, end_page+1)
    return page_obj, page_list


class GetPageListMixin:
    def get_page_list(self, page_obj, paginator):
        '''
        自定义显示的分页页码数
        :param page_obj:分页之后的当前一页的对象，用于获取当前一页页码
        :param paginator:分页器，用于获取页码总数
        :return:
        '''
        now_page = page_obj.number     # 当期页码
        if now_page < 7:
            start_page = 1
            if paginator.num_pages > 10:
                end_page = 10
            else:
                end_page = paginator.num_pages
        elif now_page > paginator.num_pages - 4:
            start_page = paginator.num_pages - 9
            end_page = paginator.num_pages
        else:
            start_page = now_page - 5
            end_page = now_page + 4
        page_list = range(start_page, end_page+1)
        return page_list


class GetTypeMixin:
    def get_blog_types(self, model):
        '''
        获取博客所有类型并统计每个类型的数量(使用annotate实现)
        :return:
        '''
        return model.objects.annotate(type_count=Count('blog'))       # 使用外键关联到Blog模型


class GetDateMixin:
    def get_blog_dates(self, model):
        '''
        获取日期分类并获取每年对应的博文数量
        :param
        :return: blog_dates:所有年日期的列表
        '''
        blog_dates_dict = {}
        blog_dates = model.objects.dates('create_time', 'year', order='DESC')
        for blog_date in blog_dates:
            blog_dates_dict[blog_date] = model.objects.filter(create_time__year=blog_date.year).count()
        return blog_dates_dict


class BlogList(ListView, GetPageListMixin, GetDateMixin, GetTypeMixin):
    '''
    返回博客列表页的处理方法
    :param request:
    :return:
    '''
    model = Blog
    template_name = 'blog_list.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogList, self).get_context_data()
        context['page_list'] = self.get_page_list(context['page_obj'], context['paginator'])
        context['counts'] = self.get_queryset().count()
        context['blog_types'] = self.get_blog_types(BlogType)
        context['blog_dates'] = self.get_blog_dates(self.model)
        return context


class BlogTypeList(BlogList):
    '''
    处理博文类型
    :param blog_type_id:类型id
    :return:
    '''
    template_name = 'blog_type.html'

    def get_queryset(self):
        self.blog_type_id = self.kwargs.get('blog_type_id')        # 在url后拼接传递进来的参数
        return self.model.objects.filter(blog_type_id=self.blog_type_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogTypeList, self).get_context_data()
        context['blog_type'] = get_object_or_404(BlogType, id=self.blog_type_id)    # 当前类型
        return context


class BlogDateList(BlogList):
    '''
    日期分类
    :param request:
    :param date: 年份
    :return:
    '''
    template_name = 'blog_date.html'

    def get_queryset(self):
        self.date = self.kwargs.get('date')
        return self.model.objects.filter(create_time__year=self.date)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogDateList, self).get_context_data()
        context['blog_date'] = self.date
        return context


class BlogDetails(DetailView, UpdateReadNumMixin):
    '''
    处理博文详情
    :param blog_id:博文id
    :return:
    '''
    model = Blog
    template_name = 'blog_details.html'
    pk_url_kwarg = 'blog_id'

    def get(self, request, *args, **kwargs):
        self.update_read_num(self.get_object())      # 更新阅读数量
        return super(BlogDetails, self).get(request)

    def get_context_data(self, **kwargs):
        blog_id = self.kwargs.get(self.pk_url_kwarg)
        context = super(BlogDetails, self).get_context_data()
        context['prev_blog'] = self.model.objects.filter(id__gt=blog_id).last()     # 上一篇（倒序排序：大于当前id的最后一条）
        context['next_blog'] = self.model.objects.filter(id__lt=blog_id).first()    # 下一篇（倒序排序：小于当前id的第一条）
        return context


