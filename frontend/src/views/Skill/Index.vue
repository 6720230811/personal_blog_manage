<template>
  <div class="skill-container">
    <div class="page-header">
      <h2>技能管理</h2>
      <el-button type="primary" @click="handleAdd">添加技能</el-button>
    </div>

    <el-card>
      <div class="filter-container">
        <el-form :inline="true" :model="listQuery" class="form-inline">
          <el-form-item label="技能名称">
            <el-input v-model="listQuery.name" placeholder="技能名称" clearable />
          </el-form-item>
          <el-form-item label="分类">
            <el-select v-model="listQuery.category" placeholder="技能分类" clearable teleported :popper-options="{ strategy: 'fixed' }" popper-class="skill-select-dropdown">
              <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat" />
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
        <el-table-column prop="name" label="技能名称" min-width="120" />
        <el-table-column prop="category" label="分类" width="120" />
        
        <el-table-column label="熟练度" width="200">
          <template #default="{ row }">
            <el-progress 
              :percentage="row.proficiency * 10" 
              :color="getProficiencyColor(row.proficiency)"
            />
          </template>
        </el-table-column>
        
        <el-table-column label="熟练度值" align="center" width="100">
          <template #default="{ row }">
            <span>{{ row.proficiency }}/10</span>
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

    <!-- 技能表单对话框 -->
    <el-dialog 
      :title="skillForm.id ? '编辑技能' : '添加技能'" 
      v-model="dialogVisible" 
      width="500px"
      :close-on-click-modal="false"
      @closed="resetForm"
    >
      <el-form ref="skillFormRef" :model="skillForm" :rules="rules" label-width="100px">
        <el-form-item label="技能名称" prop="name">
          <el-input v-model="skillForm.name" placeholder="技能名称" />
        </el-form-item>
        
        <el-form-item label="技能分类" prop="category">
          <el-select v-model="skillForm.category" placeholder="选择分类" style="width: 100%" teleported :popper-options="{ strategy: 'fixed' }" popper-class="skill-select-dropdown">
            <el-option 
              v-for="category in categories" 
              :key="category" 
              :label="category" 
              :value="category" 
            />
            <template #footer>
              <div style="padding: 8px">
                <el-input
                  v-model="newCategory"
                  placeholder="添加新分类"
                  @keyup.enter="addCategory"
                >
                  <template #append>
                    <el-button @click="addCategory">添加</el-button>
                  </template>
                </el-input>
              </div>
            </template>
          </el-select>
        </el-form-item>
        
        <el-form-item label="熟练度" prop="proficiency">
          <el-slider
            v-model="skillForm.proficiency"
            :min="1"
            :max="10"
            :format-tooltip="formatProficiency"
            :step="1"
            show-stops
          />
        </el-form-item>
        
        <el-form-item label="显示顺序" prop="display_order">
          <el-input-number v-model="skillForm.display_order" :min="0" :step="1" />
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
import { getSkillList, createSkill, updateSkill, deleteSkill } from '@/api'

export default defineComponent({
  name: 'SkillList',
  setup() {
    const list = ref<any[]>([])
    const total = ref(0)
    const listLoading = ref(false)
    const categories = ref<string[]>(['前端开发', '后端开发', '数据库', '云服务', '其他'])
    const dialogVisible = ref(false)
    const submitLoading = ref(false)
    const newCategory = ref('')
    
    const listQuery = reactive({
      page: 1,
      pageSize: 10,
      name: '',
      category: ''
    })
    
    const skillForm = reactive({
      id: null as number | null,
      name: '',
      proficiency: 5,
      category: '',
      display_order: 0
    })
    
    const rules = {
      name: [{ required: true, message: '请输入技能名称', trigger: 'blur' }],
      category: [{ required: true, message: '请选择或添加技能分类', trigger: 'change' }],
      proficiency: [{ required: true, message: '请选择熟练度', trigger: 'change' }]
    }
    
    const skillFormRef = ref<any>(null)
    
    const getList = async () => {
      listLoading.value = true
      try {
        const params = {
          page: listQuery.page,
          page_size: listQuery.pageSize,
          name: listQuery.name,
          category: listQuery.category
        }
        
        const res = await getSkillList(params) as any
        
        if (res && res.results) {
          list.value = res.results
          total.value = res.count || res.results.length
          
          // 提取分类列表
          const catSet = new Set<string>(categories.value)
          res.results.forEach((item: any) => {
            if (item.category && !catSet.has(item.category)) {
              catSet.add(item.category)
            }
          })
          categories.value = Array.from(catSet)
        }
      } catch (error) {
        ElMessage.error('获取技能列表失败')
        console.error('获取技能列表失败:', error)
      } finally {
        listLoading.value = false
      }
    }
    
    const resetQuery = () => {
      listQuery.page = 1
      listQuery.name = ''
      listQuery.category = ''
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
      Object.keys(skillForm).forEach(key => {
        if (key === 'id') {
          skillForm.id = null
        } else if (key === 'proficiency') {
          skillForm.proficiency = 5
        } else if (key === 'display_order') {
          skillForm.display_order = 0
        } else {
          (skillForm as any)[key] = ''
        }
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row: any) => {
      Object.assign(skillForm, row)
      dialogVisible.value = true
    }
    
    const handleDelete = (row: any) => {
      ElMessageBox.confirm('确认删除此技能吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteSkill(row.id)
          ElMessage.success('删除成功')
          getList()
        } catch (error) {
          ElMessage.error('删除失败')
          console.error('删除技能失败:', error)
        }
      }).catch(() => {
        // 取消删除
      })
    }
    
    const addCategory = () => {
      if (newCategory.value && !categories.value.includes(newCategory.value)) {
        categories.value.push(newCategory.value)
        skillForm.category = newCategory.value
        newCategory.value = ''
      }
    }
    
    const resetForm = () => {
      if (skillFormRef.value) {
        skillFormRef.value.resetFields()
      }
    }
    
    const submitForm = async () => {
      if (!skillFormRef.value) return
      
      try {
        await skillFormRef.value.validate()
        submitLoading.value = true
        
        try {
          if (skillForm.id) {
            // 更新技能
            await updateSkill(skillForm.id, skillForm)
            ElMessage.success('技能更新成功')
          } else {
            // 创建技能
            await createSkill(skillForm)
            ElMessage.success('技能创建成功')
          }
          
          dialogVisible.value = false
          getList()
        } catch (error) {
          ElMessage.error(skillForm.id ? '更新失败' : '创建失败')
          console.error(skillForm.id ? '更新技能失败:' : '创建技能失败:', error)
        } finally {
          submitLoading.value = false
        }
      } catch (validateError) {
        console.log('表单验证失败', validateError)
      }
    }
    
    const getProficiencyColor = (proficiency: number) => {
      if (proficiency <= 3) return '#909399'
      if (proficiency <= 6) return '#E6A23C'
      return '#67C23A'
    }
    
    const formatProficiency = (val: number) => {
      return `${val}/10`
    }
    
    onMounted(() => {
      getList()
    })
    
    return {
      list,
      total,
      listLoading,
      listQuery,
      categories,
      dialogVisible,
      skillForm,
      rules,
      submitLoading,
      skillFormRef,
      newCategory,
      getList,
      resetQuery,
      handleSizeChange,
      handleCurrentChange,
      handleAdd,
      handleEdit,
      handleDelete,
      addCategory,
      submitForm,
      resetForm,
      getProficiencyColor,
      formatProficiency
    }
  }
})
</script>

<style scoped>
.skill-container {
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
.skill-select-dropdown {
  z-index: 9999 !important;
  min-width: 180px !important;
}
</style> 