import string
import random
from time import time
from django.views.generic import FormView, View, CreateView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.cache import cache
from user.forms import LoginForms, RegisterForms, ModifiesDataForms, ModifyPassword
from mysite.settings.production import EMAIL_HOST_USER
# Create your views here.


class UserLogin(FormView):
    '''
    登录表单
    '''
    form_class = LoginForms
    template_name = 'user_login.html'

    def form_valid(self, form):
        user = form.cleaned_data['user']
        login(self.request, user)
        return super(UserLogin, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('from', '/')

    def get_context_data(self, **kwargs):
        kwargs['login_form'] = self.get_form()
        return kwargs


class LoginModal(View):
    '''
    弹窗登录
    :param request:
    :return:
    '''
    def post(self, request, *args, **kwargs):
        login_form = LoginForms(request.POST)       # 将post传入的数据传入对象中
        data = {}
        if login_form.is_valid():                   # 调用对象的is_valid(),数据校验方法
            user = login_form.cleaned_data['user']      # 校验成功之后会自动把提交的数据形成一个字典cleaned_data
            login(request, user)
            data['status'] = 200
        else:
            data['status'] = 201

        return JsonResponse(data)


class UserLogout(View):
    '''
    登出
    :param request:
    :return:
    '''
    def get(self, request, *args, **kwargs):
        logout(request)
        refere = request.META.get('HTTP_REFERER', '/')
        if 'user' in refere or 'notify' in refere:
            return redirect(reverse('home'))
        return redirect(refere)


class UserInfo(View):
    '''
    用户信息
    '''
    template_name = 'user_info.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SendMail(View):
    '''
    发送邮箱验证码
    '''
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', '')
        data = {}
        if email != '' and '@' in email:
            code = ''.join(random.sample(string.ascii_letters + string.digits, k=4))
            cache.set(key=request.user, value=code, timeout=900)
            if time() - request.session.get('send_code_time', 0) < 30:
                data['status'] = 403
            else:
                request.session['send_code_time'] = time()
                send_mail(
                    subject='邮箱验证码',
                    message='验证码：{}, 区分大小写,15分钟内有效'.format(code),
                    from_email=EMAIL_HOST_USER,       # 发送人邮件地址
                    recipient_list=[email],
                    fail_silently=False,
                )
                data['status'] = 200
        else:
            data['status'] = 403
        return JsonResponse(data)


class ModifyData(FormView):
    '''
    修改个人资料
    :param request:
    :return:
    '''
    model = User
    form_class = ModifiesDataForms
    template_name = 'modifies_data.html'

    def get_initial(self):
        '''
        获取初始值
        :return:
        '''
        return {'nickname': self.request.user.nickname, 'username': self.request.user.username, 'email': self.request.user.email}

    def get_form_kwargs(self):
        '''
        向form传入其他值，默认只传入post请求过来的数据和文件
        :return:
        '''
        kwargs = super(ModifyData, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form):
        nick_name = form.cleaned_data.get('nickname', '')
        user_name = form.cleaned_data.get('username', '')
        email = form.cleaned_data.get('email', '')

        user, create = self.model.objects.get_or_create(id=self.request.user.id)
        user.nickname = nick_name
        user.username = user_name
        user.email = email
        user.save()
        return super(ModifyData, self).form_valid(form)

    def get_success_url(self):
        return reverse('user_info')

    def get_context_data(self, **kwargs):
        kwargs['ModifyForms'] = self.get_form()
        return kwargs


class ModifyPassWord(FormView):
    '''
    修改密码
    :param request:
    :return:
    '''
    form_class = ModifyPassword
    template_name = 'modify_password.html'

    def get_form_kwargs(self):
        kwargs = super(ModifyPassWord, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

    def form_valid(self, form):
        password = form.cleaned_data.get('r_new_password', '')
        self.request.user.set_password(password)
        self.request.user.save()
        logout(self.request)
        return super(ModifyPassWord, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['modify_password_form'] = self.get_form()
        return kwargs

    def get_success_url(self):
        return reverse('login_web')


class UserRegister(FormView):
    '''
    用户注册
    '''
    model = User
    form_class = RegisterForms
    template_name = 'user_register.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        rpassword = form.cleaned_data['rpassword']
        email = form.cleaned_data['email']
        nick_name = form.cleaned_data['nickname']

        user = self.model.objects.create_user(username=username, password=rpassword, email=email)
        user.nickname = nick_name
        user.save()

        login(self.request, user)
        return super(UserRegister, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('from', '/')

    def get_context_data(self, **kwargs):
        kwargs['register_form'] = self.get_form()
        return kwargs
