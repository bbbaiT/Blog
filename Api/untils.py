# coding=utf-8
from django.http.response import JsonResponse
import time

def to_time_stamp(date):
    '''
    把datetime转变为时间戳
    向 js 传值的时候,时间戳还需要*1000
    '''
    # this_date = datetime.datetime.strptime(str(date), '%Y-%m-%d')
    this_date = time.mktime(date.timetuple())
    return this_date * 1000


def json_response(code, err=""):
    return {
        "code": code,
        'err': err,
    }
