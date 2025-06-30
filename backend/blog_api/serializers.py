from rest_framework import serializers  # 导入REST框架的序列化器模块
from .models import (  # 从models.py导入所有模型
    BlogOwner, WorkExperience, Education, Achievement,
    Skill, Projects, ProjectTags, ProjectTagMapping,
    Blogs, BlogTags, BlogTagMapping, ChatMessages,
    Visitors, SystemSettings
)

class BlogOwnerSerializer(serializers.ModelSerializer):  # 博客所有者序列化器类
    class Meta:  # 元数据类
        model = BlogOwner  # 关联的模型
        fields = ['id', 'username', 'email', 'avatar_url', 'github_url', 'github_username', 
                 'bio', 'country', 'city', 'identity', 'last_login', 'phone', 'address', 'birthday']  # 明确指定要包含的字段
        extra_kwargs = {'password': {'write_only': True}}  # 额外参数，密码字段只写不读

class WorkExperienceSerializer(serializers.ModelSerializer):  # 工作经验序列化器类
    class Meta:  # 元数据类
        model = WorkExperience  # 关联的模型
        fields = '__all__'  # 包含所有字段

class EducationSerializer(serializers.ModelSerializer):  # 教育经历序列化器类
    class Meta:  # 元数据类
        model = Education  # 关联的模型
        fields = '__all__'  # 包含所有字段

class AchievementSerializer(serializers.ModelSerializer):  # 成就序列化器类
    class Meta:  # 元数据类
        model = Achievement  # 关联的模型
        fields = '__all__'  # 包含所有字段

class SkillSerializer(serializers.ModelSerializer):  # 技能序列化器类
    class Meta:  # 元数据类
        model = Skill  # 关联的模型
        fields = '__all__'  # 包含所有字段

class ProjectTagsSerializer(serializers.ModelSerializer):  # 项目标签序列化器类
    class Meta:  # 元数据类
        model = ProjectTags  # 关联的模型
        fields = '__all__'  # 包含所有字段

class ProjectsSerializer(serializers.ModelSerializer):  # 项目序列化器类
    tags = serializers.SerializerMethodField()  # 自定义方法获取标签字段
    
    class Meta:  # 元数据类
        model = Projects  # 关联的模型
        fields = '__all__'  # 包含所有字段
        
    def get_tags(self, obj):  # 获取标签的方法
        try:
            # 使用原始SQL查询，避免ORM字段映射问题
            from django.db import connection
            cursor = connection.cursor()
            
            # 检查是否有映射数据 - 使用小写表名
            cursor.execute("SELECT COUNT(*) FROM projecttag_mapping WHERE project_id = %s", [obj.id])
            count = cursor.fetchone()[0]
            
            if count > 0:
                # 获取标签数据 - 使用小写表名
                cursor.execute(
                    "SELECT pt.id, pt.name, pt.description, pt.count FROM projecttags pt "
                    "JOIN projecttag_mapping ptm ON pt.id = ptm.tag_id "
                    "WHERE ptm.project_id = %s", [obj.id]
                )
                tags_data = []
                for row in cursor.fetchall():
                    tags_data.append({
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'count': row[3]
                    })
                return tags_data
            else:
                return []
        except Exception as e:
            print(f"获取项目标签时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []  # 发生错误时返回空列表

class ProjectTagMappingSerializer(serializers.ModelSerializer):  # 项目标签映射序列化器类
    class Meta:  # 元数据类
        model = ProjectTagMapping  # 关联的模型
        fields = '__all__'  # 包含所有字段

class ProjectDetailSerializer(serializers.ModelSerializer):  # 项目详情序列化器类，包含标签信息
    tags = serializers.SerializerMethodField()  # 自定义方法获取标签字段

    class Meta:  # 元数据类
        model = Projects  # 关联的模型
        fields = '__all__'  # 包含所有字段

    def get_tags(self, obj):  # 获取标签的方法
        try:
            # 使用原始SQL查询，避免ORM字段映射问题
            from django.db import connection
            cursor = connection.cursor()
            
            # 检查是否有映射数据 - 使用小写表名
            cursor.execute("SELECT COUNT(*) FROM projecttag_mapping WHERE project_id = %s", [obj.id])
            count = cursor.fetchone()[0]
            print(f"项目ID={obj.id}的标签映射数量: {count}")
            
            if count > 0:
                # 获取标签数据 - 使用小写表名
                cursor.execute(
                    "SELECT pt.id, pt.name, pt.description, pt.count FROM projecttags pt "
                    "JOIN projecttag_mapping ptm ON pt.id = ptm.tag_id "
                    "WHERE ptm.project_id = %s", [obj.id]
                )
                tags_data = []
                for row in cursor.fetchall():
                    tags_data.append({
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'count': row[3]
                    })
                print(f"SQL查询返回 {len(tags_data)} 个标签: {tags_data}")
                return tags_data
            else:
                print("该项目没有关联的标签")
                return []
        except Exception as e:
            print(f"获取项目标签时出错: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []  # 发生错误时返回空列表

class BlogTagsSerializer(serializers.ModelSerializer):  # 博客标签序列化器类
    class Meta:  # 元数据类
        model = BlogTags  # 关联的模型
        fields = '__all__'  # 包含所有字段

class BlogsSerializer(serializers.ModelSerializer):  # 博客序列化器类
    class Meta:  # 元数据类
        model = Blogs  # 关联的模型
        fields = '__all__'  # 包含所有字段

class BlogTagMappingSerializer(serializers.ModelSerializer):  # 博客标签映射序列化器类
    class Meta:  # 元数据类
        model = BlogTagMapping  # 关联的模型
        fields = '__all__'  # 包含所有字段

class BlogDetailSerializer(serializers.ModelSerializer):  # 博客详情序列化器类，包含标签信息
    tags = serializers.SerializerMethodField()  # 自定义方法获取标签字段

    class Meta:  # 元数据类
        model = Blogs  # 关联的模型
        fields = '__all__'  # 包含所有字段

    def get_tags(self, obj):  # 获取标签的方法
        tag_mappings = BlogTagMapping.objects.filter(blog=obj)  # 过滤出与当前博客相关的标签映射
        tags = [mapping.tag for mapping in tag_mappings]  # 提取所有标签对象
        return BlogTagsSerializer(tags, many=True).data  # 序列化标签列表并返回

class ChatMessagesSerializer(serializers.ModelSerializer):  # 聊天消息序列化器类
    class Meta:  # 元数据类
        model = ChatMessages  # 关联的模型
        fields = '__all__'  # 包含所有字段

class VisitorsSerializer(serializers.ModelSerializer):  # 访客序列化器类
    class Meta:  # 元数据类
        model = Visitors  # 关联的模型
        fields = '__all__'  # 包含所有字段

class SystemSettingsSerializer(serializers.ModelSerializer):  # 系统设置序列化器类
    class Meta:  # 元数据类
        model = SystemSettings  # 关联的模型
        fields = '__all__'  # 包含所有字段 