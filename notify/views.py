from django.views.generic import ListView, View
from django.shortcuts import render, get_object_or_404, redirect, reverse
from notifications.models import Notification

# Create your views here.


class NotifyAll(ListView):
    '''
    所有消息
    :param request:
    :return:
    '''
    template_name = 'notification.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        context['notification_query'] = self.request.user.notifications.all().filter(deleted=False)
        return context


class NotifyReadToUnread(View):
    '''
    点击查看详情，同时将未读的置为已读
    :param request:
    :return:
    '''
    model = Notification
    pk_url_kwarg = 'info_id'

    def get(self, request, *args, **kwargs):
        nocity = get_object_or_404(self.model, id=kwargs.get(self.pk_url_kwarg))
        nocity.unread = False
        nocity.save()
        return self.render_to_response(nocity)

    def render_to_response(self, nocity):
        return redirect(nocity.data.get('url', reverse('notification')))


class NotifyDelete(View):
    '''
    删除所有已读消息，不是真的删除，只是把deleted属性置位True
    :param requests:
    :return:
    '''
    model = Notification

    def get(self, request, *args, **kwargs):
        for notification in self.model.objects.read():
            notification.deleted = True
            notification.save()
        return self.render_to_response()

    def render_to_response(self):
        return redirect(reverse('notification'))
