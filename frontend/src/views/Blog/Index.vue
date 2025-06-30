<template>
  <div class="blog-list-container">
    <div class="page-header">
      <h2>博客列表</h2>
      <el-button type="primary" @click="router.push('/blog/add')">添加博客</el-button>
    </div>

    <el-card>
      <div class="filter-container">
        <el-form :inline="true" :model="listQuery" class="form-inline">
          <el-form-item label="标题">
            <el-input v-model="listQuery.search" placeholder="博客标题" clearable />
          </el-form-item>
          <el-form-item label="分类">
            <el-select v-model="listQuery.category" placeholder="选择分类" clearable teleported :popper-options="{ strategy: 'fixed' }" popper-class="blog-select-dropdown">
              <el-option v-for="category in categories" :key="category" :label="category" :value="category" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="listQuery.published" placeholder="发布状态" clearable teleported :popper-options="{ strategy: 'fixed' }" popper-class="blog-select-dropdown">
              <el-option label="已发布" :value="true" />
              <el-option label="草稿" :value="false" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="getList">查询</el-button>
            <el-button @click="resetQuery">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table
        v-loading="listLoading"
        :data="list"
        element-loading-text="加载中..."
        border
        fit
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" align="center" width="80" />
        <el-table-column prop="title" label="标题" min-width="150" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="views_count" label="浏览量" align="center" width="100" />
        
        <el-table-column label="发布状态" align="center" width="100">
          <template #default="{ row }">
            <el-tag :type="row.published ? 'success' : 'info'">
              {{ row.published ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="推荐" align="center" width="80">
          <template #default="{ row }">
            <el-tag :type="row.featured ? 'danger' : 'info'">
              {{ row.featured ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="创建时间" width="160" />
        
        <el-table-column label="操作" align="center" width="250">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button 
              :type="row.published ? 'warning' : 'success'" 
              size="small" 
              @click="handlePublish(row)"
            >
              {{ row.published ? '下架' : '发布' }}
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          v-model:page-size="listQuery.pageSize"
          v-model:current-page="listQuery.page"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getBlogList, updateBlog, deleteBlog } from '@/api'

export default defineComponent({
  name: 'BlogList',
  setup() {
    const router = useRouter()
    const list = ref<any[]>([])
    const total = ref(0)
    const listLoading = ref(false)
    const categories = ref<string[]>([])
    
    const listQuery = reactive({
      page: 1,
      pageSize: 10,
      search: '',
      category: '',
      published: null as boolean | null
    })
    
    const getList = async () => {
      listLoading.value = true
      try {
        const params = {
          page: listQuery.page,
          page_size: listQuery.pageSize,
          search: listQuery.search,
          category: listQuery.category,
          published: listQuery.published
        }
        
        const res = await getBlogList(params) as any
        
        if (res && res.results) {
          list.value = res.results
          total.value = res.count || res.results.length
          
          // 提取分类列表
          const categorySet = new Set<string>()
          res.results.forEach((item: any) => {
            if (item.category) {
              categorySet.add(item.category)
            }
          })
          categories.value = Array.from(categorySet)
        }
      } catch (error) {
        ElMessage.error('获取博客列表失败')
        console.error('获取博客列表失败:', error)
      } finally {
        listLoading.value = false
      }
    }
    
    const resetQuery = () => {
      listQuery.page = 1
      listQuery.search = ''
      listQuery.category = ''
      listQuery.published = null
      getList()
    }
    
    const handleSizeChange = (val: number) => {
      listQuery.pageSize = val
      getList()
    }
    
    const handleCurrentChange = (val: number) => {
      listQuery.page = val
      getList()
    }
    
    const handleEdit = (row: any) => {
      console.log('编辑博客:', row)
      router.push(`/blog/edit/${row.id}`)
    }
    
    const handlePublish = async (row: any) => {
      try {
        const updatedStatus = !row.published
        const updatedData = { 
          published: updatedStatus,
          published_at: updatedStatus ? new Date().toISOString() : null
        }
        await updateBlog(row.id, updatedData)
        row.published = updatedStatus
        ElMessage.success(`博客已${updatedStatus ? '发布' : '下架'}`)
      } catch (error) {
        ElMessage.error(`操作失败`)
        console.error('发布状态更新失败:', error)
      }
    }
    
    const handleDelete = (row: any) => {
      ElMessageBox.confirm('确定要删除这篇博客吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteBlog(row.id)
          ElMessage.success('博客已删除')
          getList()
        } catch (error) {
          ElMessage.error('删除失败')
          console.error('删除博客失败:', error)
        }
      }).catch(() => {
        // 取消删除
      })
    }
    
    onMounted(() => {
      getList()
    })
    
    return {
      router,
      list,
      total,
      listLoading,
      listQuery,
      categories,
      getList,
      resetQuery,
      handleSizeChange,
      handleCurrentChange,
      handleEdit,
      handlePublish,
      handleDelete
    }
  }
})
</script>

<style scoped>
.blog-list-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.filter-container {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

/* 调整表单项的样式 */
:deep(.el-form-item) {
  margin-right: 15px;
}

/* 调整下拉框的宽度 */
:deep(.el-select) {
  width: 180px;
}
</style>

<style>
/* 全局样式，确保下拉菜单显示在最上层 */
.blog-select-dropdown {
  z-index: 9999 !important;
  min-width: 180px !important;
}

.el-select__popper {
  z-index: 9999 !important;
  min-width: 180px !important;
}
</style> 