#!/usr/bin/env python
import os
import sys
import django
import datetime
from django.utils import timezone

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_admin.settings")
django.setup()

# 导入模型
from blog_api.models import (
    BlogOwner, WorkExperience, Education, Achievement, Skill,
    Projects, ProjectTags, ProjectTagMapping, Blogs, BlogTags,
    BlogTagMapping, ChatMessages, Visitors, SystemSettings
)

def clear_data():
    """清除所有现有数据"""
    print("清除现有数据...")
    BlogTagMapping.objects.all().delete()
    BlogTags.objects.all().delete()
    Blogs.objects.all().delete()
    ProjectTagMapping.objects.all().delete()
    ProjectTags.objects.all().delete()
    Projects.objects.all().delete()
    Skill.objects.all().delete()
    Achievement.objects.all().delete()
    Education.objects.all().delete()
    WorkExperience.objects.all().delete()
    ChatMessages.objects.all().delete()
    Visitors.objects.all().delete()
    SystemSettings.objects.all().delete()
    BlogOwner.objects.all().delete()
    print("数据已清除")

def add_blog_owner():
    """添加博客所有者数据"""
    print("添加博客所有者...")
    BlogOwner.objects.create(
        id=1,
        username="admin",
        password="pbkdf2_sha256$260000$q8XVTzAqiUaQBSvEWBtTtO$1yK4CmUJ3Bi6NZQe1+JDzPrx0rI7QkaU3JnBt6yTuU4=",  # 密码为'admin123'
        email="admin@example.com",
        avatar_url="https://ui-avatars.com/api/?name=Admin&background=0D8ABC&color=fff",
        github_url="https://github.com/admin",
        github_username="admin",
        bio="这是一个个人博客网站的管理员账号",
        country="中国",
        city="北京",
        identity="全栈开发工程师",
        last_login=timezone.now()
    )
    print("博客所有者添加成功")

def add_work_experience():
    """添加工作经验数据"""
    print("添加工作经验...")
    work_experiences = [
        {
            "project_name": "个人博客系统",
            "position": "全栈开发工程师",
            "description": "设计并开发了一个基于Django和Vue的个人博客系统，实现了文章管理、项目展示等功能。",
            "start_date": datetime.date(2023, 1, 1),
            "end_date": None,
            "display_order": 1
        },
        {
            "project_name": "企业管理系统",
            "position": "后端开发工程师",
            "description": "参与开发了一个企业级管理系统，负责API设计和实现，数据库优化等工作。",
            "start_date": datetime.date(2022, 3, 1),
            "end_date": datetime.date(2022, 12, 31),
            "display_order": 2
        },
        {
            "project_name": "在线教育平台",
            "position": "前端开发工程师",
            "description": "参与开发了一个在线教育平台的前端部分，使用Vue.js实现了响应式界面和交互功能。",
            "start_date": datetime.date(2021, 6, 1),
            "end_date": datetime.date(2022, 2, 28),
            "display_order": 3
        }
    ]

    for exp_data in work_experiences:
        WorkExperience.objects.create(**exp_data)
    print(f"成功添加 {len(work_experiences)} 条工作经验")

def add_education():
    """添加教育经历数据"""
    print("添加教育经历...")
    educations = [
        {
            "school_name": "北京大学",
            "major": "计算机科学与技术",
            "degree": "硕士",
            "start_date": datetime.date(2018, 9, 1),
            "end_date": datetime.date(2021, 7, 1),
            "display_order": 1
        },
        {
            "school_name": "清华大学",
            "major": "软件工程",
            "degree": "学士",
            "start_date": datetime.date(2014, 9, 1),
            "end_date": datetime.date(2018, 7, 1),
            "display_order": 2
        }
    ]

    for edu_data in educations:
        Education.objects.create(**edu_data)
    print(f"成功添加 {len(educations)} 条教育经历")

def add_achievements():
    """添加成就数据"""
    print("添加成就...")
    achievements = [
        {
            "name": "优秀毕业生",
            "description": "被评为校级优秀毕业生",
            "date": datetime.date(2021, 6, 30),
            "location": "北京",
            "display_order": 1
        },
        {
            "name": "编程大赛一等奖",
            "description": "在全国大学生编程大赛中获得一等奖",
            "date": datetime.date(2020, 11, 15),
            "location": "上海",
            "display_order": 2
        },
        {
            "name": "优秀项目奖",
            "description": "开发的个人博客项目在校园创新创业大赛中获得优秀项目奖",
            "date": datetime.date(2019, 5, 20),
            "location": "北京",
            "display_order": 3
        }
    ]

    for ach_data in achievements:
        Achievement.objects.create(**ach_data)
    print(f"成功添加 {len(achievements)} 条成就")

def add_skills():
    """添加技能数据"""
    print("添加技能...")
    skills = [
        {
            "name": "Python",
            "proficiency": 90,
            "category": "编程语言",
            "display_order": 1
        },
        {
            "name": "JavaScript",
            "proficiency": 85,
            "category": "编程语言",
            "display_order": 2
        },
        {
            "name": "TypeScript",
            "proficiency": 80,
            "category": "编程语言",
            "display_order": 3
        },
        {
            "name": "Django",
            "proficiency": 85,
            "category": "后端框架",
            "display_order": 4
        },
        {
            "name": "Vue.js",
            "proficiency": 80,
            "category": "前端框架",
            "display_order": 5
        },
        {
            "name": "MySQL",
            "proficiency": 75,
            "category": "数据库",
            "display_order": 6
        },
        {
            "name": "Docker",
            "proficiency": 70,
            "category": "DevOps",
            "display_order": 7
        },
        {
            "name": "Git",
            "proficiency": 85,
            "category": "开发工具",
            "display_order": 8
        },
    ]

    for skill_data in skills:
        Skill.objects.create(**skill_data)
    print(f"成功添加 {len(skills)} 条技能")

def add_projects():
    """添加项目数据"""
    print("添加项目...")
    projects = [
        {
            "github_id": "project1",
            "name": "personal-blog",
            "full_name": "admin/personal-blog",
            "description": "基于Django和Vue开发的个人博客系统",
            "url": "https://github.com/admin/personal-blog",
            "owner": "admin",
            "language": "Python",
            "stars_count": 120,
            "forks_count": 35,
            "watchers_count": 15,
            "open_issues_count": 5,
            "created_at": timezone.now() - datetime.timedelta(days=365),
            "updated_at": timezone.now() - datetime.timedelta(days=7),
            "fetched_at": timezone.now(),
            "trending_rank": 1,
            "is_favorite": True,
            "notes": "我的主要项目"
        },
        {
            "github_id": "project2",
            "name": "vue-dashboard",
            "full_name": "admin/vue-dashboard",
            "description": "基于Vue.js开发的管理后台模板",
            "url": "https://github.com/admin/vue-dashboard",
            "owner": "admin",
            "language": "JavaScript",
            "stars_count": 85,
            "forks_count": 20,
            "watchers_count": 10,
            "open_issues_count": 2,
            "created_at": timezone.now() - datetime.timedelta(days=300),
            "updated_at": timezone.now() - datetime.timedelta(days=14),
            "fetched_at": timezone.now(),
            "trending_rank": 2,
            "is_favorite": True,
            "notes": "我的Vue项目模板"
        },
        {
            "github_id": "project3",
            "name": "django-rest-api",
            "full_name": "admin/django-rest-api",
            "description": "使用Django REST framework开发的API示例",
            "url": "https://github.com/admin/django-rest-api",
            "owner": "admin",
            "language": "Python",
            "stars_count": 65,
            "forks_count": 15,
            "watchers_count": 8,
            "open_issues_count": 1,
            "created_at": timezone.now() - datetime.timedelta(days=250),
            "updated_at": timezone.now() - datetime.timedelta(days=21),
            "fetched_at": timezone.now(),
            "trending_rank": 3,
            "is_favorite": False,
            "notes": "API开发示例"
        }
    ]

    project_objects = []
    for proj_data in projects:
        project_objects.append(Projects.objects.create(**proj_data))
    
    # 添加项目标签
    tags = ["Python", "JavaScript", "Vue.js", "Django", "Web开发", "前端", "后端"]
    tag_objects = []
    for tag_name in tags:
        tag_objects.append(ProjectTags.objects.create(
            name=tag_name,
            description=f"{tag_name}相关项目",
            count=0
        ))
    
    # 建立项目和标签的关系
    mappings = [
        (0, 0), (0, 3), (0, 4), (0, 6),  # personal-blog: Python, Django, Web开发, 后端
        (1, 1), (1, 2), (1, 4), (1, 5),  # vue-dashboard: JavaScript, Vue.js, Web开发, 前端
        (2, 0), (2, 3), (2, 4), (2, 6)   # django-rest-api: Python, Django, Web开发, 后端
    ]
    
    for proj_idx, tag_idx in mappings:
        ProjectTagMapping.objects.create(
            project=project_objects[proj_idx],
            tag=tag_objects[tag_idx]
        )
        # 更新标签使用次数
        tag = tag_objects[tag_idx]
        tag.count += 1
        tag.save()
        
    print(f"成功添加 {len(projects)} 个项目和 {len(tags)} 个项目标签")

def add_blogs():
    """添加博客文章数据"""
    print("添加博客文章...")
    blogs = [
        {
            "title": "Django与Vue.js结合开发全栈应用",
            "content": """
# Django与Vue.js结合开发全栈应用

在这篇文章中，我将分享如何使用Django作为后端，Vue.js作为前端来开发一个全栈应用。

## 后端设置

首先，我们需要安装Django和Django REST framework：

```bash
pip install django djangorestframework django-cors-headers
```

然后，创建一个新的Django项目：

```bash
django-admin startproject backend
cd backend
python manage.py startapp api
```

## 前端设置

接下来，我们需要设置Vue.js项目：

```bash
npm install -g @vue/cli
vue create frontend
```

## 连接前后端

为了让前端能够与后端通信，我们需要设置CORS：

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'corsheaders',
    'rest_framework',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]
```

## 结论

通过结合Django和Vue.js，我们可以构建功能强大的全栈应用，Django提供了强大的后端能力，Vue.js则提供了灵活的前端开发体验。
            """,
            "cover_image": "https://via.placeholder.com/800x400?text=Django+and+Vue.js",
            "summary": "学习如何使用Django和Vue.js开发全栈应用",
            "category": "Web开发",
            "published": True,
            "published_at": timezone.now() - datetime.timedelta(days=30),
            "views_count": 256,
            "featured": True
        },
        {
            "title": "TypeScript在Vue项目中的应用",
            "content": """
# TypeScript在Vue项目中的应用

TypeScript为JavaScript添加了静态类型检查，这在大型项目中非常有用。本文将探讨如何在Vue项目中使用TypeScript。

## 为什么在Vue项目中使用TypeScript？

- 更好的代码补全和智能提示
- 在编译时捕获错误
- 更好的代码组织和可维护性
- 更清晰的组件属性和方法定义

## 设置Vue + TypeScript项目

使用Vue CLI创建支持TypeScript的项目：

```bash
vue create my-ts-app
# 选择手动设置并包含TypeScript
```

## 在Vue组件中使用TypeScript

```typescript
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    message: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      count: 0
    };
  },
  methods: {
    increment(): void {
      this.count++;
    }
  }
});
</script>
```

## 使用Vue 3 Composition API

```typescript
<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  setup() {
    const count = ref<number>(0)
    
    function increment(): void {
      count.value++
    }
    
    return {
      count,
      increment
    }
  }
})
</script>
```

## 结论

在Vue项目中使用TypeScript可以提高代码质量，减少bug，并提供更好的开发体验。随着项目规模的增长，TypeScript带来的好处将越来越明显。
            """,
            "cover_image": "https://via.placeholder.com/800x400?text=TypeScript+and+Vue",
            "summary": "了解在Vue项目中使用TypeScript的好处和方法",
            "category": "前端开发",
            "published": True,
            "published_at": timezone.now() - datetime.timedelta(days=15),
            "views_count": 187,
            "featured": True
        },
        {
            "title": "Django REST framework入门指南",
            "content": """
# Django REST framework入门指南

Django REST framework (DRF) 是一个强大的工具包，用于构建Web API。本文将介绍DRF的基础知识和使用方法。

## 安装和设置

```bash
pip install djangorestframework
```

在settings.py中添加DRF：

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
]
```

## 创建模型

```python
# models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
```

## 创建序列化器

```python
# serializers.py
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
```

## 创建视图

```python
# views.py
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

## 配置URL

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

## 结论

Django REST framework提供了一种简单而强大的方式来构建API。它有很多内置功能，如身份验证、权限、分页等，使API开发变得更加容易。
            """,
            "cover_image": "https://via.placeholder.com/800x400?text=Django+REST+framework",
            "summary": "Django REST framework的基础知识和使用方法",
            "category": "后端开发",
            "published": True,
            "published_at": timezone.now() - datetime.timedelta(days=7),
            "views_count": 124,
            "featured": False
        },
        {
            "title": "使用Docker部署Django应用",
            "content": """
# 使用Docker部署Django应用

Docker可以帮助我们创建一个一致的开发和生产环境，本文将介绍如何使用Docker部署Django应用。

## 编写Dockerfile

首先，在项目根目录创建一个Dockerfile：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
```

## 创建docker-compose.yml

```yaml
version: '3'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env.db
  
  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - ./.env

volumes:
  postgres_data:
```

## 创建环境变量文件

.env.db:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=myproject
```

.env:
```
DEBUG=0
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@db:5432/myproject
```

## 启动容器

```bash
docker-compose up -d --build
```

## 运行迁移

```bash
docker-compose exec web python manage.py migrate
```

## 创建超级用户

```bash
docker-compose exec web python manage.py createsuperuser
```

## 结论

使用Docker部署Django应用可以简化部署过程，并确保开发和生产环境的一致性。Docker Compose使得管理多个相关容器变得更加简单。
            """,
            "cover_image": "https://via.placeholder.com/800x400?text=Docker+and+Django",
            "summary": "学习如何使用Docker容器部署Django应用",
            "category": "DevOps",
            "published": True,
            "published_at": timezone.now() - datetime.timedelta(days=3),
            "views_count": 98,
            "featured": False
        },
        {
            "title": "Vue 3组合式API指南",
            "content": """
# Vue 3组合式API指南

Vue 3引入了组合式API，这是一种新的编写Vue组件的方式。本文将介绍组合式API的基础知识和使用方法。

## 什么是组合式API？

组合式API (Composition API) 是Vue 3引入的一种新特性，它提供了一种更灵活的方式来组织组件逻辑。与选项式API相比，组合式API允许我们按照逻辑关注点来组织代码，而不是按照选项类型。

## 基本使用

```html
<template>
  <div>
    <p>Count: {{ count }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const count = ref(0)
    
    function increment() {
      count.value++
    }
    
    return {
      count,
      increment
    }
  }
}
</script>
```

## 响应式引用

在组合式API中，我们使用`ref`和`reactive`来创建响应式状态：

```javascript
import { ref, reactive } from 'vue'

// 使用ref处理简单值
const count = ref(0)
// 修改值
count.value++

// 使用reactive处理对象
const state = reactive({
  name: 'John',
  age: 25
})
// 修改对象属性
state.age++
```

## 计算属性和监听器

```javascript
import { ref, computed, watch } from 'vue'

const count = ref(0)

// 计算属性
const doubleCount = computed(() => count.value * 2)

// 监听器
watch(count, (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`)
})
```

## 生命周期钩子

```javascript
import { onMounted, onUpdated, onUnmounted } from 'vue'

export default {
  setup() {
    onMounted(() => {
      console.log('Component mounted')
    })
    
    onUpdated(() => {
      console.log('Component updated')
    })
    
    onUnmounted(() => {
      console.log('Component unmounted')
    })
  }
}
```

## 结论

Vue 3的组合式API提供了一种更灵活、更可组合的方式来构建Vue组件。它特别适合在处理大型组件时，可以将相关逻辑分组在一起，提高代码的可读性和可维护性。
            """,
            "cover_image": "https://via.placeholder.com/800x400?text=Vue+3+Composition+API",
            "summary": "学习Vue 3组合式API的基础知识和使用方法",
            "category": "前端开发",
            "published": False,
            "published_at": None,
            "views_count": 0,
            "featured": False
        }
    ]

    blog_objects = []
    for blog_data in blogs:
        blog_objects.append(Blogs.objects.create(**blog_data))
    
    # 添加博客标签
    tags = ["Django", "Vue.js", "TypeScript", "Docker", "Python", "JavaScript", "REST API", "Web开发"]
    tag_objects = []
    for tag_name in tags:
        tag_objects.append(BlogTags.objects.create(
            name=tag_name,
            count=0
        ))
    
    # 建立博客和标签的关系
    mappings = [
        (0, 0), (0, 1), (0, 7),  # Django与Vue.js结合: Django, Vue.js, Web开发
        (1, 1), (1, 2), (1, 5),  # TypeScript在Vue项目: Vue.js, TypeScript, JavaScript
        (2, 0), (2, 4), (2, 6),  # Django REST framework: Django, Python, REST API
        (3, 0), (3, 3), (3, 4),  # Docker部署Django: Django, Docker, Python
        (4, 1), (4, 5), (4, 7)   # Vue 3组合式API: Vue.js, JavaScript, Web开发 - 修复了这里
    ]
    
    for blog_idx, tag_idx in mappings:
        BlogTagMapping.objects.create(
            blog=blog_objects[blog_idx],
            tag=tag_objects[tag_idx]
        )
        # 更新标签使用次数
        tag = tag_objects[tag_idx]
        tag.count += 1
        tag.save()
        
    print(f"成功添加 {len(blogs)} 篇博客文章和 {len(tags)} 个博客标签")

def add_visitors():
    """添加访客数据"""
    print("添加访客数据...")
    now = timezone.now()
    visitors = []

    # 生成过去30天的访问数据
    for day in range(30):
        day_date = now - datetime.timedelta(days=day)
        # 每天随机5-20次访问
        for _ in range(5 + day % 15):
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            visit_time = day_date.replace(hour=hour, minute=minute, second=second)
            
            # 随机页面
            pages = [
                "/",
                "/blog",
                "/blog/1",
                "/blog/2",
                "/projects",
                "/about",
                "/contact"
            ]
            page = random.choice(pages)
            
            # 随机IP和用户代理
            ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
            ]
            user_agent = random.choice(agents)
            
            visitors.append(Visitors(
                ip_address=ip,
                user_agent=user_agent,
                visit_time=visit_time,
                page_url=page,
                referer=random.choice(["https://google.com", "https://bing.com", None, None]),
                country=random.choice(["中国", "美国", "日本", None]),
                city=random.choice(["北京", "上海", "纽约", "东京", None])
            ))
    
    Visitors.objects.bulk_create(visitors)
    print(f"成功添加 {len(visitors)} 条访客记录")

def add_system_settings():
    """添加系统设置"""
    print("添加系统设置...")
    settings = [
        {
            "setting_key": "site_name",
            "setting_value": "我的个人博客",
            "description": "网站名称",
            "updated_at": timezone.now()
        },
        {
            "setting_key": "site_description",
            "setting_value": "一个展示个人项目和博客的网站",
            "description": "网站描述",
            "updated_at": timezone.now()
        },
        {
            "setting_key": "theme",
            "setting_value": "light",
            "description": "网站主题",
            "updated_at": timezone.now()
        },
        {
            "setting_key": "posts_per_page",
            "setting_value": "10",
            "description": "每页显示的博客文章数量",
            "updated_at": timezone.now()
        },
        {
            "setting_key": "enable_comments",
            "setting_value": "true",
            "description": "是否启用评论功能",
            "updated_at": timezone.now()
        }
    ]

    for setting_data in settings:
        SystemSettings.objects.create(**setting_data)
    print(f"成功添加 {len(settings)} 条系统设置")

if __name__ == "__main__":
    import random  # 导入random模块用于生成随机数据
    
    clear_data()
    add_blog_owner()
    add_work_experience()
    add_education()
    add_achievements()
    add_skills()
    add_projects()
    add_blogs()
    add_visitors()
    add_system_settings()
    
    print("所有测试数据添加完成！") 