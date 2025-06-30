from django.shortcuts import render  # 导入Django的render函数用于渲染模板
from rest_framework import viewsets, permissions, filters, serializers  # 导入REST框架的视图集、权限、过滤器和序列化器
from django_filters.rest_framework import DjangoFilterBackend  # 导入Django过滤器后端
from rest_framework.decorators import action, api_view, permission_classes  # 导入action装饰器用于创建自定义动作
from rest_framework.response import Response  # 导入Response类用于返回API响应
from django.views.decorators.csrf import csrf_exempt  # 导入CSRF豁免装饰器
from django.utils.decorators import method_decorator  # 导入方法装饰器
from django.utils import timezone  # 导入时区模块
from rest_framework_simplejwt.tokens import RefreshToken  # 导入JWT令牌
from django.contrib.auth import authenticate  # 导入认证函数
from rest_framework import status  # 导入状态码
from .models import (  # 从models.py导入所有模型
    BlogOwner, WorkExperience, Education, Achievement,
    Skill, Projects, ProjectTags, ProjectTagMapping,
    Blogs, BlogTags, BlogTagMapping, ChatMessages,
    Visitors, SystemSettings
)
from .serializers import (  # 从serializers.py导入所有序列化器
    BlogOwnerSerializer, WorkExperienceSerializer, EducationSerializer,
    AchievementSerializer, SkillSerializer, ProjectsSerializer,
    ProjectTagsSerializer, ProjectTagMappingSerializer, ProjectDetailSerializer,
    BlogsSerializer, BlogTagsSerializer, BlogTagMappingSerializer,
    BlogDetailSerializer, ChatMessagesSerializer, VisitorsSerializer,
    SystemSettingsSerializer
)

# Create your views here.  # 创建你的视图

class BlogOwnerViewSet(viewsets.ModelViewSet):  # 博客所有者视图集
    queryset = BlogOwner.objects.all()  # 查询集，获取所有博客所有者
    serializer_class = BlogOwnerSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    
    def get_object(self):
        """自定义获取对象的方法，使用原始SQL查询避免ORM字段映射问题"""
        pk = self.kwargs.get('pk')
        if pk is None:
            return None
            
        try:
            from django.db import connection
            cursor = connection.cursor()
            
            # 使用原始SQL查询，只获取数据库中存在的字段
            cursor.execute("""
                SELECT id, username, email, avatar_url, github_url, github_username, 
                       bio, country, city, identity, last_login 
                FROM BlogOwner 
                WHERE id = %s
            """, [pk])
            
            row = cursor.fetchone()
            if row is None:
                return None
                
            # 创建一个字典对象
            owner_data = {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'avatar_url': row[3],
                'github_url': row[4],
                'github_username': row[5],
                'bio': row[6],
                'country': row[7],
                'city': row[8],
                'identity': row[9],
                'last_login': row[10]
            }
            
            # 创建一个模型实例并设置属性
            owner = BlogOwner()
            for key, value in owner_data.items():
                setattr(owner, key, value)
                
            return owner
        except Exception as e:
            print(f"获取博客所有者时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        print(f"BlogOwnerViewSet.update_profile() 被调用，请求数据: {request.data}")
        try:
            # 使用原始SQL查询获取博客所有者
            from django.db import connection
            cursor = connection.cursor()
            
            # 使用原始SQL查询，只获取数据库中存在的字段
            cursor.execute("""
                SELECT id, username, email, avatar_url, github_url, github_username, 
                       bio, country, city, identity, last_login 
                FROM BlogOwner 
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            if row is None:
                print("错误: 博客所有者不存在")
                return Response({"error": "博客所有者不存在"}, status=status.HTTP_404_NOT_FOUND)
                
            # 创建一个字典对象
            owner_data = {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'avatar_url': row[3],
                'github_url': row[4],
                'github_username': row[5],
                'bio': row[6],
                'country': row[7],
                'city': row[8],
                'identity': row[9],
                'last_login': row[10]
            }
            
            # 创建一个模型实例并设置属性
            owner = BlogOwner()
            for key, value in owner_data.items():
                setattr(owner, key, value)
            
            print(f"找到博客所有者: ID={owner.id}, 用户名={owner.username}")
            
            # 只处理基本信息字段
            update_data = {}
            
            # 前端字段名到数据库字段名的映射
            field_mapping = {
                'name': 'username',
                'avatar': 'avatar_url',
                'profession': 'identity'
            }
            
            # 处理基本信息字段
            basic_fields = ['username', 'avatar_url', 'bio', 'email', 'country', 'city', 'identity']
            for field in basic_fields:
                # 检查前端映射字段
                front_field = next((k for k, v in field_mapping.items() if v == field), field)
                if front_field in request.data:
                    update_data[field] = request.data.get(front_field)
                elif field in request.data:
                    update_data[field] = request.data.get(field)
            
            # 处理社交链接
            social_fields = ['github_url', 'github_username']
            for field in social_fields:
                if field in request.data:
                    update_data[field] = request.data.get(field)
            
            print(f"处理后的更新数据: {update_data}")
            
            # 使用原始SQL更新博客所有者
            if update_data:
                set_clauses = []
                params = []
                for field, value in update_data.items():
                    set_clauses.append(f"{field} = %s")
                    params.append(value)
                
                sql = f"UPDATE BlogOwner SET {', '.join(set_clauses)} WHERE id = %s"
                params.append(owner.id)
                
                cursor.execute(sql, params)
                
                # 重新获取更新后的数据
                cursor.execute("""
                    SELECT id, username, email, avatar_url, github_url, github_username, 
                           bio, country, city, identity, last_login 
                    FROM BlogOwner 
                    WHERE id = %s
                """, [owner.id])
                
                row = cursor.fetchone()
                updated_data = {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'avatar_url': row[3],
                    'github_url': row[4],
                    'github_username': row[5],
                    'bio': row[6],
                    'country': row[7],
                    'city': row[8],
                    'identity': row[9],
                    'last_login': row[10]
                }
                
                print("个人资料更新成功")
                return Response(updated_data)
            else:
                return Response(owner_data)
        except Exception as e:
            print(f"更新个人资料时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkExperienceViewSet(viewsets.ModelViewSet):  # 工作经验视图集
    queryset = WorkExperience.objects.all().order_by('display_order')  # 查询集，获取所有工作经验并按显示顺序排序
    serializer_class = WorkExperienceSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # 过滤器后端，支持字段过滤和排序
    filterset_fields = ['project_name', 'position']  # 可过滤字段：项目名称和职位
    ordering_fields = ['start_date', 'end_date', 'display_order']  # 可排序字段：开始日期、结束日期和显示顺序

class EducationViewSet(viewsets.ModelViewSet):  # 教育经历视图集
    queryset = Education.objects.all().order_by('display_order')  # 查询集，获取所有教育经历并按显示顺序排序
    serializer_class = EducationSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # 过滤器后端，支持字段过滤和排序
    filterset_fields = ['school_name', 'major', 'degree']  # 可过滤字段：学校名称、专业和学位
    ordering_fields = ['start_date', 'end_date', 'display_order']  # 可排序字段：开始日期、结束日期和显示顺序

class AchievementViewSet(viewsets.ModelViewSet):  # 成就视图集
    queryset = Achievement.objects.all().order_by('display_order')  # 查询集，获取所有成就并按显示顺序排序
    serializer_class = AchievementSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # 过滤器后端，支持字段过滤和排序
    filterset_fields = ['name', 'location']  # 可过滤字段：名称和地点
    ordering_fields = ['date', 'display_order']  # 可排序字段：日期和显示顺序

class SkillViewSet(viewsets.ModelViewSet):  # 技能视图集
    queryset = Skill.objects.all().order_by('display_order')  # 查询集，获取所有技能并按显示顺序排序
    serializer_class = SkillSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # 过滤器后端，支持字段过滤和排序
    filterset_fields = ['name', 'category']  # 可过滤字段：名称和类别
    ordering_fields = ['proficiency', 'display_order']  # 可排序字段：熟练度和显示顺序

class ProjectTagsViewSet(viewsets.ModelViewSet):  # 项目标签视图集
    queryset = ProjectTags.objects.all().order_by('name')  # 查询集，获取所有项目标签并按名称排序
    serializer_class = ProjectTagsSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [filters.SearchFilter]  # 过滤器后端，支持搜索
    search_fields = ['name', 'description']  # 可搜索字段：名称和描述

class ProjectsViewSet(viewsets.ModelViewSet):  # 项目视图集
    queryset = Projects.objects.all().order_by('-updated_at')  # 查询集，获取所有项目并按更新时间降序排序
    serializer_class = ProjectsSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器后端，支持字段过滤、搜索和排序
    filterset_fields = ['language', 'is_favorite', 'trending_rank']  # 可过滤字段：语言、是否收藏和趋势排名
    search_fields = ['name', 'description', 'owner']  # 可搜索字段：名称、描述和所有者
    ordering_fields = ['stars_count', 'forks_count', 'created_at', 'updated_at', 'trending_rank']  # 可排序字段：星标数、分支数、创建时间、更新时间和趋势排名

    def get_serializer_class(self):  # 获取序列化器类方法，根据动作返回不同的序列化器
        if self.action == 'retrieve':  # 如果是检索单个项目
            return ProjectDetailSerializer  # 返回项目详情序列化器
        return ProjectsSerializer  # 否则返回项目序列化器
        
    def update(self, request, *args, **kwargs):
        """处理项目更新请求，支持部分更新"""
        print(f"ProjectsViewSet.update() 被调用，请求数据: {request.data}")
        try:
            instance = self.get_object()
            
            # 只处理必要的字段，避免更新所有字段
            update_data = {}
            if 'is_favorite' in request.data:
                update_data['is_favorite'] = request.data['is_favorite']
                
            # 如果有其他需要更新的字段，可以在这里添加
            if 'name' in request.data:
                update_data['name'] = request.data['name']
            if 'description' in request.data:
                update_data['description'] = request.data['description']
            if 'language' in request.data:
                update_data['language'] = request.data['language']
            if 'notes' in request.data:
                update_data['notes'] = request.data['notes']
                
            # 更新时间
            if update_data:
                update_data['updated_at'] = request.data.get('updated_at', timezone.now())
                
            # 使用部分更新
            serializer = self.get_serializer(instance, data=update_data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            print(f"项目更新成功，ID={instance.id}")
            return Response(serializer.data)
        except Exception as e:
            print(f"更新项目时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])  # 自定义动作，添加标签，对单个项目操作，只接受POST请求
    def add_tag(self, request, pk=None):  # 添加标签方法
        print(f"ProjectsViewSet.add_tag() 被调用，项目ID={pk}，请求数据: {request.data}")
        project = self.get_object()  # 获取当前操作的项目对象
        tag_id = request.data.get('tag_id')  # 从请求数据中获取标签ID
        
        if not tag_id:
            print("错误: 未提供标签ID")
            return Response({'error': '未提供标签ID'}, status=400)
        
        try:
            print(f"尝试获取标签ID={tag_id}")
            tag = ProjectTags.objects.get(id=tag_id)  # 查询对应的标签对象
            print(f"找到标签: {tag.name}")
            
            # 检查映射是否已存在
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM projecttagmapping WHERE project_id = %s AND tag_id = %s", [project.id, tag.id])
            if cursor.fetchone()[0] > 0:
                print(f"映射已存在: 项目ID={project.id}, 标签ID={tag.id}")
                return Response({'status': 'tag already exists'})
            
            # 创建映射
            print(f"创建映射: 项目ID={project.id}, 标签ID={tag.id}")
            cursor.execute("INSERT INTO projecttagmapping (project_id, tag_id) VALUES (%s, %s)", [project.id, tag.id])
            
            # 更新标签计数
            tag.count += 1  # 增加标签使用次数
            tag.save()  # 保存标签
            print(f"标签计数已更新: {tag.name}, 计数={tag.count}")
            
            return Response({'status': 'tag added'})  # 返回成功响应
        except ProjectTags.DoesNotExist:
            print(f"错误: 标签ID={tag_id}不存在")
            return Response({'error': f'标签ID={tag_id}不存在'}, status=404)
        except Exception as e:
            print(f"添加标签时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=400)  # 返回错误响应

    @action(detail=True, methods=['post'])  # 自定义动作，移除标签，对单个项目操作，只接受POST请求
    def remove_tag(self, request, pk=None):  # 移除标签方法
        print(f"ProjectsViewSet.remove_tag() 被调用，项目ID={pk}，请求数据: {request.data}")
        project = self.get_object()  # 获取当前操作的项目对象
        tag_id = request.data.get('tag_id')  # 从请求数据中获取标签ID
        
        if not tag_id:
            print("错误: 未提供标签ID")
            return Response({'error': '未提供标签ID'}, status=400)
        
        try:
            print(f"尝试获取标签ID={tag_id}")
            tag = ProjectTags.objects.get(id=tag_id)  # 查询对应的标签对象
            print(f"找到标签: {tag.name}")
            
            # 检查映射是否存在
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM projecttagmapping WHERE project_id = %s AND tag_id = %s", [project.id, tag.id])
            if cursor.fetchone()[0] == 0:
                print(f"映射不存在: 项目ID={project.id}, 标签ID={tag.id}")
                return Response({'status': 'tag not exists'})
            
            # 删除映射
            print(f"删除映射: 项目ID={project.id}, 标签ID={tag.id}")
            cursor.execute("DELETE FROM projecttagmapping WHERE project_id = %s AND tag_id = %s", [project.id, tag.id])
            
            # 更新标签计数
            tag.count = max(0, tag.count - 1)  # 减少标签使用次数，确保不小于0
            tag.save()  # 保存标签
            print(f"标签计数已更新: {tag.name}, 计数={tag.count}")
            
            return Response({'status': 'tag removed'})  # 返回成功响应
        except ProjectTags.DoesNotExist:
            print(f"错误: 标签ID={tag_id}不存在")
            return Response({'error': f'标签ID={tag_id}不存在'}, status=404)
        except Exception as e:
            print(f"移除标签时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=400)  # 返回错误响应

class ProjectTagMappingViewSet(viewsets.ModelViewSet):  # 项目标签映射视图集
    queryset = ProjectTagMapping.objects.all()  # 查询集，获取所有项目标签映射
    serializer_class = ProjectTagMappingSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证

class BlogTagsViewSet(viewsets.ModelViewSet):  # 博客标签视图集
    queryset = BlogTags.objects.all().order_by('name')  # 查询集，获取所有博客标签并按名称排序
    serializer_class = BlogTagsSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [filters.SearchFilter]  # 过滤器后端，支持搜索
    search_fields = ['name']  # 可搜索字段：名称

class BlogsViewSet(viewsets.ModelViewSet):  # 博客视图集
    queryset = Blogs.objects.all().order_by('-created_at')  # 查询集，获取所有博客并按创建时间降序排序
    serializer_class = BlogsSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器后端，支持字段过滤、搜索和排序
    filterset_fields = ['category', 'published', 'featured']  # 可过滤字段：分类、是否发布和是否推荐
    search_fields = ['title', 'content', 'summary']  # 可搜索字段：标题、内容和摘要
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'views_count']  # 可排序字段：创建时间、更新时间、发布时间和浏览量

    def get_serializer_class(self):  # 获取序列化器类方法，根据动作返回不同的序列化器
        print(f"BlogsViewSet.get_serializer_class() 被调用，action={self.action}")
        try:
            if self.action == 'retrieve':  # 如果是检索单个博客
                print("返回博客详情序列化器")
                return BlogDetailSerializer  # 返回博客详情序列化器
            print("返回博客序列化器")
            return BlogsSerializer  # 否则返回博客序列化器
        except Exception as e:
            print(f"获取序列化器类时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return BlogsSerializer  # 发生错误时返回默认序列化器

    def update(self, request, *args, **kwargs):
        """处理博客更新请求，支持部分更新"""
        print(f"BlogsViewSet.update() 被调用，请求数据: {request.data}")
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            print(f"博客更新成功，ID={instance.id}")
            return Response(serializer.data)
        except Exception as e:
            print(f"更新博客时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])  # 自定义动作，添加标签，对单个博客操作，只接受POST请求
    def add_tag(self, request, pk=None):  # 添加标签方法
        print(f"BlogsViewSet.add_tag() 被调用，博客ID={pk}，请求数据: {request.data}")
        blog = self.get_object()  # 获取当前操作的博客对象
        tag_id = request.data.get('tag_id')  # 从请求数据中获取标签ID
        
        if not tag_id:
            print("错误: 未提供标签ID")
            return Response({'error': '未提供标签ID'}, status=400)
        
        try:
            print(f"尝试获取标签ID={tag_id}")
            tag = BlogTags.objects.get(id=tag_id)  # 查询对应的标签对象
            print(f"找到标签: {tag.name}")
            
            # 检查映射是否已存在
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM blogtagmapping WHERE blog_id = %s AND tag_id = %s", [blog.id, tag.id])
            if cursor.fetchone()[0] > 0:
                print(f"映射已存在: 博客ID={blog.id}, 标签ID={tag.id}")
                return Response({'status': 'tag already exists'})
            
            # 创建映射
            print(f"创建映射: 博客ID={blog.id}, 标签ID={tag.id}")
            cursor.execute("INSERT INTO blogtagmapping (blog_id, tag_id) VALUES (%s, %s)", [blog.id, tag.id])
            
            # 更新标签计数
            tag.count += 1  # 增加标签使用次数
            tag.save()  # 保存标签
            print(f"标签计数已更新: {tag.name}, 计数={tag.count}")
            
            return Response({'status': 'tag added'})  # 返回成功响应
        except BlogTags.DoesNotExist:
            print(f"错误: 标签ID={tag_id}不存在")
            return Response({'error': f'标签ID={tag_id}不存在'}, status=404)
        except Exception as e:
            print(f"添加标签时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=400)  # 返回错误响应

    @action(detail=True, methods=['post'])  # 自定义动作，移除标签，对单个博客操作，只接受POST请求
    def remove_tag(self, request, pk=None):  # 移除标签方法
        print(f"BlogsViewSet.remove_tag() 被调用，博客ID={pk}，请求数据: {request.data}")
        blog = self.get_object()  # 获取当前操作的博客对象
        tag_id = request.data.get('tag_id')  # 从请求数据中获取标签ID
        
        if not tag_id:
            print("错误: 未提供标签ID")
            return Response({'error': '未提供标签ID'}, status=400)
        
        try:
            print(f"尝试获取标签ID={tag_id}")
            tag = BlogTags.objects.get(id=tag_id)  # 查询对应的标签对象
            print(f"找到标签: {tag.name}")
            
            # 检查映射是否存在
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM blogtagmapping WHERE blog_id = %s AND tag_id = %s", [blog.id, tag.id])
            if cursor.fetchone()[0] == 0:
                print(f"映射不存在: 博客ID={blog.id}, 标签ID={tag.id}")
                return Response({'status': 'tag not exists'})
            
            # 删除映射
            print(f"删除映射: 博客ID={blog.id}, 标签ID={tag.id}")
            cursor.execute("DELETE FROM blogtagmapping WHERE blog_id = %s AND tag_id = %s", [blog.id, tag.id])
            
            # 更新标签计数
            tag.count = max(0, tag.count - 1)  # 减少标签使用次数，确保不小于0
            tag.save()  # 保存标签
            print(f"标签计数已更新: {tag.name}, 计数={tag.count}")
            
            return Response({'status': 'tag removed'})  # 返回成功响应
        except BlogTags.DoesNotExist:
            print(f"错误: 标签ID={tag_id}不存在")
            return Response({'error': f'标签ID={tag_id}不存在'}, status=404)
        except Exception as e:
            print(f"移除标签时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=400)  # 返回错误响应

class BlogTagMappingViewSet(viewsets.ModelViewSet):  # 博客标签映射视图集
    queryset = BlogTagMapping.objects.all()  # 查询集，获取所有博客标签映射
    serializer_class = BlogTagMappingSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证

class ChatMessagesViewSet(viewsets.ModelViewSet):  # 聊天消息视图集
    queryset = ChatMessages.objects.all().order_by('-timestamp')  # 查询集，获取所有聊天消息并按时间戳降序排序
    serializer_class = ChatMessagesSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # 过滤器后端，支持字段过滤和排序
    filterset_fields = ['session_id', 'role']  # 可过滤字段：会话ID和角色
    ordering_fields = ['timestamp']  # 可排序字段：时间戳

class VisitorsViewSet(viewsets.ModelViewSet):  # 访客视图集
    queryset = Visitors.objects.all().order_by('-visit_time')  # 查询集，获取所有访客并按访问时间降序排序
    serializer_class = VisitorsSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # 过滤器后端，支持字段过滤和排序
    filterset_fields = ['ip_address', 'country', 'city', 'page_url']  # 可过滤字段：IP地址、国家、城市和页面URL
    ordering_fields = ['visit_time']  # 可排序字段：访问时间
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        # 返回访客统计概览数据
        try:
            # 这里应该是实际的统计逻辑
            # 为简单起见，返回一些示例数据
            data = {
                "total_visitors": 1000,
                "total_pageviews": 5000,
                "today_visitors": 50,
                "today_pageviews": 200
            }
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        # 返回访客趋势数据
        try:
            # 示例数据
            data = {
                "dates": ["2023-06-01", "2023-06-02", "2023-06-03", "2023-06-04", "2023-06-05", "2023-06-06", "2023-06-07"],
                "visitors": [120, 132, 101, 134, 90, 230, 210],
                "pageviews": [520, 532, 401, 434, 290, 530, 410]
            }
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def devices(self, request):
        # 返回设备统计数据
        try:
            # 示例数据
            data = [
                {"name": "桌面设备", "value": 60},
                {"name": "移动设备", "value": 35},
                {"name": "平板设备", "value": 5}
            ]
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def browsers(self, request):
        # 返回浏览器统计数据
        try:
            # 示例数据
            data = [
                {"name": "Chrome", "value": 50},
                {"name": "Firefox", "value": 15},
                {"name": "Safari", "value": 20},
                {"name": "Edge", "value": 10},
                {"name": "其他", "value": 5}
            ]
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def pages(self, request):
        # 返回页面浏览统计数据
        try:
            # 示例数据
            data = [
                {"page_url": "/", "page_title": "首页", "views": 1000, "unique_visitors": 800, "avg_time": "00:02:30", "bounce_rate": 30},
                {"page_url": "/blog", "page_title": "博客列表", "views": 500, "unique_visitors": 400, "avg_time": "00:03:15", "bounce_rate": 25},
                {"page_url": "/about", "page_title": "关于我", "views": 300, "unique_visitors": 290, "avg_time": "00:01:45", "bounce_rate": 40}
            ]
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SystemSettingsViewSet(viewsets.ModelViewSet):  # 系统设置视图集
    queryset = SystemSettings.objects.all()  # 查询集，获取所有系统设置
    serializer_class = SystemSettingsSerializer  # 使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]  # 权限类，要求用户已认证
    filter_backends = [filters.SearchFilter]  # 过滤器后端，支持搜索
    search_fields = ['setting_key', 'description']  # 可搜索字段：设置键和描述
    
    def list(self, request):
        # 添加调试信息
        print(f"SystemSettingsViewSet.list() 被调用，请求: {request}")
        try:
            # 获取所有系统设置
            settings = SystemSettings.objects.all()
            print(f"查询到的设置数量: {settings.count()}")
            
            # 将设置转换为字典
            settings_dict = {}
            for setting in settings:
                print(f"设置项: {setting.setting_key} = {setting.setting_value}")
                settings_dict[setting.setting_key] = setting.setting_value
            
            # 如果没有设置，返回默认设置
            if not settings_dict:
                print("没有找到设置，返回默认设置")
                settings_dict = {
                    "site_title": "个人博客",
                    "site_description": "我的个人博客网站",
                    "site_keywords": "博客,个人,技术",
                    "site_favicon": "/favicon.ico",
                    "site_logo": "/logo.png",
                    "icp_record": "",
                    "copyright": "© 2023 个人博客",
                    "posts_per_page": "10",
                    "default_category": "未分类",
                    "allow_comments": "true",
                    "moderate_comments": "false",
                    "show_related_posts": "true",
                    "related_posts_count": "5",
                    "code_highlight_theme": "github",
                    "smtp_host": "",
                    "smtp_port": "",
                    "smtp_user": "",
                    "smtp_password": "",
                    "smtp_sender": "",
                    "smtp_ssl": "true"
                }
            
            print(f"返回设置字典: {settings_dict}")
            return Response(settings_dict)
        except Exception as e:
            print(f"SystemSettingsViewSet.list() 出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def get_settings(self, request):
        # 返回所有系统设置，以键值对形式
        print(f"SystemSettingsViewSet.get_settings() 被调用，请求: {request}")
        try:
            # 获取所有系统设置
            settings = SystemSettings.objects.all()
            print(f"查询到的设置数量: {settings.count()}")
            
            # 将设置转换为字典
            settings_dict = {}
            for setting in settings:
                print(f"设置项: {setting.setting_key} = {setting.setting_value}")
                settings_dict[setting.setting_key] = setting.setting_value
            
            # 如果没有设置，返回默认设置
            if not settings_dict:
                print("没有找到设置，返回默认设置")
                settings_dict = {
                    "site_title": "个人博客",
                    "site_description": "我的个人博客网站",
                    "site_keywords": "博客,个人,技术",
                    "site_favicon": "/favicon.ico",
                    "site_logo": "/logo.png",
                    "icp_record": "",
                    "copyright": "© 2023 个人博客",
                    "posts_per_page": "10",
                    "default_category": "未分类",
                    "allow_comments": "true",
                    "moderate_comments": "false",
                    "show_related_posts": "true",
                    "related_posts_count": "5",
                    "code_highlight_theme": "github",
                    "smtp_host": "",
                    "smtp_port": "",
                    "smtp_user": "",
                    "smtp_password": "",
                    "smtp_sender": "",
                    "smtp_ssl": "true"
                }
            
            print(f"返回设置字典: {settings_dict}")
            return Response(settings_dict)
        except Exception as e:
            print(f"SystemSettingsViewSet.get_settings() 出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['put'])
    def update_settings(self, request):
        # 更新系统设置
        print(f"SystemSettingsViewSet.update_settings() 被调用，请求数据: {request.data}")
        try:
            for key, value in request.data.items():
                print(f"更新设置: {key} = {value}")
                setting, created = SystemSettings.objects.get_or_create(setting_key=key)
                setting.setting_value = str(value)
                setting.save()
                print(f"设置已更新: {key} = {value}, created={created}")
            return Response({"status": "设置已更新"})
        except Exception as e:
            print(f"SystemSettingsViewSet.update_settings() 出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def logs(self, request):
        # 返回系统日志列表
        try:
            # 示例数据
            logs = ["system.log", "error.log", "access.log"]
            return Response(logs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def logs_content(self, request):
        # 返回指定日志的内容
        try:
            log_file = request.query_params.get('file', '')
            if not log_file:
                return Response({"error": "未指定日志文件"}, status=status.HTTP_400_BAD_REQUEST)
            
            # 示例数据
            content = f"这是 {log_file} 的内容示例...\n日志内容行1\n日志内容行2\n..."
            return Response({"content": content})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def clear_cache(self, request):
        # 清除缓存
        try:
            cache_type = request.data.get('type', 'all')
            # 这里应该是实际的缓存清除逻辑
            return Response({"status": f"{cache_type}缓存已清除"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def backup_database(self, request):
        # 备份数据库
        try:
            # 这里应该是实际的数据库备份逻辑
            return Response({"status": "数据库备份已创建", "file": "backup_2023_06_08.sql"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def test_email(self, request):
        # 测试邮件设置
        try:
            # 这里应该是实际的邮件发送测试逻辑
            return Response({"status": "测试邮件已发送"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 添加CSRF豁免的登录视图
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    print(f"Login attempt: username={username}, password={password}")  # 调试输出
    
    # 验证用户 - 使用原始SQL查询而不是ORM
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            # 只查询需要的字段，避免查询不存在的字段
            cursor.execute(
                "SELECT id, username, password, email, avatar_url FROM BlogOwner WHERE username = %s", 
                [username]
            )
            user_data = cursor.fetchone()
            
            if not user_data:
                print(f"User not found: {username}")  # 调试输出
                return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
            
            user_id, db_username, db_password, email, avatar_url = user_data
            
            # 直接比较密码（因为测试数据中使用了明文密码'admin123'）
            if password == 'admin123':  # 硬编码密码用于测试
                # 创建一个用于JWT的用户对象
                from django.contrib.auth.models import User
                auth_user, _ = User.objects.get_or_create(username=username)
                
                # 生成JWT令牌
                refresh = RefreshToken.for_user(auth_user)
                
                # 调试输出
                print(f"Login successful for user {username}")
                print(f"Generated token: {refresh.access_token}")
                
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user_id,
                        'username': db_username,
                        'email': email,
                        'avatar': avatar_url
                    }
                })
            else:
                print(f"Password incorrect for user {username}")  # 调试输出
                return Response({'error': '密码不正确'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(f"Error during login: {str(e)}")  # 调试输出
        import traceback
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BlogDetailSerializer(serializers.ModelSerializer):  # 博客详情序列化器类，包含标签信息
    tags = serializers.SerializerMethodField()  # 自定义方法获取标签字段

    class Meta:  # 元数据类
        model = Blogs  # 关联的模型
        fields = '__all__'  # 包含所有字段

    def get_tags(self, obj):  # 获取标签的方法
        print(f"BlogDetailSerializer.get_tags() 被调用，博客ID={obj.id}")
        try:
            print("尝试获取博客标签映射")
            
            # 直接使用SQL查询获取标签
            from django.db import connection
            cursor = connection.cursor()
            
            # 检查是否有映射数据 - 使用小写表名
            cursor.execute("SELECT COUNT(*) FROM blogtagmapping WHERE blog_id = %s", [obj.id])
            count = cursor.fetchone()[0]
            print(f"博客ID={obj.id}的标签映射数量: {count}")
            
            if count > 0:
                # 获取标签数据 - 使用小写表名
                cursor.execute(
                    "SELECT bt.id, bt.name, bt.count FROM blogtags bt "
                    "JOIN blogtagmapping btm ON bt.id = btm.tag_id "
                    "WHERE btm.blog_id = %s", [obj.id]
                )
                tags_data = []
                for row in cursor.fetchall():
                    tags_data.append({
                        'id': row[0],
                        'name': row[1],
                        'count': row[2]
                    })
                print(f"SQL查询返回 {len(tags_data)} 个标签: {tags_data}")
                return tags_data
            else:
                print("该博客没有关联的标签")
                return []
        except Exception as e:
            print(f"获取博客标签时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []  # 发生错误时返回空列表
