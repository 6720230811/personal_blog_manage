from django.contrib import admin  # 导入Django管理后台模块
from .models import (  # 从当前应用的models.py导入所有模型
    BlogOwner, WorkExperience, Education, Achievement,
    Skill, Projects, ProjectTags, ProjectTagMapping,
    Blogs, BlogTags, BlogTagMapping, ChatMessages,
    Visitors, SystemSettings
)

# Register your models here.
# 注册模型到Django管理后台

@admin.register(BlogOwner)  # 使用装饰器注册BlogOwner模型
class BlogOwnerAdmin(admin.ModelAdmin):  # 定义BlogOwner的管理界面类，继承自ModelAdmin
    """博客所有者管理"""
    list_display = ('id', 'username', 'email', 'identity', 'last_login')  # 在列表页显示的字段
    search_fields = ('username', 'email')  # 可搜索的字段
    list_filter = ('last_login',)  # 可筛选的字段


@admin.register(WorkExperience)  # 使用装饰器注册WorkExperience模型
class WorkExperienceAdmin(admin.ModelAdmin):  # 定义WorkExperience的管理界面类
    """工作经验管理"""
    list_display = ('project_name', 'position', 'start_date', 'end_date', 'display_order')  # 列表显示字段
    search_fields = ('project_name', 'position')  # 搜索字段
    list_filter = ('start_date',)  # 筛选字段
    ordering = ('display_order',)  # 默认排序方式


@admin.register(Education)  # 使用装饰器注册Education模型
class EducationAdmin(admin.ModelAdmin):  # 定义Education的管理界面类
    """教育经历管理"""
    list_display = ('school_name', 'major', 'degree', 'start_date', 'end_date', 'display_order')  # 列表显示字段
    search_fields = ('school_name', 'major')  # 搜索字段
    list_filter = ('degree', 'start_date')  # 筛选字段
    ordering = ('display_order',)  # 默认排序方式


@admin.register(Achievement)  # 使用装饰器注册Achievement模型
class AchievementAdmin(admin.ModelAdmin):  # 定义Achievement的管理界面类
    """成就管理"""
    list_display = ('name', 'date', 'location', 'display_order')  # 列表显示字段
    search_fields = ('name', 'description')  # 搜索字段
    list_filter = ('date', 'location')  # 筛选字段
    ordering = ('display_order',)  # 默认排序方式


@admin.register(Skill)  # 使用装饰器注册Skill模型
class SkillAdmin(admin.ModelAdmin):  # 定义Skill的管理界面类
    """技能管理"""
    list_display = ('name', 'category', 'proficiency', 'display_order')  # 列表显示字段
    search_fields = ('name', 'category')  # 搜索字段
    list_filter = ('category', 'proficiency')  # 筛选字段
    ordering = ('display_order',)  # 默认排序方式


@admin.register(Projects)  # 使用装饰器注册Projects模型
class ProjectsAdmin(admin.ModelAdmin):  # 定义Projects的管理界面类
    """项目管理"""
    list_display = ('name', 'full_name', 'language', 'stars_count', 'is_favorite', 'trending_rank', 'updated_at')  # 列表显示字段
    search_fields = ('name', 'full_name', 'description')  # 搜索字段
    list_filter = ('language', 'is_favorite', 'created_at')  # 筛选字段
    ordering = ('-updated_at',)  # 默认排序方式，'-'表示降序
    list_per_page = 20  # 每页显示的记录数


@admin.register(ProjectTags)  # 使用装饰器注册ProjectTags模型
class ProjectTagsAdmin(admin.ModelAdmin):  # 定义ProjectTags的管理界面类
    """项目标签管理"""
    list_display = ('name', 'description', 'count')  # 列表显示字段
    search_fields = ('name', 'description')  # 搜索字段
    ordering = ('name',)  # 默认按名称升序排序


@admin.register(ProjectTagMapping)  # 使用装饰器注册ProjectTagMapping模型
class ProjectTagMappingAdmin(admin.ModelAdmin):  # 定义ProjectTagMapping的管理界面类
    """项目标签映射管理"""
    list_display = ('project', 'tag')  # 列表显示字段
    search_fields = ('project__name', 'tag__name')  # 搜索字段，支持跨关系搜索
    list_filter = ('tag',)  # 按标签筛选


@admin.register(Blogs)  # 使用装饰器注册Blogs模型
class BlogsAdmin(admin.ModelAdmin):  # 定义Blogs的管理界面类
    """博客文章管理"""
    list_display = ('title', 'category', 'published', 'featured', 'views_count', 'created_at', 'published_at')  # 列表显示字段
    search_fields = ('title', 'content', 'summary')  # 搜索字段
    list_filter = ('category', 'published', 'featured', 'created_at')  # 筛选字段
    ordering = ('-created_at',)  # 默认按创建时间降序排序
    list_per_page = 20  # 每页显示的记录数
    date_hierarchy = 'created_at'  # 日期层次结构导航


@admin.register(BlogTags)  # 使用装饰器注册BlogTags模型
class BlogTagsAdmin(admin.ModelAdmin):  # 定义BlogTags的管理界面类
    """博客标签管理"""
    list_display = ('name', 'count')  # 列表显示字段
    search_fields = ('name',)  # 搜索字段
    ordering = ('name',)  # 默认按名称升序排序


@admin.register(BlogTagMapping)  # 使用装饰器注册BlogTagMapping模型
class BlogTagMappingAdmin(admin.ModelAdmin):  # 定义BlogTagMapping的管理界面类
    """博客标签映射管理"""
    list_display = ('blog', 'tag')  # 列表显示字段
    search_fields = ('blog__title', 'tag__name')  # 搜索字段，支持跨关系搜索
    list_filter = ('tag',)  # 按标签筛选


@admin.register(ChatMessages)  # 使用装饰器注册ChatMessages模型
class ChatMessagesAdmin(admin.ModelAdmin):  # 定义ChatMessages的管理界面类
    """聊天消息管理"""
    list_display = ('session_id', 'role', 'timestamp', 'related_project')  # 列表显示字段
    search_fields = ('session_id', 'content')  # 搜索字段
    list_filter = ('role', 'timestamp')  # 筛选字段
    ordering = ('-timestamp',)  # 默认按时间戳降序排序
    list_per_page = 50  # 每页显示的记录数


@admin.register(Visitors)  # 使用装饰器注册Visitors模型
class VisitorsAdmin(admin.ModelAdmin):  # 定义Visitors的管理界面类
    """访客管理"""
    list_display = ('ip_address', 'page_url', 'visit_time', 'country', 'city')  # 列表显示字段
    search_fields = ('ip_address', 'page_url', 'user_agent')  # 搜索字段
    list_filter = ('visit_time', 'country', 'city')  # 筛选字段
    ordering = ('-visit_time',)  # 默认按访问时间降序排序
    list_per_page = 50  # 每页显示的记录数
    date_hierarchy = 'visit_time'  # 日期层次结构导航


@admin.register(SystemSettings)  # 使用装饰器注册SystemSettings模型
class SystemSettingsAdmin(admin.ModelAdmin):  # 定义SystemSettings的管理界面类
    """系统设置管理"""
    list_display = ('setting_key', 'description', 'updated_at')  # 列表显示字段
    search_fields = ('setting_key', 'description')  # 搜索字段
    ordering = ('setting_key',)  # 默认按设置键名升序排序
