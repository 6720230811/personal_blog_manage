<template>
  <div class="project-list-container">
    <div class="page-header">
      <h2>项目管理</h2>
      <el-button type="primary" @click="handleAdd">添加项目</el-button>
    </div>

    <el-card>
      <div class="filter-container">
        <el-form :inline="true" :model="listQuery" class="form-inline">
          <el-form-item label="项目名称">
            <el-input v-model="listQuery.search" placeholder="项目名称" clearable />
          </el-form-item>
          <el-form-item label="语言">
            <el-select v-model="listQuery.language" placeholder="编程语言" clearable teleported :popper-options="{ strategy: 'fixed' }" popper-class="project-select-dropdown">
              <el-option v-for="lang in languages" :key="lang" :label="lang" :value="lang" />
            </el-select>
          </el-form-item>
          <el-form-item label="收藏">
            <el-select v-model="listQuery.is_favorite" placeholder="收藏状态" clearable teleported :popper-options="{ strategy: 'fixed' }" popper-class="project-select-dropdown">
              <el-option label="已收藏" :value="true" />
              <el-option label="未收藏" :value="false" />
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
        <el-table-column prop="name" label="项目名称" min-width="150" />
        <el-table-column prop="language" label="语言" width="100" />
        <el-table-column prop="stars_count" label="星标数" align="center" width="100" />
        <el-table-column prop="forks_count" label="Fork数" align="center" width="100" />
        
        <el-table-column label="收藏" align="center" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_favorite ? 'danger' : 'info'">
              {{ row.is_favorite ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="标签" min-width="150">
          <template #default="{ row }">
            <el-tag v-for="tag in row.tags" :key="tag.id" type="success" class="tag">{{ tag.name }}</el-tag>
            <span v-if="!row.tags || row.tags.length === 0">无标签</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="updated_at" label="更新时间" width="160" />
        
        <el-table-column label="操作" align="center" width="250">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button 
              :type="row.is_favorite ? 'warning' : 'success'" 
              size="small" 
              @click="handleToggleFavorite(row)"
            >
              {{ row.is_favorite ? '取消收藏' : '收藏' }}
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

    <!-- 项目表单对话框 -->
    <el-dialog 
      :title="projectForm.id ? '编辑项目' : '添加项目'" 
      v-model="dialogVisible" 
      width="600px"
      :close-on-click-modal="false"
      @closed="resetForm"
    >
      <el-form ref="projectFormRef" :model="projectForm" :rules="rules" label-width="100px">
        <el-form-item label="GitHub ID" prop="github_id">
          <el-input v-model="projectForm.github_id" placeholder="GitHub 仓库 ID" />
        </el-form-item>
        
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="projectForm.name" placeholder="项目名称" />
        </el-form-item>
        
        <el-form-item label="完整名称" prop="full_name">
          <el-input v-model="projectForm.full_name" placeholder="完整名称 (如 username/repo)" />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="projectForm.description" 
            type="textarea" 
            :rows="3"
            placeholder="项目描述" 
          />
        </el-form-item>
        
        <el-form-item label="项目URL" prop="url">
          <el-input v-model="projectForm.url" placeholder="项目URL" />
        </el-form-item>
        
        <el-form-item label="所有者" prop="owner">
          <el-input v-model="projectForm.owner" placeholder="仓库所有者" />
        </el-form-item>
        
        <el-form-item label="语言" prop="language">
          <el-input v-model="projectForm.language" placeholder="编程语言" />
        </el-form-item>
        
        <el-form-item label="收藏" prop="is_favorite">
          <el-switch v-model="projectForm.is_favorite" />
        </el-form-item>
        
        <el-form-item label="标签">
          <el-select
            v-model="selectedTags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请选择标签"
            teleported
            :popper-options="{ strategy: 'fixed' }"
            popper-class="project-select-dropdown"
          >
            <el-option
              v-for="tag in tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="备注" prop="notes">
          <el-input 
            v-model="projectForm.notes" 
            type="textarea" 
            :rows="3"
            placeholder="项目备注" 
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  getProjectList, 
  getProjectDetail, 
  createProject, 
  updateProject, 
  deleteProject,
  getProjectTagList, 
  addTagToProject, 
  removeTagFromProject 
} from '@/api'

export default defineComponent({
  name: 'ProjectList',
  setup() {
    const list = ref<any[]>([])
    const total = ref(0)
    const listLoading = ref(false)
    const languages = ref<string[]>([])
    const tags = ref<any[]>([])
    const selectedTags = ref<number[]>([])
    const dialogVisible = ref(false)
    const submitLoading = ref(false)
    
    const listQuery = reactive({
      page: 1,
      pageSize: 10,
      search: '',
      language: '',
      is_favorite: null as boolean | null
    })
    
    const projectForm = reactive({
      id: null as number | null,
      github_id: '',
      name: '',
      full_name: '',
      description: '',
      url: '',
      owner: '',
      language: '',
      is_favorite: false,
      notes: '',
      stars_count: 0,
      forks_count: 0,
      watchers_count: 0,
      open_issues_count: 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      fetched_at: new Date().toISOString()
    })
    
    const rules = {
      github_id: [{ required: true, message: '请输入GitHub ID', trigger: 'blur' }],
      name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
      full_name: [{ required: true, message: '请输入完整名称', trigger: 'blur' }],
      url: [{ required: true, message: '请输入项目URL', trigger: 'blur' }],
      owner: [{ required: true, message: '请输入所有者', trigger: 'blur' }]
    }
    
    const projectFormRef = ref<any>(null)
    
    const getList = async () => {
      listLoading.value = true
      try {
        const params = {
          page: listQuery.page,
          page_size: listQuery.pageSize,
          search: listQuery.search,
          language: listQuery.language,
          is_favorite: listQuery.is_favorite
        }
        
        console.log('获取项目列表，参数:', params)
        const res = await getProjectList(params) as any
        console.log('获取项目列表结果:', res)
        
        if (res && res.results) {
          // 检查每个项目是否包含标签数据
          res.results.forEach((item: any) => {
            console.log(`项目ID=${item.id}, 名称=${item.name}, 标签:`, item.tags)
          })
          
          list.value = res.results
          total.value = res.count || res.results.length
          
          // 提取语言列表
          const langSet = new Set<string>()
          res.results.forEach((item: any) => {
            if (item.language) {
              langSet.add(item.language)
            }
          })
          languages.value = Array.from(langSet)
        }
      } catch (error) {
        ElMessage.error('获取项目列表失败')
        console.error('获取项目列表失败:', error)
      } finally {
        listLoading.value = false
      }
    }
    
    const fetchTags = async () => {
      try {
        const res = await getProjectTagList() as any
        if (res && res.results) {
          tags.value = res.results
        }
      } catch (error) {
        console.error('获取标签失败:', error)
      }
    }
    
    const resetQuery = () => {
      listQuery.page = 1
      listQuery.search = ''
      listQuery.language = ''
      listQuery.is_favorite = null
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
    
    const handleAdd = () => {
      Object.keys(projectForm).forEach(key => {
        if (key !== 'is_favorite' && key !== 'created_at' && key !== 'updated_at' && key !== 'fetched_at') {
          (projectForm as any)[key] = key === 'id' ? null : ''
        }
      })
      projectForm.is_favorite = false
      projectForm.created_at = new Date().toISOString()
      projectForm.updated_at = new Date().toISOString()
      projectForm.fetched_at = new Date().toISOString()
      selectedTags.value = []
      dialogVisible.value = true
    }
    
    const handleEdit = async (row: any) => {
      try {
        const res = await getProjectDetail(row.id) as any
        if (res) {
          Object.assign(projectForm, res)
          
          // 获取项目标签
          if (res.tags && Array.isArray(res.tags)) {
            selectedTags.value = res.tags.map((tag: any) => tag.id)
          } else {
            selectedTags.value = []
          }
          
          dialogVisible.value = true
        }
      } catch (error) {
        ElMessage.error('获取项目详情失败')
        console.error('获取项目详情失败:', error)
      }
    }
    
    const handleToggleFavorite = async (row: any) => {
      try {
        const updatedStatus = !row.is_favorite
        // 只发送必要的字段，避免发送完整对象
        const updateData = { 
          is_favorite: updatedStatus,
          updated_at: new Date().toISOString()
        }
        console.log(`${updatedStatus ? '收藏' : '取消收藏'}项目，ID=${row.id}，数据:`, updateData)
        
        const res = await updateProject(row.id, updateData)
        console.log(`${updatedStatus ? '收藏' : '取消收藏'}项目成功:`, res)
        
        // 更新本地数据
        row.is_favorite = updatedStatus
        ElMessage.success(`项目已${updatedStatus ? '收藏' : '取消收藏'}`)
      } catch (error) {
        ElMessage.error('操作失败')
        console.error('收藏状态更新失败:', error)
        // 刷新列表，确保显示正确的状态
        getList()
      }
    }
    
    const handleDelete = (row: any) => {
      ElMessageBox.confirm('确认删除此项目吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteProject(row.id)
          ElMessage.success('删除成功')
          getList()
        } catch (error) {
          ElMessage.error('删除失败')
          console.error('删除项目失败:', error)
        }
      }).catch(() => {
        // 取消删除
      })
    }
    
    const resetForm = () => {
      if (projectFormRef.value) {
        projectFormRef.value.resetFields()
      }
      selectedTags.value = []
    }
    
    const submitForm = async () => {
      if (!projectFormRef.value) return
      
      try {
        await projectFormRef.value.validate()
        submitLoading.value = true
        
        const now = new Date().toISOString()
        const projectData = {
          ...projectForm,
          updated_at: now,
          fetched_at: now
        }
        
        try {
          let res
          if (projectForm.id) {
            // 更新项目
            console.log('更新项目数据:', projectData)
            res = await updateProject(projectForm.id, projectData) as any
            console.log('项目更新成功:', res)
            
            // 处理标签更新
            const oldTags = list.value.find((item: any) => item.id === projectForm.id)?.tags || []
            const oldTagIds = oldTags.map((tag: any) => tag.id)
            
            console.log('旧标签:', oldTags)
            console.log('新选择的标签ID:', selectedTags.value)
            
            // 添加新标签
            for (const tagId of selectedTags.value) {
              if (!oldTagIds.includes(tagId)) {
                console.log(`添加新标签 ID=${tagId}`)
                try {
                  await addTagToProject(projectForm.id, tagId)
                } catch (tagError) {
                  console.error(`添加标签失败 ID=${tagId}:`, tagError)
                  // 继续处理其他标签，不中断流程
                }
              }
            }
            
            // 移除旧标签
            for (const tagId of oldTagIds) {
              if (!selectedTags.value.includes(tagId)) {
                console.log(`移除旧标签 ID=${tagId}`)
                try {
                  await removeTagFromProject(projectForm.id, tagId)
                } catch (tagError) {
                  console.error(`移除标签失败 ID=${tagId}:`, tagError)
                  // 继续处理其他标签，不中断流程
                }
              }
            }
            
            ElMessage.success('项目更新成功')
          } else {
            // 创建项目
            console.log('创建项目数据:', projectData)
            res = await createProject(projectData) as any
            console.log('项目创建成功:', res)
            
            // 添加标签
            if (res && res.id) {
              console.log('为新项目添加标签:', selectedTags.value)
              for (const tagId of selectedTags.value) {
                try {
                  await addTagToProject(res.id, tagId)
                } catch (tagError) {
                  console.error(`为新项目添加标签失败 ID=${tagId}:`, tagError)
                  // 继续处理其他标签，不中断流程
                }
              }
            }
            
            ElMessage.success('项目创建成功')
          }
          
          dialogVisible.value = false
          getList()
        } catch (error) {
          ElMessage.error(projectForm.id ? '更新失败' : '创建失败')
          console.error(projectForm.id ? '更新项目失败:' : '创建项目失败:', error)
        } finally {
          submitLoading.value = false
        }
      } catch (validateError) {
        console.log('表单验证失败', validateError)
      }
    }
    
    onMounted(() => {
      getList()
      fetchTags()
    })
    
    return {
      list,
      total,
      listLoading,
      listQuery,
      languages,
      tags,
      selectedTags,
      dialogVisible,
      projectForm,
      rules,
      submitLoading,
      projectFormRef,
      getList,
      resetQuery,
      handleSizeChange,
      handleCurrentChange,
      handleAdd,
      handleEdit,
      handleToggleFavorite,
      handleDelete,
      submitForm,
      resetForm
    }
  }
})
</script>

<style scoped>
.project-list-container {
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

.tag {
  margin-right: 5px;
}

/* 调整表单项的样式 */
:deep(.el-form-item) {
  margin-right: 15px;
}

/* 调整下拉框的宽度 */
:deep(.el-select) {
  width: 180px;
}

/* 调整表单中项目标签下拉框的宽度 */
.el-dialog :deep(.el-select) {
  width: 100%;
}
</style>

<style>
/* 全局样式，确保下拉菜单显示在最上层 */
.project-select-dropdown {
  z-index: 9999 !important;
  min-width: 180px !important;
}
</style> 