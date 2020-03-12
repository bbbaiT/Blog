from django.contrib import admin
from read_statistics.models import ReadNumSum, ReadNumDay

# Register your models here.


@admin.register(ReadNumSum)
class ReadNumSumAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'read_num', 'object_id']


@admin.register(ReadNumDay)
class ReadNumDayAdmin(admin.ModelAdmin):
    list_display = ['read_date', 'content_object', 'read_num', 'object_id']
