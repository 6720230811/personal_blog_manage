<template>
  <div class="education-container">
    <div class="page-header">
      <h2>教育经历</h2>
      <el-button type="primary" @click="handleAdd">添加教育经历</el-button>
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
        <el-table-column prop="school_name" label="学校名称" min-width="150" />
        <el-table-column prop="major" label="专业" width="150" />
        <el-table-column prop="degree" label="学位" width="120" />
        
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

    <!-- 教育经历表单对话框 -->
    <el-dialog 
      :title="educationForm.id ? '编辑教育经历' : '添加教育经历'" 
      v-model="dialogVisible" 
      width="500px"
      :close-on-click-modal="false"
      @closed="resetForm"
    >
      <el-form ref="educationFormRef" :model="educationForm" :rules="rules" label-width="100px">
        <el-form-item label="学校名称" prop="school_name">
          <el-input v-model="educationForm.school_name" placeholder="学校名称" />
        </el-form-item>
        
        <el-form-item label="专业" prop="major">
          <el-input v-model="educationForm.major" placeholder="专业名称" />
        </el-form-item>
        
        <el-form-item label="学位" prop="degree">
          <el-select v-model="educationForm.degree" placeholder="选择学位" style="width: 100%">
            <el-option label="学士" value="学士" />
            <el-option label="硕士" value="硕士" />
            <el-option label="博士" value="博士" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="开始时间" prop="start_date">
          <el-date-picker
            v-model="educationForm.start_date"
            type="date"
            placeholder="选择开始日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="结束时间" prop="end_date">
          <el-date-picker
            v-model="educationForm.end_date"
            type="date"
            placeholder="选择结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="显示顺序" prop="display_order">
          <el-input-number v-model="educationForm.display_order" :min="0" :step="1" />
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
import { getEducationList, createEducation, updateEducation, deleteEducation } from '@/api'

export default defineComponent({
  name: 'EducationList',
  setup() {
    const list = ref<any[]>([])
    const listLoading = ref(false)
    const dialogVisible = ref(false)
    const submitLoading = ref(false)
    
    const educationForm = reactive({
      id: null as number | null,
      school_name: '',
      major: '',
      degree: '',
      start_date: '',
      end_date: '',
      display_order: 0
    })
    
    const rules = {
      school_name: [{ required: true, message: '请输入学校名称', trigger: 'blur' }],
      start_date: [{ required: true, message: '请选择开始时间', trigger: 'change' }]
    }
    
    const educationFormRef = ref<any>(null)
    
    const getList = async () => {
      listLoading.value = true
      try {
        const res = await getEducationList({ ordering: 'display_order' }) as any
        
        if (res && res.results) {
          list.value = res.results
        }
      } catch (error) {
        ElMessage.error('获取教育经历失败')
        console.error('获取教育经历失败:', error)
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
      Object.keys(educationForm).forEach(key => {
        if (key === 'id') {
          educationForm.id = null
        } else if (key === 'display_order') {
          educationForm.display_order = 0
        } else {
          (educationForm as any)[key] = ''
        }
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row: any) => {
      Object.assign(educationForm, row)
      dialogVisible.value = true
    }
    
    const handleDelete = (row: any) => {
      ElMessageBox.confirm('确认删除此教育经历吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteEducation(row.id)
          ElMessage.success('删除成功')
          getList()
        } catch (error) {
          ElMessage.error('删除失败')
          console.error('删除教育经历失败:', error)
        }
      }).catch(() => {
        // 取消删除
      })
    }
    
    const resetForm = () => {
      if (educationFormRef.value) {
        educationFormRef.value.resetFields()
      }
    }
    
    const submitForm = async () => {
      if (!educationFormRef.value) return
      
      try {
        await educationFormRef.value.validate()
        submitLoading.value = true
        
        try {
          if (educationForm.id) {
            // 更新教育经历
            await updateEducation(educationForm.id, educationForm)
            ElMessage.success('教育经历更新成功')
          } else {
            // 创建教育经历
            await createEducation(educationForm)
            ElMessage.success('教育经历创建成功')
          }
          
          dialogVisible.value = false
          getList()
        } catch (error) {
          ElMessage.error(educationForm.id ? '更新失败' : '创建失败')
          console.error(educationForm.id ? '更新教育经历失败:' : '创建教育经历失败:', error)
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
      educationForm,
      rules,
      submitLoading,
      educationFormRef,
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
.education-container {
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