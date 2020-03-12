from django.views.generic import View, FormView
from django.http import JsonResponse
from comment.models import Comment
from comment.forms import CommentForms
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class CommentSubmit(FormView):
    '''
    处理post过来的数据，及保存数据
    :param request:
    :return:
    '''

    model = Comment
    form_class = CommentForms
    data = {}

    def get_form_kwargs(self):
        kwargs = super(CommentSubmit, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        comment = self.model()
        comment.user = form.cleaned_data.get('user')
        comment.content_object = form.cleaned_data.get('comment_obj')
        comment.text = form.cleaned_data.get('text')

        parent = form.cleaned_data.get('parent')
        if parent is not None:      # 父级存在，则是回复数据
            # 顶级评论：如果父级的顶级评论存在则这条回复的顶级评论也是父级的顶级评论， 如果不存在，那么父级就是这条回复的顶级评论
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.replay_to = parent.user     # 回复的上条评论者是父级的评论者
        comment.save()

        # 返回的数据
        self.data['status'] = 0
        self.data['user'] = comment.user.nickname_or_username
        self.data['comment_time'] = comment.comment_time.timestamp()
        self.data['text'] = comment.text
        self.data['replay_to'] = comment.replay_to.nickname_or_username if parent is not None else ''
        self.data['id'] = comment.id
        self.data['root_id'] = comment.root.id if comment.root is not None else ''
        self.data['content_type'] = ContentType.objects.get_for_model(comment).model
        return self.render_to_response(self.data)

    def form_invalid(self, form):
        self.data['status'] = 1
        self.data['message'] = list(form.errors.values())[0][0]
        return self.render_to_response(self.data)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
