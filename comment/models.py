from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your views here.


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    user = models.ForeignKey(User, related_name='comment_usr', on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)

    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.CASCADE)
    # 回复的父级是哪条评论的内容，如果是第一条评论，则没有父级
    parent = models.ForeignKey('self', null=True, related_name='parent_comment', on_delete=models.CASCADE)
    # 记录回复谁的评论
    # (由于这个外键和上面的user关联到同一个外键，所以需要加related_name给当前外键设置一个别名，Uer模型可通过这个别名找到对应的数据信息)
    replay_to = models.ForeignKey(User, null=True, related_name='replay_to', on_delete=models.CASCADE)

    def __str__(self):
        return self.content_object

    class Meta:
        # ordering = ['-comment_time', '-object_id']
        verbose_name = '评论信息'
        verbose_name_plural = '评论信息'
