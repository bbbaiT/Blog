# -*- coding: utf-8 -*-
'''
生产环境
'''
from Environmental_Public.environmental import mysql


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'srryuc6j8y03!0y-g7z*=_zk#0v%j_(d#ql*(^hf)0xly8%f$v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': mysql['db'],  # 数据库名称
        'USER': mysql['user'],      # 登录账户
        'PASSWORD': mysql['password'],    # 密码
        'HOST': mysql['host'],  # 服务器地址
        'POST': mysql['port'],  # 端口
    }
}


# 邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = ''  # qq邮箱用户名
EMAIL_HOST_PASSWORD = ''       # 邮箱密钥
EMAIL_SUBJECT_PREFIX = '[个人网站]'     # 邮箱前缀，默认是 [Django]
EMAIL_USE_SSL = True         # 启用安全链接


# 配置管理员的邮箱
ADMINS = (
    ('admin', ''),
)
# 配置生产环境的log输出
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {               # 这是log文件输出配置
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '',  # log输出为位置及名称
        },
        'mail_admins': {        # 发送邮件配置
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],       # 调用哪个配置
            'level': 'DEBUG',
            'propagate': True,          # 出现DEBUG等级以上的信息是否也被记录
        },
        'django.request': {             # ERROR发送邮件
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
