from django.contrib import admin
from comment.models import Comment
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'text', 'user', 'comment_time', 'object_id')
