<template>
  <div class="blog-edit-container">
    <div class="page-header">
      <h2>编辑博客</h2>
      <el-button @click="router.push('/blog')">返回列表</el-button>
    </div>

    <el-card v-loading="loading">
      <el-form ref="blogFormRef" :model="blogForm" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="blogForm.title" placeholder="请输入博客标题" />
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-select v-model="blogForm.category" placeholder="请选择分类" teleported :popper-options="{ strategy: 'fixed' }" popper-class="blog-select-dropdown">
            <el-option
              v-for="item in categories"
              :key="item"
              :label="item"
              :value="item"
            />
            <template #dropdown>
              <div>
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
                <el-divider />
              </div>
            </template>
          </el-select>
        </el-form-item>

        <el-form-item label="封面图片" prop="cover_image">
          <el-input v-model="blogForm.cover_image" placeholder="请输入封面图片URL" />
        </el-form-item>

        <el-form-item label="摘要" prop="summary">
          <el-input
            v-model="blogForm.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入博客摘要"
          />
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <el-input
            v-model="blogForm.content"
            type="textarea"
            :rows="10"
            placeholder="请输入博客内容"
          />
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
            popper-class="blog-select-dropdown"
          >
            <el-option
              v-for="tag in tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="发布状态">
          <el-switch
            v-model="blogForm.published"
            active-text="已发布"
            inactive-text="草稿"
          />
        </el-form-item>

        <el-form-item label="推荐">
          <el-switch
            v-model="blogForm.featured"
            active-text="是"
            inactive-text="否"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">保存</el-button>
          <el-button @click="router.push('/blog')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getBlogDetail, updateBlog, getBlogTagList, addBlogTag, addTagToBlog, removeTagFromBlog } from '@/api'

export default defineComponent({
  name: 'BlogEdit',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const route = useRoute()
    const router = useRouter()
    const blogForm = reactive({
      title: '',
      category: '',
      cover_image: '',
      summary: '',
      content: '',
      featured: false,
      published: false,
      views_count: 0,
      created_at: '',
      updated_at: '',
      published_at: null as string | null
    })
    
    const rules = {
      title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
      category: [{ required: true, message: '请选择分类', trigger: 'change' }],
      content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
    }
    
    const blogFormRef = ref<any>(null)
    const submitLoading = ref(false)
    const loading = ref(false)
    const tags = ref<any[]>([])
    const categories = ref<string[]>(['技术', '生活', '随笔', '学习'])
    const selectedTags = ref<number[]>([])
    const newCategory = ref('')
    const blogTags = ref<any[]>([])
    
    const fetchBlogDetail = async () => {
      loading.value = true
      try {
        const id = Number(props.id)
        console.log('获取博客详情，ID:', id)
        
        // 添加错误处理
        if (isNaN(id) || id <= 0) {
          throw new Error(`无效的博客ID: ${props.id}`)
        }
        
        const res = await getBlogDetail(id) as any
        console.log('获取到的博客详情:', res)
        
        if (!res) {
          throw new Error('获取博客详情返回空数据')
        }
        
        // 复制博客数据到表单
        Object.keys(blogForm).forEach(key => {
          if (res[key] !== undefined) {
            if (key === 'published' || key === 'featured') {
              // 处理布尔值字段
              if (typeof res[key] === 'string') {
                (blogForm as any)[key] = res[key].toLowerCase() === 'true'
              } else {
                (blogForm as any)[key] = Boolean(res[key])
              }
            } else {
              (blogForm as any)[key] = res[key]
            }
          }
        })
        console.log('处理后的表单数据:', blogForm)
        
        // 获取博客标签
        if (res.tags && Array.isArray(res.tags)) {
          blogTags.value = res.tags
          selectedTags.value = res.tags.map((tag: any) => tag.id)
          console.log('处理后的标签:', selectedTags.value)
        } else {
          console.warn('博客没有标签数据或标签格式不正确:', res.tags)
        }
        
        // 添加分类到选项中
        if (res.category && !categories.value.includes(res.category)) {
          categories.value.push(res.category)
          console.log('添加分类到选项:', res.category)
        }
      } catch (error: any) {
        console.error('获取博客详情失败:', error)
        ElMessage.error(`获取博客详情失败: ${error.message || '未知错误'}`)
      } finally {
        loading.value = false
      }
    }
    
    const fetchTags = async () => {
      try {
        console.log('获取标签列表')
        const res = await getBlogTagList() as any
        console.log('获取到的标签列表:', res)
        
        if (res && res.results) {
          tags.value = res.results
        }
      } catch (error: any) {
        console.error('获取标签失败:', error)
        ElMessage.error(`获取标签失败: ${error.message || '未知错误'}`)
      }
    }
    
    const addCategory = () => {
      if (newCategory.value && !categories.value.includes(newCategory.value)) {
        categories.value.push(newCategory.value)
        blogForm.category = newCategory.value
        newCategory.value = ''
      }
    }
    
    const submitForm = async () => {
      if (!blogFormRef.value) {
        console.error('表单引用不存在')
        return
      }
      
      try {
        await blogFormRef.value.validate()
        submitLoading.value = true
        
        // 更新时间
        const now = new Date().toISOString()
        const blogData = {
          ...blogForm,
          updated_at: now,
          published_at: blogForm.published ? (blogForm.published_at || now) : null
        }
        
        console.log('提交的博客数据:', blogData)
        
        try {
          const id = Number(props.id)
          console.log(`开始更新博客ID: ${id}`)
          
          // 确保ID有效
          if (isNaN(id) || id <= 0) {
            throw new Error(`无效的博客ID: ${props.id}`)
          }
          
          const updateResult = await updateBlog(id, blogData)
          console.log('更新博客结果:', updateResult)
          
          // 处理标签更新
          const oldTagIds = blogTags.value.map(tag => tag.id)
          console.log('原有标签IDs:', oldTagIds)
          console.log('新标签IDs:', selectedTags.value)
          
          // 添加新标签
          const addTagPromises = []
          for (const tagId of selectedTags.value) {
            if (!oldTagIds.includes(tagId)) {
              console.log('添加标签:', tagId)
              addTagPromises.push(addTagToBlog(id, tagId))
            }
          }
          
          // 移除旧标签
          const removeTagPromises = []
          for (const tagId of oldTagIds) {
            if (!selectedTags.value.includes(tagId)) {
              console.log('移除标签:', tagId)
              removeTagPromises.push(removeTagFromBlog(id, tagId))
            }
          }
          
          // 等待所有标签操作完成
          if (addTagPromises.length > 0 || removeTagPromises.length > 0) {
            console.log(`执行 ${addTagPromises.length} 个添加标签操作和 ${removeTagPromises.length} 个移除标签操作`)
            await Promise.all([...addTagPromises, ...removeTagPromises])
            console.log('所有标签操作完成')
          } else {
            console.log('没有标签需要更新')
          }
          
          ElMessage.success('博客更新成功')
          router.push('/blog')
        } catch (error: any) {
          console.error('更新博客失败:', error)
          ElMessage.error(`更新博客失败: ${error.message || '未知错误'}`)
        } finally {
          submitLoading.value = false
        }
      } catch (validateError) {
        console.log('表单验证失败', validateError)
        ElMessage.error('请检查表单填写是否正确')
      }
    }
    
    onMounted(() => {
      console.log('博客编辑页面加载，ID:', props.id)
      fetchBlogDetail()
      fetchTags()
    })
    
    return {
      router,
      blogForm,
      rules,
      blogFormRef,
      submitLoading,
      loading,
      tags,
      categories,
      selectedTags,
      newCategory,
      submitForm,
      addCategory
    }
  }
})
</script>

<style scoped>
.blog-edit-container {
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

/* 调整表单项的样式 */
:deep(.el-form-item) {
  margin-bottom: 20px;
}

/* 调整下拉框的宽度 */
:deep(.el-select) {
  width: 100%;
}

/* 调整文本域的宽度 */
:deep(.el-textarea) {
  width: 100%;
}
</style> 