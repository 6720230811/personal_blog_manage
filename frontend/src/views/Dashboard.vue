<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>仪表盘</h2>
      <p>欢迎使用个人博客管理系统</p>
    </div>

    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>博客总数</span>
            </div>
          </template>
          <div class="card-content">
            <h1>{{ stats.blogCount || 0 }}</h1>
            <el-button type="primary" plain @click="router.push('/blog')">查看全部</el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>项目总数</span>
            </div>
          </template>
          <div class="card-content">
            <h1>{{ stats.projectCount || 0 }}</h1>
            <el-button type="success" plain @click="router.push('/project')">查看全部</el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>技能数量</span>
            </div>
          </template>
          <div class="card-content">
            <h1>{{ stats.skillCount || 0 }}</h1>
            <el-button type="warning" plain @click="router.push('/skill')">查看全部</el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>访问量</span>
            </div>
          </template>
          <div class="card-content">
            <h1>{{ stats.visitorCount || 0 }}</h1>
            <el-button type="info" plain @click="router.push('/visitor')">查看明细</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>最近博客</span>
              <el-button type="text" @click="router.push('/blog')">更多</el-button>
            </div>
          </template>
          <el-table :data="recentBlogs" style="width: 100%">
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="category" label="分类" width="120" />
            <el-table-column prop="created_at" label="创建时间" width="180" />
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>最近访客</span>
              <el-button type="text" @click="router.push('/visitor')">更多</el-button>
            </div>
          </template>
          <el-table :data="recentVisitors" style="width: 100%">
            <el-table-column prop="ip_address" label="IP地址" width="120" />
            <el-table-column prop="page_url" label="访问页面" />
            <el-table-column prop="visit_time" label="访问时间" width="180" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getBlogList } from '@/api'
import { getProjectList } from '@/api'
import { getSkillList } from '@/api'
import { getVisitorList } from '@/api'

// 基本数据类型接口
interface Blog {
  id: number;
  title: string;
  category: string;
  created_at: string;
  [key: string]: any;
}

interface Visitor {
  id: number;
  ip_address: string;
  page_url: string;
  visit_time: string;
  [key: string]: any;
}

export default defineComponent({
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    
    const stats = reactive({
      blogCount: 0,
      projectCount: 0,
      skillCount: 0,
      visitorCount: 0
    })
    
    const recentBlogs = reactive<Blog[]>([])
    const recentVisitors = reactive<Visitor[]>([])
    
    const fetchDashboardData = async () => {
      try {
        // 获取博客列表
        const blogRes = await getBlogList() as any
        if (blogRes && Array.isArray(blogRes.results)) {
          stats.blogCount = blogRes.count || blogRes.results.length
          recentBlogs.push(...blogRes.results.slice(0, 5))
        }
        
        // 获取项目列表
        const projectRes = await getProjectList() as any
        if (projectRes && Array.isArray(projectRes.results)) {
          stats.projectCount = projectRes.count || projectRes.results.length
        }
        
        // 获取技能列表
        const skillRes = await getSkillList() as any
        if (skillRes && Array.isArray(skillRes.results)) {
          stats.skillCount = skillRes.count || skillRes.results.length
        }
        
        // 获取访客列表
        const visitorRes = await getVisitorList() as any
        if (visitorRes && Array.isArray(visitorRes.results)) {
          stats.visitorCount = visitorRes.count || visitorRes.results.length
          recentVisitors.push(...visitorRes.results.slice(0, 5))
        }
      } catch (error) {
        console.error('获取仪表盘数据失败:', error)
      }
    }
    
    onMounted(() => {
      fetchDashboardData()
    })
    
    return {
      router,
      stats,
      recentBlogs,
      recentVisitors
    }
  }
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-header {
  margin-bottom: 20px;
}

.dashboard-header h2 {
  margin: 0;
  margin-bottom: 10px;
}

.dashboard-header p {
  color: #606266;
  margin: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  text-align: center;
  padding: 10px 0;
}

.card-content h1 {
  font-size: 32px;
  margin-bottom: 20px;
  color: #409EFF;
}

.mt-20 {
  margin-top: 20px;
}
</style> 