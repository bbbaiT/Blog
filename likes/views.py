from django.views.generic import View
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from likes.models import LikeSum, LikeEveryOne
# Create your views here.


class LikeUpdate(View):
    data = {}

    def get(self, request, *args, **kwargs):
        model = request.GET.get('content_type')
        user = request.user

        if not user.is_authenticated:
            return self.is_invaild(code=403, message='用户尚未登录')
        try:
            object_id = int(request.GET.get('object_id'))
            content_type = ContentType.objects.get(model=model)
            model_cls = content_type.model_class()
            model_cls.objects.get(id=object_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('点赞对象不存在')

        if request.GET.get('is_like') == 'false':       # 没有检测到点赞记录,要进行点赞
            return self.like(content_type, object_id, user)
        else:
            return self.unlike(content_type, object_id, user)

    def like(self, content_type, object_id, user):
        # 进行点赞操作,没有记录
        like_one, created = LikeEveryOne.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:     # 未点赞过，已经创建了一条记录
            like_sum, created_sum = LikeSum.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_sum.like_num += 1
            like_sum.save()
            return self.is_vaild(201, '点赞成功', like_sum.like_num)
        else:
            # 已经点赞过，不能继续点赞
            return self.is_invaild(401, '点赞失败')

    def unlike(self, content_type, object_id, user):
        # 取消点赞操作
            # 检测用户是否已有点赞记录
        if LikeEveryOne.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有记录,删除记录
            like_one = LikeEveryOne.objects.filter(content_type=content_type, object_id=object_id, user=user)
            like_one.delete()
            # 并且总数-1
            like_sum, created_sum = LikeSum.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created_sum:     # 没有创建一条新的，表示库中已有数据
                like_sum.like_num -= 1
                like_sum.save()
                return self.is_vaild(202, '取消点赞成功', like_sum.like_num)
        # 数据库中没有点赞记录，不能取消点赞
        return self.is_invaild(402, '取消点赞失败')

    def is_vaild(self, code, message, like_num):
        # 验证通过
        self.data['status'] = code
        self.data['message'] = message
        self.data['like_num'] = like_num
        return self.render_to_response(self.data)

    def is_invaild(self, code, message):
        # 验证未通过
        self.data['status'] = code
        self.data['message'] = message
        return self.render_to_response(self.data)

    def render_to_response(self, context):
        return JsonResponse(context)
