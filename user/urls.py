# -*- coding: utf-8 -*-
from django.urls import path
from user.views import UserLogin, LoginModal, UserLogout, UserInfo, SendMail, ModifyData, ModifyPassWord, UserRegister

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login_web/', UserLogin.as_view(), name='login_web'),
    path('login_modal/', LoginModal.as_view(), name='login_modal'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('info/', UserInfo.as_view(), name='user_info'),
    path('modify_data/', ModifyData.as_view(), name='modify_data'),
    path('send_mail_code/', SendMail.as_view(), name='send_mail_code'),
    path('modify_password/', ModifyPassWord.as_view(), name='modify_password'),
]
