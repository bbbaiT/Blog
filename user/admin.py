from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import MyUser


class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)
    list_display = ('username', 'email', 'nickname', 'is_staff', 'is_active', 'is_superuser')

    def nickname(self, obj):
        return obj.myuser.nickname
    nickname.short_description = '昵称'       # 后台显示的描述


# 重新注册
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')
