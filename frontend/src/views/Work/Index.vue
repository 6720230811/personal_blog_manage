<template>
  <div class="work-container">
    <div class="page-header">
      <h2>工作经历</h2>
      <el-button type="primary" @click="handleAdd">添加工作经历</el-button>
    </div>

    <el-card>
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
        <el-table-column prop="project_name" label="项目/公司名称" min-width="150" />
        <el-table-column prop="position" label="职位" width="150" />
        
        <el-table-column label="起止时间" width="200">
          <template #default="{ row }">
            <span>{{ formatDate(row.start_date) }} ~ {{ row.end_date ? formatDate(row.end_date) : '至今' }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="display_order" label="显示顺序" align="center" width="100" />
        
        <el-table-column label="操作" align="center" width="180">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 工作经历表单对话框 -->
    <el-dialog 
      :title="workForm.id ? '编辑工作经历' : '添加工作经历'" 
      v-model="dialogVisible" 
      width="600px"
      :close-on-click-modal="false"
      @closed="resetForm"
    >
      <el-form ref="workFormRef" :model="workForm" :rules="rules" label-width="100px">
        <el-form-item label="项目/公司" prop="project_name">
          <el-input v-model="workForm.project_name" placeholder="项目或公司名称" />
        </el-form-item>
        
        <el-form-item label="职位" prop="position">
          <el-input v-model="workForm.position" placeholder="职位名称" />
        </el-form-item>
        
        <el-form-item label="开始时间" prop="start_date">
          <el-date-picker
            v-model="workForm.start_date"
            type="date"
            placeholder="选择开始日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="结束时间" prop="end_date">
          <el-date-picker
            v-model="workForm.end_date"
            type="date"
            placeholder="选择结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="工作描述" prop="description">
          <el-input
            v-model="workForm.description"
            type="textarea"
            :rows="5"
            placeholder="工作职责和成就描述"
          />
        </el-form-item>
        
        <el-form-item label="显示顺序" prop="display_order">
          <el-input-number v-model="workForm.display_order" :min="0" :step="1" />
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
import { getWorkList, createWork, updateWork, deleteWork } from '@/api'

export default defineComponent({
  name: 'WorkList',
  setup() {
    const list = ref<any[]>([])
    const listLoading = ref(false)
    const dialogVisible = ref(false)
    const submitLoading = ref(false)
    
    const workForm = reactive({
      id: null as number | null,
      project_name: '',
      position: '',
      description: '',
      start_date: '',
      end_date: '',
      display_order: 0
    })
    
    const rules = {
      project_name: [{ required: true, message: '请输入项目/公司名称', trigger: 'blur' }],
      position: [{ required: true, message: '请输入职位名称', trigger: 'blur' }],
      start_date: [{ required: true, message: '请选择开始时间', trigger: 'change' }]
    }
    
    const workFormRef = ref<any>(null)
    
    const getList = async () => {
      listLoading.value = true
      try {
        const res = await getWorkList({ ordering: 'display_order' }) as any
        
        if (res && res.results) {
          list.value = res.results
        }
      } catch (error) {
        ElMessage.error('获取工作经历失败')
        console.error('获取工作经历失败:', error)
      } finally {
        listLoading.value = false
      }
    }
    
    const formatDate = (dateStr: string) => {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    }
    
    const handleAdd = () => {
      Object.keys(workForm).forEach(key => {
        if (key === 'id') {
          workForm.id = null
        } else if (key === 'display_order') {
          workForm.display_order = 0
        } else {
          (workForm as any)[key] = ''
        }
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row: any) => {
      Object.assign(workForm, row)
      dialogVisible.value = true
    }
    
    const handleDelete = (row: any) => {
      ElMessageBox.confirm('确认删除此工作经历吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteWork(row.id)
          ElMessage.success('删除成功')
          getList()
        } catch (error) {
          ElMessage.error('删除失败')
          console.error('删除工作经历失败:', error)
        }
      }).catch(() => {
        // 取消删除
      })
    }
    
    const resetForm = () => {
      if (workFormRef.value) {
        workFormRef.value.resetFields()
      }
    }
    
    const submitForm = async () => {
      if (!workFormRef.value) return
      
      try {
        await workFormRef.value.validate()
        submitLoading.value = true
        
        try {
          if (workForm.id) {
            // 更新工作经历
            await updateWork(workForm.id, workForm)
            ElMessage.success('工作经历更新成功')
          } else {
            // 创建工作经历
            await createWork(workForm)
            ElMessage.success('工作经历创建成功')
          }
          
          dialogVisible.value = false
          getList()
        } catch (error) {
          ElMessage.error(workForm.id ? '更新失败' : '创建失败')
          console.error(workForm.id ? '更新工作经历失败:' : '创建工作经历失败:', error)
        } finally {
          submitLoading.value = false
        }
      } catch (validateError) {
        console.log('表单验证失败', validateError)
      }
    }
    
    onMounted(() => {
      getList()
    })
    
    return {
      list,
      listLoading,
      dialogVisible,
      workForm,
      rules,
      submitLoading,
      workFormRef,
      formatDate,
      getList,
      handleAdd,
      handleEdit,
      handleDelete,
      submitForm,
      resetForm
    }
  }
})
</script>

<style scoped>
.work-container {
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
</style> 