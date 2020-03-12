# -*- coding: utf-8 -*-
import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.cache import cache


class LoginForms(forms.Form):
    '''
    登录表单
    '''
    username = forms.CharField(label='用户名', required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入用户名'})
                            )
    password = forms.CharField(label='密码', required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入密码'}),
                               )

    def clean(self):
        '''
        处理和验证信息，对象的.id_valid()方法会调用此方法
        :return:
        '''
        username = self.cleaned_data.get('username', '')
        password = self.cleaned_data.get('password', '')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')      # 登录验证失败，抛出验证错误
        self.cleaned_data['user'] = user        # 由于view中要用到，所以放入cleaned_data,一起传出去
        return self.cleaned_data


class RegisterForms(forms.Form):
    '''
    注册表单
    '''
    nickname = forms.CharField(max_length=15, min_length=5, label='昵称', required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入5-15位昵称'}))
    username = forms.CharField(label='用户名', required=True, min_length=5, max_length=15,
                               widget=forms.TextInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入5-15位用户名'}))
    password = forms.CharField(label='密码', required=True, min_length=3, max_length=9,
                               widget=forms.PasswordInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入3-9位密码'}),)
    rpassword = forms.CharField(label='确认密码', required=True,min_length=3, max_length=9,
                               widget=forms.PasswordInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请再次输入密码'}),)
    email = forms.EmailField(label='邮箱', required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入邮箱'}))

    def clean(self):
        self.cleaned_data['username'] = self.check_username()
        self.cleaned_data['rpassword'] = self.check_password()
        self.cleaned_data['email'] = self.check_email()
        return self.cleaned_data

    def check_username(self,):
        '''
        验证用户是否重复
        :return:
        '''
        username = self.cleaned_data.get('username', '')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def check_password(self):
        '''
        验证两次输入的密码是否一致
        :return:
        '''
        password = self.cleaned_data.get('password', '')
        rpassword = self.cleaned_data.get('rpassword', '')
        if password != rpassword or rpassword == '':
            raise forms.ValidationError('两次密码不一致')
        else:
            return rpassword

    def check_email(self):
        '''
        验证邮箱是否已绑定
        :return:
        '''
        email = self.cleaned_data.get('email', '')
        if email != '' and User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已绑定')
        return email


class ModifiesDataForms(forms.Form):
    '''
    修改资料表单
    '''
    nickname = forms.CharField(max_length=15, min_length=5, label='昵称', required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入5-15位昵称'}))
    username = forms.CharField(label='用户名', required=True, min_length=5, max_length=15,
                               widget=forms.TextInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入5-15位用户名'}))
    email = forms.EmailField(label='邮箱', required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入邮箱'}))
    verificationcode = forms.CharField(label='验证码', required=False, max_length=4,
                            widget=forms.TextInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '修改邮箱请点击获取验证码到邮箱'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')   # 将user利用关键字传入这里，并将其取出
        super(ModifiesDataForms, self).__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data['user'] = self.check_user()
        self.check_username()
        self.check_nickname()
        self.check_email()
        return self.cleaned_data

    def check_user(self):
        '''
        验证用户是否登录
        :return:
        '''
        if not self.request.user.is_authenticated:
            raise forms.ValidationError('用户未登录')
        return self.request.user

    def check_username(self):
        '''
        验证用户名是否已存在
        :return:
        '''
        user_name = self.cleaned_data.get('username', '')
        if user_name != User.objects.get(id=self.request.user.id).username and User.objects.filter(username=user_name).exists():
            raise forms.ValidationError('用户名已存在')
        return user_name

    def check_nickname(self):
        '''
        检测昵称是否为空
        :return:
        '''
        nick_name = self.cleaned_data.get('nickname', '').strip()
        if nick_name == '':
            raise forms.ValidationError('新的昵称不得为空')
        return nick_name

    def check_email(self):
        '''
        检测邮箱及验证码
        :return:
        '''
        email = self.cleaned_data.get('email', '')
        code = self.cleaned_data.get('verificationcode', '')

        if email != '':
            if re.findall('^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$', email):
                if email == User.objects.get(id=self.request.user.id).email:        # 未改邮箱
                    return email
                if User.objects.filter(email=email).exists():                       # 邮箱已存在
                    raise forms.ValidationError('邮箱已绑定')
                if code == '':                                              # 未输入验证码
                    raise forms.ValidationError('请输入验证码')
                if cache.get(self.request.user) != code:           # 验证码不对
                    raise forms.ValidationError('验证码不正确或已失效')
                cache.delete(self.request.user)                     # 验证码验证完成之后删除验证码
            else:
                raise forms.ValidationError('邮箱未找到')
        return email


class ModifyPassword(forms.Form):
    old_password = forms.CharField(label='旧密码', required=True,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入旧密码'}))
    new_password = forms.CharField(label='新密码', required=True, min_length=3, max_length=9,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请输入3-9位新密码'}))
    r_new_password = forms.CharField(label='再一次输入新密码', required=True, min_length=3, max_length=9,
                                     widget=forms.PasswordInput(attrs={'class': 'form-control input-sm chat-input', 'placeholder': '请再次输入3-9位新密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ModifyPassword, self).__init__(*args, **kwargs)

    def clean(self):
        old_password = self.check_old_password()
        new_password = self.check_new_password()
        if old_password == new_password:
            raise forms.ValidationError('新密码不可以旧密码一致')
        return self.cleaned_data

    def check_old_password(self):
        '''
        检测旧密码是否正确
        :return:
        '''
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码输入错误')
        return old_password

    def check_new_password(self):
        '''
        检测两次输入的新密码是否一致
        :return:
        '''
        new_password = self.cleaned_data.get('new_password', '')
        r_new_password = self.cleaned_data.get('r_new_password', '')
        if new_password != r_new_password or r_new_password == '':
            raise forms.ValidationError('两次输入的新密码不一致')
        return r_new_password
