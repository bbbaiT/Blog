import datetime
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from Api.serializers import UserSerializer, BlogSerializers, BlogAddSerializers
from blog.models import Blog
from django.utils import timezone
# Create your views here.


class MyPageNumberPagination(PageNumberPagination):
    '''
    自定义分页，
    '''
    page_size = 10      # 每页显示的数量
    page_size_query_param = 'size'      # 默认每页显示10个，可以通过传入pager1/?p=2&size=4,改变默认每页显示的个数
    page_query_param = 'p'          # get请求页码时的参数
    max_page_size = 10      # 每页最大显示条数
    last_page_strings = ('last',)        # 最后一页的别名, 默认为('last',)，建议改为()

    def get_paginated_response(self, data):
        return JsonResponse(
            {
                'code': 200,
                'count': self.page.paginator.count,     # 所有对象的总数量
                'page_size': self.page_size,            # 每一页显示的数量
                'page_nums': self.page.paginator.num_pages,  # 页码总页数
                'next': self.get_next_link(),       # 下一页的链接
                'previous': self.get_previous_link(),   # 上一页的链接
                'data': data,   # 返回的数据列表
            }
        )


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

        # 满足条件的话，就表示token已失效，重新一个生成一个token
        if timezone.now() > (token.created + datetime.timedelta(hours=2)):
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
        return token


class BlogListView(APIView):
    '''博文列表'''
    model = Blog
    serializer_class = BlogSerializers
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        qyeryset = self.get_queryset()
        pagination = MyPageNumberPagination()       # 分页
        pg_obj = pagination.paginate_queryset(qyeryset, request, view=self)        # 这个方法获取分页，并获取当前这一页的对象集
        data = BlogSerializers(instance=pg_obj, many=True).data

        return pagination.get_paginated_response(data)

    def get_queryset(self):
        return self.model.objects.all()


class BlogDetailView(generics.RetrieveAPIView):
    '''博文详情'''
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    lookup_field = 'id'             # 传递进来的参数
    http_method_names = ['get']     # 指定的请求方式

    def get(self, request, *args, **kwargs):
        instance = self.get_object()        # 获取指定的对象
        serializer = self.get_serializer(instance)      # 对象数据转化为Json数据

        return JsonResponse(serializer.data)


class BlogAddView(generics.CreateAPIView):
    '''添加博文，需要登录'''
    model = Blog
    serializer_class = BlogAddSerializers
    http_method_names = ['post']
    permission_classes = (IsAuthenticated, )

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

