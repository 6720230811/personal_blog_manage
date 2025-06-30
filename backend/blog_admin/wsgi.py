"""
WSGI config for blog_admin project.
blog_admin 项目的 WSGI 配置。

It exposes the WSGI callable as a module-level variable named ``application``.
它将 WSGI 可调用对象作为名为 ``application`` 的模块级变量公开。

For more information on this file, see
有关此文件的更多信息，请参见：
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# 导入操作系统模块，用于环境变量设置
import os

# 从 Django 导入 WSGI 应用程序处理函数
from django.core.wsgi import get_wsgi_application

# 设置默认的 Django 设置模块路径
# 这行代码告诉 Django 使用 blog_admin.settings 模块作为配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_admin.settings')

# 创建 WSGI 应用程序对象
# 这个对象将被 WSGI 服务器（如 Gunicorn、uWSGI）用来与 Django 应用通信
application = get_wsgi_application()
