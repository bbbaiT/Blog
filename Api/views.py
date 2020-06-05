import datetime
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from Api.serializers import UserSerializer, BlogSerializers, BlogAddSerializers
from blog.models import Blog, BlogType
from django.utils import timezone

# Create your views here.


class MyPageNumberPagination(PageNumberPagination):
    '''
    自定义分页，
    '''
    page_size = 10      # 每页显示的数量
    page_size_query_param = 's'      # 默认每页显示10个，可以通过传入pager1/?p=2&size=4,改变默认每页显示的个数
    page_query_param = 'p'          # get请求页码时的参数
    max_page_size = 10      # 每页最大显示条数
    last_page_strings = ('last',)        # 最后一页的别名, 默认为('last',)，建议改为()

    def get_paginated_response(self, data, date_list=[], type_list=[]):
        return JsonResponse(
            {
                'code': 200,
                'count': self.page.paginator.count,     # 所有对象的总数量
                'page_size': self.page_size,            # 每一页显示的数量
                'page_nums': self.page.paginator.num_pages,  # 页码总页数
                'next': self.get_next_link(),       # 下一页的链接
                'previous': self.get_previous_link(),   # 上一页的链接
                'data': data,   # 返回的数据列表
                'date': date_list,
                'type': type_list,
            }
        )


class MixGetBlogTypeNum:
    def get_blog_type_num(self, model):
        blog_type_list = []
        types = BlogType.objects.all()
        for blog_type in types:
            blog_type_list.append({
                'id': blog_type.id,
                'type_name': blog_type.type_name,
                'num': model.objects.filter(blog_type_id=blog_type.id).count()
            })
        return blog_type_list


class MixGetBlogDateNum:
    def get_blog_date_num(self, model):
        blog_dates_list = []
        blog_dates = model.objects.dates('create_time', 'year', order='DESC')
        for blog_date in blog_dates:
            blog_dates_list.append(
                {str(blog_date)[:4]: model.objects.filter(create_time__year=blog_date.year).count()})
        return blog_dates_list


class UserLoginWeb(APIView):
    '''
    登录
    '''
    serializer_class = UserSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'status': 0, 'msg': '用户名或密码错误'})
        token = self.auth_token(user)

        login(self.request, user)
        return JsonResponse({'status': 1, 'token': token.key})

    def auth_token(self, user):
        '''加密token'''
        token, create = Token.objects.get_or_create(user=user)
        # token = Token.objects.create(user=user)

        # 满足条件的话，就表示token已失效，重新一个生成一个token
        # if timezone.now() > (token.created + datetime.timedelta(hours=2)):
        #     Token.objects.filter(user=user).delete()
        # token = Token.objects.create(user=user)
        return token


class BlogListView(APIView, MixGetBlogTypeNum, MixGetBlogDateNum):
    '''博文列表'''
    model = Blog
    serializer_class = BlogSerializers
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.get_context_data(request, queryset)

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, request, queryset):
        pagination = MyPageNumberPagination()  # 分页
        pg_obj = pagination.paginate_queryset(queryset, request, view=self)  # 这个方法获取分页，并获取当前这一页的对象集
        data = self.serializer_class(instance=pg_obj, many=True).data

        return pagination.get_paginated_response(data, date_list=self.get_blog_date_num(self.model),
                                                 type_list=self.get_blog_type_num(self.model))


class BlogTypeView(BlogListView):
    def get(self, request, *args, **kwargs):
        type_id = kwargs.get('id', 1)
        query_set = self.get_queryset(type_id)
        return self.get_context_data(request, query_set)

    def get_queryset(self, type_id):
        return self.model.objects.filter(blog_type_id=type_id).all()


class BlogDateView(BlogListView):
    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        if year > datetime.datetime.now().year or year < 2019:
            return JsonResponse({'code': -1, "err": '参数错误'})

        query_set = self.get_queryset(year)
        return self.get_context_data(request, query_set)

    def get_queryset(self, year):
        return self.model.objects.filter(create_time__year=year).all()


class BlogSearchView(BlogListView):
    search_params = 'wd'

    def get(self, request, *args, **kwargs):
        self.search = request.query_params.get(self.search_params, None)

        query_set = self.get_queryset()
        return self.get_context_data(request, query_set)

    def get_queryset(self):
        if not self.search:
            return self.model.objects.all()
        search_list = self.search.split(' ')
        # 多词搜索 分词
        Q_objects = None
        for wd in search_list:
            if Q_objects:
                Q_objects = Q_objects | Q(title__icontains=wd) | Q(content__icontains=wd)
            else:
                Q_objects = Q(title__icontains=wd) | Q(content__icontains=wd)

        return self.model.objects.filter(Q_objects)


class BlogDetailView(generics.RetrieveAPIView):
    '''博文详情'''
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    lookup_field = 'id'             # 传递进来的参数
    http_method_names = ['get']     # 指定的请求方式

    def get(self, request, *args, **kwargs):
        obj = self.get_object()        # 获取指定的对象
        serializer = self.get_serializer(obj)      # 对象数据转化为Json数据
        return JsonResponse(serializer.data)




class BlogAddView(generics.CreateAPIView):
    '''添加博文，需要登录'''
    model = Blog
    serializer_class = BlogAddSerializers
    http_method_names = ['post']
    # permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():   # raise_exception=True  全部校验，调用Serializers的validate方法
                return JsonResponse({'status': 0, 'msg': '验证未通过'})
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return JsonResponse({'data': serializer.data, 'status': 1, 'headers': headers})
        except Exception as e:
            return JsonResponse({'status': 0, 'msg': e})

    def perform_create(self, serializer):
        '''进行保存之类的操作'''
        user = self.request.user
        title = serializer.data.get('title')
        content = serializer.data.get('content')
        blog = self.model(title=title, content=content, user=user, blog_type_id=3)
        blog.save()
        return blog

