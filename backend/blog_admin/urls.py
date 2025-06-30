"""
URL configuration for blog_admin project.
blog_admin 项目的 URL 配置。

The `urlpatterns` list routes URLs to views. For more information please see:
`urlpatterns` 列表将 URL 路由到视图。更多信息请参见：
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
示例：
Function views
函数视图
    1. Add an import:  from my_app import views
    1. 添加导入：  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    2. 向 urlpatterns 添加 URL：  path('', views.home, name='home')
Class-based views
基于类的视图
    1. Add an import:  from other_app.views import Home
    1. 添加导入：  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    2. 向 urlpatterns 添加 URL：  path('', Home.as_view(), name='home')
Including another URLconf
包含另一个 URLconf
    1. Import the include() function: from django.urls import include, path
    1. 导入 include() 函数：from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    2. 向 urlpatterns 添加 URL：  path('blog/', include('blog.urls'))
"""
# 导入 Django 管理后台模块
from django.contrib import admin
# 导入 Django URL 处理函数
from django.urls import path, include
# 导入 DRF 路由器
from rest_framework import routers
# 导入所有视图集
from blog_api.views import (
    BlogOwnerViewSet,          # 博客所有者视图集
    WorkExperienceViewSet,     # 工作经验视图集
    EducationViewSet,          # 教育经历视图集
    AchievementViewSet,        # 成就视图集
    SkillViewSet,              # 技能视图集
    ProjectsViewSet,           # 项目视图集
    ProjectTagsViewSet,        # 项目标签视图集
    ProjectTagMappingViewSet,  # 项目标签映射视图集
    BlogsViewSet,              # 博客文章视图集
    BlogTagsViewSet,           # 博客标签视图集
    BlogTagMappingViewSet,     # 博客标签映射视图集
    ChatMessagesViewSet,       # 聊天消息视图集
    VisitorsViewSet,           # 访客统计视图集
    SystemSettingsViewSet,     # 系统设置视图集
    login_view                 # 自定义登录视图
)
# 导入 Django 设置
from django.conf import settings
# 导入静态文件处理函数
from django.conf.urls.static import static

# 创建 DRF 默认路由器实例
router = routers.DefaultRouter()
# 注册博客所有者 API 路由，URL 前缀为 'blog-owner'
router.register(r'blog-owner', BlogOwnerViewSet)
# 注册工作经验 API 路由，URL 前缀为 'work-experiences'
router.register(r'work-experiences', WorkExperienceViewSet)
# 注册教育经历 API 路由，URL 前缀为 'education'
router.register(r'education', EducationViewSet)
# 注册成就 API 路由，URL 前缀为 'achievements'
router.register(r'achievements', AchievementViewSet)
# 注册技能 API 路由，URL 前缀为 'skills'
router.register(r'skills', SkillViewSet)
# 注册项目 API 路由，URL 前缀为 'projects'
router.register(r'projects', ProjectsViewSet)
# 注册项目标签 API 路由，URL 前缀为 'project-tags'
router.register(r'project-tags', ProjectTagsViewSet)
# 注册项目标签映射 API 路由，URL 前缀为 'project-tag-mappings'
router.register(r'project-tag-mappings', ProjectTagMappingViewSet)
# 注册博客文章 API 路由，URL 前缀为 'blogs'
router.register(r'blogs', BlogsViewSet)
# 注册博客标签 API 路由，URL 前缀为 'blog-tags'
router.register(r'blog-tags', BlogTagsViewSet)
# 注册博客标签映射 API 路由，URL 前缀为 'blog-tag-mappings'
router.register(r'blog-tag-mappings', BlogTagMappingViewSet)
# 注册聊天消息 API 路由，URL 前缀为 'chat-messages'
router.register(r'chat-messages', ChatMessagesViewSet)
# 注册访客统计 API 路由，URL 前缀为 'visitors'
router.register(r'visitors', VisitorsViewSet)
# 注册系统设置 API 路由，URL 前缀为 'settings'
router.register(r'settings', SystemSettingsViewSet)

# 定义 URL 模式列表
urlpatterns = [
    # Django 管理后台 URL，访问路径为 '/admin/'
    path('admin/', admin.site.urls),
    # API 根路径，包含所有路由器中定义的 URL，访问路径为 '/api/'
    path('api/', include(router.urls)),
    # DRF 认证 URL，用于登录/登出等功能，访问路径为 '/api/api-auth/'
    path('api/api-auth/', include('rest_framework.urls')),
    # 自定义登录视图
    path('api/login/', login_view, name='login'),
    # 添加博客所有者更新API
    path('api/blog-owner/update_profile/', BlogOwnerViewSet.as_view({'put': 'update_profile'}), name='blog-owner-update'),
    # 添加系统设置获取API
    path('api/settings/get/', SystemSettingsViewSet.as_view({'get': 'get_settings'}), name='settings-get'),
    # 添加系统设置更新API
    path('api/settings/update/', SystemSettingsViewSet.as_view({'put': 'update_settings'}), name='settings-update'),
    # 添加访客统计概览API
    path('api/visitor-stats/overview/', VisitorsViewSet.as_view({'get': 'overview'}), name='visitor-stats-overview'),
    # 添加访客趋势API
    path('api/visitor-stats/trends/', VisitorsViewSet.as_view({'get': 'trends'}), name='visitor-stats-trends'),
    # 添加设备统计API
    path('api/visitor-stats/devices/', VisitorsViewSet.as_view({'get': 'devices'}), name='visitor-stats-devices'),
    # 添加浏览器统计API
    path('api/visitor-stats/browsers/', VisitorsViewSet.as_view({'get': 'browsers'}), name='visitor-stats-browsers'),
    # 添加页面浏览统计API
    path('api/visitor-stats/pages/', VisitorsViewSet.as_view({'get': 'pages'}), name='visitor-stats-pages'),
    # 添加系统日志API
    path('api/settings/logs/', SystemSettingsViewSet.as_view({'get': 'logs'}), name='system-logs'),
    # 添加系统日志内容API
    path('api/settings/logs/content/', SystemSettingsViewSet.as_view({'get': 'logs_content'}), name='system-log-content'),
    # 添加清除缓存API
    path('api/settings/clear-cache/', SystemSettingsViewSet.as_view({'post': 'clear_cache'}), name='clear-cache'),
    # 添加备份数据库API
    path('api/settings/backup-database/', SystemSettingsViewSet.as_view({'post': 'backup_database'}), name='backup-database'),
    # 添加测试邮件API
    path('api/settings/test-email/', SystemSettingsViewSet.as_view({'post': 'test_email'}), name='test-email'),
]

# 如果是调试模式，添加媒体文件的 URL 配置
if settings.DEBUG:
    # 添加媒体文件的 URL 配置，使得开发环境可以访问上传的媒体文件
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
