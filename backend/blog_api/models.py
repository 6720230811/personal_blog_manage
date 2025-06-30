from django.db import models  # 导入Django数据库模型模块

# Create your models here.  # 创建你的模型

class BlogOwner(models.Model):
    """博客所有者模型，存储个人信息"""  # 模型的文档字符串说明
    id = models.IntegerField(primary_key=True)  # 主键字段，使用整数
    username = models.CharField("用户名", max_length=50)  # 用户名字段，最大长度50
    password = models.CharField("密码", max_length=255)  # 密码字段，最大长度255
    email = models.EmailField("邮箱", max_length=100)  # 邮箱字段，最大长度100
    avatar_url = models.CharField("头像URL", max_length=255, null=True, blank=True)  # 头像URL字段，可为空
    github_url = models.CharField("GitHub链接", max_length=255, null=True, blank=True)  # GitHub链接字段，可为空
    github_username = models.CharField("GitHub用户名", max_length=50, null=True, blank=True)  # GitHub用户名字段，可为空
    bio = models.TextField("个人简介", null=True, blank=True)  # 个人简介字段，可为空
    country = models.CharField("国家", max_length=50, null=True, blank=True)  # 国家字段，可为空
    city = models.CharField("城市", max_length=50, null=True, blank=True)  # 城市字段，可为空
    identity = models.CharField("身份", max_length=100, null=True, blank=True)  # 身份字段，可为空
    last_login = models.DateTimeField("上次登录时间", null=True, blank=True)  # 上次登录时间字段，可为空
    phone = models.CharField("电话", max_length=20, null=True, blank=True)  # 电话字段，可为空
    address = models.CharField("地址", max_length=255, null=True, blank=True)  # 地址字段，可为空
    birthday = models.DateField("生日", null=True, blank=True)  # 生日字段，可为空

    class Meta:  # 元数据类
        verbose_name = "博客所有者"  # 单数形式的显示名称
        verbose_name_plural = "博客所有者"  # 复数形式的显示名称
        db_table = "BlogOwner"  # 指定数据库表名

    def __str__(self):  # 字符串表示方法
        return self.username  # 返回用户名作为对象的字符串表示


class WorkExperience(models.Model):
    """工作经验模型"""  # 模型的文档字符串说明
    project_name = models.CharField("项目名称", max_length=100)  # 项目名称字段，最大长度100
    position = models.CharField("职位", max_length=100)  # 职位字段，最大长度100
    description = models.TextField("描述", null=True, blank=True)  # 描述字段，可为空
    start_date = models.DateField("开始日期")  # 开始日期字段
    end_date = models.DateField("结束日期", null=True, blank=True)  # 结束日期字段，可为空
    display_order = models.IntegerField("显示顺序", default=0)  # 显示顺序字段，默认值为0

    class Meta:  # 元数据类
        verbose_name = "工作经验"  # 单数形式的显示名称
        verbose_name_plural = "工作经验"  # 复数形式的显示名称
        db_table = "WorkExperience"  # 指定数据库表名
        ordering = ["display_order"]  # 按显示顺序排序

    def __str__(self):  # 字符串表示方法
        return f"{self.position} - {self.project_name}"  # 返回职位和项目名称作为对象的字符串表示


class Education(models.Model):
    """教育经历模型"""  # 模型的文档字符串说明
    school_name = models.CharField("学校名称", max_length=100)  # 学校名称字段，最大长度100
    major = models.CharField("专业", max_length=100, null=True, blank=True)  # 专业字段，可为空
    degree = models.CharField("学位", max_length=50, null=True, blank=True)  # 学位字段，可为空
    start_date = models.DateField("开始日期")  # 开始日期字段
    end_date = models.DateField("结束日期", null=True, blank=True)  # 结束日期字段，可为空
    display_order = models.IntegerField("显示顺序", default=0)  # 显示顺序字段，默认值为0

    class Meta:  # 元数据类
        verbose_name = "教育经历"  # 单数形式的显示名称
        verbose_name_plural = "教育经历"  # 复数形式的显示名称
        db_table = "Education"  # 指定数据库表名
        ordering = ["display_order"]  # 按显示顺序排序

    def __str__(self):  # 字符串表示方法
        return f"{self.school_name} - {self.major or '未指定专业'}"  # 返回学校名称和专业作为对象的字符串表示


class Achievement(models.Model):
    """成就模型"""  # 模型的文档字符串说明
    name = models.CharField("成就名称", max_length=150)  # 成就名称字段，最大长度150
    description = models.TextField("描述", null=True, blank=True)  # 描述字段，可为空
    date = models.DateField("日期", null=True, blank=True)  # 日期字段，可为空
    location = models.CharField("地点", max_length=100, null=True, blank=True)  # 地点字段，可为空
    display_order = models.IntegerField("显示顺序", default=0)  # 显示顺序字段，默认值为0

    class Meta:  # 元数据类
        verbose_name = "成就"  # 单数形式的显示名称
        verbose_name_plural = "成就"  # 复数形式的显示名称
        db_table = "Achievement"  # 指定数据库表名
        ordering = ["display_order"]  # 按显示顺序排序

    def __str__(self):  # 字符串表示方法
        return self.name  # 返回成就名称作为对象的字符串表示


class Skill(models.Model):
    """技能模型"""  # 模型的文档字符串说明
    name = models.CharField("技能名称", max_length=100)  # 技能名称字段，最大长度100
    proficiency = models.IntegerField("熟练度")  # 熟练度字段
    category = models.CharField("类别", max_length=50, null=True, blank=True)  # 类别字段，可为空
    display_order = models.IntegerField("显示顺序", default=0)  # 显示顺序字段，默认值为0

    class Meta:  # 元数据类
        verbose_name = "技能"  # 单数形式的显示名称
        verbose_name_plural = "技能"  # 复数形式的显示名称
        db_table = "Skill"  # 指定数据库表名
        ordering = ["display_order"]  # 按显示顺序排序
        indexes = [  # 创建索引
            models.Index(fields=["category"])  # 为类别字段创建索引
        ]

    def __str__(self):  # 字符串表示方法
        return self.name  # 返回技能名称作为对象的字符串表示


class Projects(models.Model):
    """项目模型"""  # 模型的文档字符串说明
    github_id = models.CharField("GitHub ID", max_length=100, unique=True)  # GitHub ID字段，唯一
    name = models.CharField("项目名称", max_length=100)  # 项目名称字段，最大长度100
    full_name = models.CharField("完整名称", max_length=150)  # 完整名称字段，最大长度150
    description = models.TextField("描述", null=True, blank=True)  # 描述字段，可为空
    url = models.CharField("URL", max_length=255)  # URL字段，最大长度255
    owner = models.CharField("所有者", max_length=100)  # 所有者字段，最大长度100
    language = models.CharField("语言", max_length=50, null=True, blank=True)  # 语言字段，可为空
    stars_count = models.IntegerField("星标数", default=0)  # 星标数字段，默认值为0
    forks_count = models.IntegerField("分支数", default=0)  # 分支数字段，默认值为0
    watchers_count = models.IntegerField("观察者数", default=0)  # 观察者数字段，默认值为0
    open_issues_count = models.IntegerField("开放问题数", default=0)  # 开放问题数字段，默认值为0
    created_at = models.DateTimeField("创建时间")  # 创建时间字段
    updated_at = models.DateTimeField("更新时间")  # 更新时间字段
    fetched_at = models.DateTimeField("获取时间")  # 获取时间字段
    trending_rank = models.IntegerField("趋势排名", null=True, blank=True)  # 趋势排名字段，可为空
    is_favorite = models.BooleanField("是否收藏", default=False)  # 是否收藏字段，默认值为False
    notes = models.TextField("备注", null=True, blank=True)  # 备注字段，可为空

    class Meta:  # 元数据类
        verbose_name = "项目"  # 单数形式的显示名称
        verbose_name_plural = "项目"  # 复数形式的显示名称
        db_table = "Projects"  # 指定数据库表名
        indexes = [  # 创建索引
            models.Index(fields=["trending_rank"]),  # 为趋势排名字段创建索引
            models.Index(fields=["language"]),  # 为语言字段创建索引
            models.Index(fields=["stars_count"])  # 为星标数字段创建索引
        ]

    def __str__(self):  # 字符串表示方法
        return self.full_name  # 返回完整名称作为对象的字符串表示


class ProjectTags(models.Model):
    """项目标签模型"""  # 模型的文档字符串说明
    name = models.CharField("标签名称", max_length=50, unique=True)  # 标签名称字段，唯一
    description = models.CharField("描述", max_length=255, null=True, blank=True)  # 描述字段，可为空
    count = models.IntegerField("使用次数", default=0)  # 使用次数字段，默认值为0

    class Meta:  # 元数据类
        verbose_name = "项目标签"  # 单数形式的显示名称
        verbose_name_plural = "项目标签"  # 复数形式的显示名称
        db_table = "ProjectTags"  # 指定数据库表名

    def __str__(self):  # 字符串表示方法
        return self.name  # 返回标签名称作为对象的字符串表示


class ProjectTagMapping(models.Model):
    """项目标签映射模型"""  # 模型的文档字符串说明
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, verbose_name="项目")  # 项目外键，级联删除
    tag = models.ForeignKey(ProjectTags, on_delete=models.CASCADE, verbose_name="标签")  # 标签外键，级联删除

    class Meta:  # 元数据类
        verbose_name = "项目标签映射"  # 单数形式的显示名称
        verbose_name_plural = "项目标签映射"  # 复数形式的显示名称
        db_table = "ProjectTag_Mapping"  # 指定数据库表名
        unique_together = (("project", "tag"),)  # 项目和标签的组合必须唯一

    def __str__(self):  # 字符串表示方法
        return f"{self.project.name} - {self.tag.name}"  # 返回项目名称和标签名称的组合作为对象的字符串表示


class Blogs(models.Model):
    """博客文章模型"""  # 模型的文档字符串说明
    title = models.CharField("标题", max_length=255)  # 标题字段，最大长度255
    content = models.TextField("内容")  # 内容字段
    cover_image = models.CharField("封面图片", max_length=255, null=True, blank=True)  # 封面图片字段，可为空
    summary = models.TextField("摘要", null=True, blank=True)  # 摘要字段，可为空
    category = models.CharField("分类", max_length=50)  # 分类字段，最大长度50
    published = models.BooleanField("是否发布", default=False)  # 是否发布字段，默认值为False
    published_at = models.DateTimeField("发布时间", null=True, blank=True)  # 发布时间字段，可为空
    created_at = models.DateTimeField("创建时间", auto_now_add=True)  # 创建时间字段，自动添加当前时间
    updated_at = models.DateTimeField("更新时间", auto_now=True)  # 更新时间字段，自动更新为当前时间
    views_count = models.IntegerField("浏览量", default=0)  # 浏览量字段，默认值为0
    featured = models.BooleanField("是否推荐", default=False)  # 是否推荐字段，默认值为False

    class Meta:  # 元数据类
        verbose_name = "博客文章"  # 单数形式的显示名称
        verbose_name_plural = "博客文章"  # 复数形式的显示名称
        db_table = "Blogs"  # 指定数据库表名
        indexes = [  # 创建索引
            models.Index(fields=["category"]),  # 为分类字段创建索引
            models.Index(fields=["published_at"]),  # 为发布时间字段创建索引
            models.Index(fields=["featured"])  # 为是否推荐字段创建索引
        ]

    def __str__(self):  # 字符串表示方法
        return self.title  # 返回标题作为对象的字符串表示


class BlogTags(models.Model):
    """博客标签模型"""  # 模型的文档字符串说明
    name = models.CharField("标签名称", max_length=50, unique=True)  # 标签名称字段，唯一
    count = models.IntegerField("使用次数", default=0)  # 使用次数字段，默认值为0

    class Meta:  # 元数据类
        verbose_name = "博客标签"  # 单数形式的显示名称
        verbose_name_plural = "博客标签"  # 复数形式的显示名称
        db_table = "BlogTags"  # 指定数据库表名

    def __str__(self):  # 字符串表示方法
        return self.name  # 返回标签名称作为对象的字符串表示


class BlogTagMapping(models.Model):
    """博客标签映射模型"""  # 模型的文档字符串说明
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, verbose_name="博客")  # 博客外键，级联删除
    tag = models.ForeignKey(BlogTags, on_delete=models.CASCADE, verbose_name="标签")  # 标签外键，级联删除

    class Meta:  # 元数据类
        verbose_name = "博客标签映射"  # 单数形式的显示名称
        verbose_name_plural = "博客标签映射"  # 复数形式的显示名称
        db_table = "BlogTag_Mapping"  # 指定数据库表名
        unique_together = (("blog", "tag"),)  # 博客和标签的组合必须唯一

    def __str__(self):  # 字符串表示方法
        return f"{self.blog.title} - {self.tag.name}"  # 返回博客标题和标签名称的组合作为对象的字符串表示


class ChatMessages(models.Model):
    """聊天消息模型"""  # 模型的文档字符串说明
    session_id = models.CharField("会话ID", max_length=50)  # 会话ID字段，最大长度50
    role = models.CharField("角色", max_length=10)  # 角色字段，最大长度10
    content = models.TextField("内容")  # 内容字段
    timestamp = models.DateTimeField("时间戳")  # 时间戳字段
    related_project = models.ForeignKey(Projects, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="相关项目")  # 相关项目外键，可为空，设置为NULL

    class Meta:  # 元数据类
        verbose_name = "聊天消息"  # 单数形式的显示名称
        verbose_name_plural = "聊天消息"  # 复数形式的显示名称
        db_table = "ChatMessages"  # 指定数据库表名
        indexes = [  # 创建索引
            models.Index(fields=["session_id"]),  # 为会话ID字段创建索引
            models.Index(fields=["timestamp"])  # 为时间戳字段创建索引
        ]

    def __str__(self):  # 字符串表示方法
        return f"{self.role} - {self.timestamp}"  # 返回角色和时间戳的组合作为对象的字符串表示


class Visitors(models.Model):
    """访客模型"""  # 模型的文档字符串说明
    ip_address = models.CharField("IP地址", max_length=45)  # IP地址字段，最大长度45
    user_agent = models.CharField("用户代理", max_length=255, null=True, blank=True)  # 用户代理字段，可为空
    visit_time = models.DateTimeField("访问时间")  # 访问时间字段
    page_url = models.CharField("页面URL", max_length=255)  # 页面URL字段，最大长度255
    referer = models.CharField("来源", max_length=255, null=True, blank=True)  # 来源字段，可为空
    country = models.CharField("国家", max_length=50, null=True, blank=True)  # 国家字段，可为空
    city = models.CharField("城市", max_length=50, null=True, blank=True)  # 城市字段，可为空

    class Meta:  # 元数据类
        verbose_name = "访客"  # 单数形式的显示名称
        verbose_name_plural = "访客"  # 复数形式的显示名称
        db_table = "Visitors"  # 指定数据库表名
        indexes = [  # 创建索引
            models.Index(fields=["visit_time"]),  # 为访问时间字段创建索引
            models.Index(fields=["ip_address"]),  # 为IP地址字段创建索引
            models.Index(fields=["page_url"])  # 为页面URL字段创建索引
        ]

    def __str__(self):  # 字符串表示方法
        return f"{self.ip_address} - {self.visit_time}"  # 返回IP地址和访问时间的组合作为对象的字符串表示


class SystemSettings(models.Model):
    """系统设置模型"""  # 模型的文档字符串说明
    setting_key = models.CharField("设置键", max_length=50, unique=True)  # 设置键字段，唯一
    setting_value = models.TextField("设置值")  # 设置值字段
    description = models.CharField("描述", max_length=255, null=True, blank=True)  # 描述字段，可为空
    updated_at = models.DateTimeField("更新时间", auto_now=True)  # 更新时间字段，自动更新为当前时间

    class Meta:  # 元数据类
        verbose_name = "系统设置"  # 单数形式的显示名称
        verbose_name_plural = "系统设置"  # 复数形式的显示名称
        db_table = "SystemSettings"  # 指定数据库表名

    def __str__(self):  # 字符串表示方法
        return self.setting_key  # 返回设置键作为对象的字符串表示
