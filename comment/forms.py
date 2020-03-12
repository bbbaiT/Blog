# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from comment.models import Comment


class CommentForms(forms.Form):
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'))
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    # 记录回复的评论的id
    replay_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'replay_id'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')   # 将user利用关键字传入这里，并将其取出
        super(CommentForms, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')

        object_id = self.cleaned_data.get('object_id')
        content_type_str = self.cleaned_data.get('content_type')
        try:
            model_class_obj = ContentType.objects.get(model=content_type_str).model_class()
            comment_obj = model_class_obj.objects.get(id=object_id)
            self.cleaned_data['comment_obj'] = comment_obj
        except ObjectDoesNotExist:      # 捕获对象不存在的错误
            raise forms.ValidationError('评论对象不存在')

        self.cleaned_data['replay_id'] = self.check_replay_id()

        return self.cleaned_data

    def check_replay_id(self):
        replay_id = self.cleaned_data['replay_id']      # 回复的评论的id
        if replay_id < 0:
            raise forms.ValidationError('回复对象不存在')
        elif replay_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(id=replay_id).exists():     # id>0 且数据库中存在这条评论数据
            self.cleaned_data['parent'] = Comment.objects.get(id=replay_id)
        else:
            raise forms.ValidationError('回复对象不存在')
        return replay_id
