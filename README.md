# 个人博客后台管理系统

基于Vue3、TypeScript和Django实现的个人博客后台管理系统
<div style="display: flex; overflow-x: auto; gap: 10px; padding: 10px 0;">
  <img src="images/1.png" style="height: 200px; flex-shrink: 0;">
  <img src="images/2.png" style="height: 200px; flex-shrink: 0;">
  <img src="images/3.png" style="height: 200px; flex-shrink: 0;">
  <img src="images/4.png" style="height: 200px; flex-shrink: 0;">
  <img src="images/5.png" style="height: 200px; flex-shrink: 0;">

</div>
## 技术栈

### 后端
- Django
- Django REST Framework
- MySQL

### 前端
- Vue 3
- TypeScript
- Vuex
- Vue Router
- Element Plus
- Axios

## 项目结构

```
personal_blog_admin/
├── backend/               # Django后端
│   ├── blog_admin/        # Django项目配置
│   └── blog_api/          # Django应用
│        ├── models.py     # 数据模型
│        ├── serializers.py # 序列化器
│        ├── views.py      # 视图函数
│        └── ...
└── frontend/              # Vue前端
    ├── public/            # 静态资源
    └── src/               # 源代码
        ├── api/           # API接口
        ├── assets/        # 资源文件
        ├── components/    # 组件
        ├── layout/        # 布局组件
        ├── router/        # 路由
        ├── store/         # Vuex状态
        ├── types/         # TypeScript类型
        ├── utils/         # 工具函数
        ├── views/         # 页面视图
        ├── App.vue        # 根组件
        └── main.ts        # 入口文件
```

## 功能列表

- 博客管理（增删改查）
- 博客标签管理
- 项目管理
- 项目标签管理
- 技能管理
- 教育经历管理
- 工作经历管理
- 成就管理
- 个人信息管理
- 访客统计
- 系统设置

## 开发说明

### 后端开发

1. 安装依赖：
   ```
   pip install django djangorestframework django-cors-headers mysqlclient
   ```

2. 数据库配置：
   - 确保MySQL服务已启动
   - 导入`create_personal_blog_db.sql`创建数据库和表结构

3. 运行Django后端：
   ```
   cd backend
   python manage.py migrate
   python manage.py runserver
   ```

### 前端开发

1. 安装依赖：
   ```
   cd frontend
   npm install
   ```

2. 运行开发服务器：
   ```
   npm run dev
   ```

3. 打包生产环境：
   ```
   npm run build
   ```

## 部署说明

### Django后端部署

1. 配置Django生产环境设置
2. 使用Gunicorn/uWSGI作为WSGI服务器
3. 配置Nginx作为代理服务器

### 前端部署

1. 构建前端：
   ```
   cd frontend
   npm run build
   ```

2. 将生成的dist目录内容部署到web服务器 


personal_blog_admin 个人博客后台管理系统
这是一个基于 Vue 3 + TypeScript 前端和 Django 后端的个人博客后台管理系统，主要用于管理个人博客、项目、技能等内容。
目录结构解析
1. 后端部分 (backend/)
blog_admin/ - Django 项目配置目录
settings.py - Django 项目配置文件，包含数据库、中间件等设置
urls.py - 全局 URL 路由配置，定义了 API 端点
asgi.py/wsgi.py - 应用服务器接口文件
blog_api/ - API 应用目录
models.py - 数据模型定义（注意：实际模型在 SQL 文件中定义）
serializers.py - REST API 序列化器，处理数据转换
views.py - API 视图函数，处理请求和响应
migrations/ - 数据库迁移文件目录
manage.py - Django 项目管理脚本
2. 前端部分 (frontend/)
src/ - 源代码目录
api/ - API 接口调用
axios.ts - Axios 请求配置
index.ts - API 函数定义
assets/ - 静态资源文件
components/ - 可复用组件
layout/ - 布局组件
Index.vue - 主布局组件，包含侧边栏和顶部导航
router/ - 路由配置
index.ts - 定义应用路由和导航守卫
store/ - Vuex 状态管理
index.ts - 状态管理配置
types/ - TypeScript 类型定义
views/ - 页面视图组件
Achievement/ - 成就管理页面
Blog/ - 博客管理相关页面
Dashboard.vue - 仪表盘页面
Education/ - 教育经历管理页面
Login.vue - 登录页面
NotFound.vue - 404 页面
Profile/ - 个人信息管理页面
Project/ - 项目管理页面
Setting/ - 系统设置页面
Skill/ - 技能管理页面
Visitor/ - 访客统计页面
Work/ - 工作经历管理页面
App.vue - 根组件
main.ts - 应用入口文件
配置文件
package.json - 项目依赖和脚本配置
tsconfig.json - TypeScript 配置
vite.config.ts - Vite 构建工具配置
index.html - HTML 入口文件
3. 根目录文件
create_personal_blog_db.sql - 数据库创建脚本，定义了系统所需的表结构
README.md - 项目说明文档
功能模块
博客管理：博客的增删改查、分类和标签管理
项目管理：个人项目的管理，包括 GitHub 项目信息
技能管理：个人技能的管理和展示
教育经历：学历信息管理
工作经历：职业经验管理
成就管理：个人成就记录
个人信息：基本个人资料管理
访客统计：网站访问数据分析和可视化
系统设置：系统配置和维护
技术栈
前端：Vue 3、TypeScript、Vuex、Vue Router、Element Plus、Axios、ECharts
后端：Django、Django REST Framework、MySQL
该系统提供了完整的个人博客后台管理功能，包括内容管理、数据统计和系统设置等，适合个人开发者用于管理自己的个人网站和展示个人信息。
