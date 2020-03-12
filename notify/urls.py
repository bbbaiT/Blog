# -*- coding: utf-8 -*-
from django.urls import path
from notify.views import NotifyAll, NotifyReadToUnread, NotifyDelete


urlpatterns = [
    path('', NotifyAll.as_view(), name='notification'),
    path('<int:info_id>', NotifyReadToUnread.as_view(), name='notification_read'),
    path('delete/', NotifyDelete.as_view(), name='notification_delete'),
]

