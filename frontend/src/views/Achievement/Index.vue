<template>
  <div class="achievement-container">
    <div class="page-header">
      <h2>成就管理</h2>
      <el-button type="primary" @click="handleAdd">添加成就</el-button>
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
        <el-table-column prop="name" label="成就名称" min-width="150" />
        <el-table-column prop="date" label="获得时间" width="150">
          <template #default="{ row }">
            {{ row.date ? formatDate(row.date) : '未知' }}
          </template>
        </el-table-column>
        <el-table-column prop="location" label="地点" width="150" />
        <el-table-column prop="display_order" label="显示顺序" align="center" width="100" />
        
        <el-table-column label="操作" align="center" width="180">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 成就表单对话框 -->
    <el-dialog 
      :title="achievementForm.id ? '编辑成就' : '添加成就'" 
      v-model="dialogVisible" 
      width="600px"
      :close-on-click-modal="false"
      @closed="resetForm"
    >
      <el-form ref="achievementFormRef" :model="achievementForm" :rules="rules" label-width="100px">
        <el-form-item label="成就名称" prop="name">
          <el-input v-model="achievementForm.name" placeholder="成就或奖项名称" />
        </el-form-item>
        
        <el-form-item label="获得时间" prop="date">
          <el-date-picker
            v-model="achievementForm.date"
            type="date"
            placeholder="选择获得日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="地点" prop="location">
          <el-input v-model="achievementForm.location" placeholder="获得地点" />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="achievementForm.description"
            type="textarea"
            :rows="5"
            placeholder="成就详细描述"
          />
        </el-form-item>
        
        <el-form-item label="显示顺序" prop="display_order">
          <el-input-number v-model="achievementForm.display_order" :min="0" :step="1" />
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
import { getAchievementList, createAchievement, updateAchievement, deleteAchievement } from '@/api'

export default defineComponent({
  name: 'AchievementList',
  setup() {
    const list = ref<any[]>([])
    const listLoading = ref(false)
    const dialogVisible = ref(false)
    const submitLoading = ref(false)
    
    const achievementForm = reactive({
      id: null as number | null,
      name: '',
      description: '',
      date: '',
      location: '',
      display_order: 0
    })
    
    const rules = {
      name: [{ required: true, message: '请输入成就名称', trigger: 'blur' }]
    }
    
    const achievementFormRef = ref<any>(null)
    
    const getList = async () => {
      listLoading.value = true
      try {
        const res = await getAchievementList({ ordering: 'display_order' }) as any
        
        if (res && res.results) {
          list.value = res.results
        }
      } catch (error) {
        ElMessage.error('获取成就列表失败')
        console.error('获取成就列表失败:', error)
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
      Object.keys(achievementForm).forEach(key => {
        if (key === 'id') {
          achievementForm.id = null
        } else if (key === 'display_order') {
          achievementForm.display_order = 0
        } else {
          (achievementForm as any)[key] = ''
        }
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row: any) => {
      Object.assign(achievementForm, row)
      dialogVisible.value = true
    }
    
    const handleDelete = (row: any) => {
      ElMessageBox.confirm('确认删除此成就吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteAchievement(row.id)
          ElMessage.success('删除成功')
          getList()
        } catch (error) {
          ElMessage.error('删除失败')
          console.error('删除成就失败:', error)
        }
      }).catch(() => {
        // 取消删除
      })
    }
    
    const resetForm = () => {
      if (achievementFormRef.value) {
        achievementFormRef.value.resetFields()
      }
    }
    
    const submitForm = async () => {
      if (!achievementFormRef.value) return
      
      try {
        await achievementFormRef.value.validate()
        submitLoading.value = true
        
        try {
          if (achievementForm.id) {
            // 更新成就
            await updateAchievement(achievementForm.id, achievementForm)
            ElMessage.success('成就更新成功')
          } else {
            // 创建成就
            await createAchievement(achievementForm)
            ElMessage.success('成就创建成功')
          }
          
          dialogVisible.value = false
          getList()
        } catch (error) {
          ElMessage.error(achievementForm.id ? '更新失败' : '创建失败')
          console.error(achievementForm.id ? '更新成就失败:' : '创建成就失败:', error)
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
      achievementForm,
      rules,
      submitLoading,
      achievementFormRef,
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
.achievement-container {
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