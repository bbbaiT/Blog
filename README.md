- 使用python3.6
- 基于Django后端渲染开发的博客网站，具有点赞，评论，回复，站内通知，邮件通知功能
- API功能处于测试，未启用
    - 已完成 文章列表，文章详情， 分类查询， 年份查询， 搜索接口
    - 接口url见Api.urls
- 使用mysql数据库
- 配置`Environmental_Public/environmental`文件中的数据库信息
    - 使用blog库(需要自建)
- 配置`mysite/settings/production`文件中的qq邮箱账号及密钥（可以改变邮箱，需自行修改）
- 配置`mysite/settings/production`文件中的SECRET_KEY，可通过下列代码生成
    ```python
    from django.core.management import utils
    utils.get_random_secret_key()
    ```
