<template>
  <div class="blog-add-container">
    <div class="page-header">
      <h2>添加博客</h2>
      <el-button @click="router.push('/blog')">返回列表</el-button>
    </div>

    <el-card>
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

        <el-form-item label="推荐">
          <el-switch
            v-model="blogForm.featured"
            active-text="是"
            inactive-text="否"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">发布</el-button>
          <el-button @click="saveDraft" :loading="draftLoading">保存草稿</el-button>
          <el-button @click="router.push('/blog')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getBlogTagList, addBlogTag, createBlog, addTagToBlog } from '@/api'

export default defineComponent({
  name: 'BlogAdd',
  setup() {
    const router = useRouter()
    const blogFormRef = ref<any>(null)
    const blogForm = reactive({
      title: '',
      category: '',
      cover_image: '',
      summary: '',
      content: '',
      featured: false,
      published: false
    })
    
    const rules = {
      title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
      category: [{ required: true, message: '请选择分类', trigger: 'change' }],
      content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
    }
    
    const submitLoading = ref(false)
    const draftLoading = ref(false)
    const tags = ref<any[]>([])
    const categories = ref<string[]>(['技术', '生活', '随笔', '学习'])
    const selectedTags = ref<number[]>([])
    const newCategory = ref('')
    
    const fetchTags = async () => {
      try {
        const res = await getBlogTagList() as any
        if (res && res.results) {
          tags.value = res.results
        }
      } catch (error) {
        console.error('获取标签失败:', error)
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
      if (!blogFormRef.value) return
      
      try {
        await blogFormRef.value.validate()
        submitLoading.value = true
        
        // 设置发布状态
        blogForm.published = true
        
        // 添加时间
        const now = new Date().toISOString()
        const blogData = {
          ...blogForm,
          created_at: now,
          updated_at: now,
          published_at: now
        }
        
        try {
          const res = await createBlog(blogData) as any
          if (res && res.id) {
            // 添加标签
            for (const tagId of selectedTags.value) {
              await addTagToBlog(res.id, tagId)
            }
            
            ElMessage.success('博客发布成功')
            router.push('/blog')
          }
        } catch (error) {
          ElMessage.error('博客发布失败')
          console.error('发布博客失败:', error)
        } finally {
          submitLoading.value = false
        }
      } catch (validateError) {
        console.log('表单验证失败', validateError)
      }
    }
    
    const saveDraft = async () => {
      if (!blogFormRef.value) return
      
      try {
        await blogFormRef.value.validate()
        draftLoading.value = true
        
        // 设置草稿状态
        blogForm.published = false
        
        // 添加时间
        const now = new Date().toISOString()
        const blogData = {
          ...blogForm,
          created_at: now,
          updated_at: now
        }
        
        try {
          const res = await createBlog(blogData) as any
          if (res && res.id) {
            // 添加标签
            for (const tagId of selectedTags.value) {
              await addTagToBlog(res.id, tagId)
            }
            
            ElMessage.success('草稿保存成功')
            router.push('/blog')
          }
        } catch (error) {
          ElMessage.error('草稿保存失败')
          console.error('保存草稿失败:', error)
        } finally {
          draftLoading.value = false
        }
      } catch (validateError) {
        console.log('表单验证失败', validateError)
      }
    }
    
    onMounted(() => {
      fetchTags()
    })
    
    return {
      router,
      blogForm,
      rules,
      blogFormRef,
      submitLoading,
      draftLoading,
      tags,
      categories,
      selectedTags,
      newCategory,
      submitForm,
      saveDraft,
      addCategory
    }
  }
})
</script>

<style scoped>
.blog-add-container {
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