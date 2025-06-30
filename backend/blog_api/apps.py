from django.apps import AppConfig  # 导入Django应用配置类


class BlogApiConfig(AppConfig):  # 定义博客API应用的配置类，继承自AppConfig
    """博客API应用配置"""
    default_auto_field = 'django.db.models.BigAutoField'  # 设置默认主键字段类型为BigAutoField（64位整数）
    name = 'blog_api'  # 设置应用名称为'blog_api'，Django通过这个名称识别应用
    
    def ready(self):  # 当应用准备就绪时执行的方法
        """应用就绪时执行的操作"""
        # 可以在这里导入信号处理器或执行其他初始化操作
        pass
