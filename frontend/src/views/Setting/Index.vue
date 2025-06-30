<template>
  <div class="setting-container">
    <div class="page-header">
      <h2>系统设置</h2>
      <el-button type="primary" @click="handleSave" :loading="saveLoading">保存设置</el-button>
    </div>

    <el-card v-loading="loading">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本设置" name="basic">
          <el-form ref="basicFormRef" :model="basicForm" :rules="basicRules" label-width="120px">
            <el-form-item label="网站标题" prop="site_title">
              <el-input v-model="basicForm.site_title" placeholder="网站标题" />
            </el-form-item>
            
            <el-form-item label="网站描述" prop="site_description">
              <el-input
                v-model="basicForm.site_description"
                type="textarea"
                :rows="3"
                placeholder="网站描述"
              />
            </el-form-item>
            
            <el-form-item label="网站关键词" prop="site_keywords">
              <el-input v-model="basicForm.site_keywords" placeholder="网站关键词，以逗号分隔" />
            </el-form-item>
            
            <el-form-item label="网站图标" prop="site_favicon">
              <el-input v-model="basicForm.site_favicon" placeholder="网站图标URL" />
            </el-form-item>
            
            <el-form-item label="网站Logo" prop="site_logo">
              <el-input v-model="basicForm.site_logo" placeholder="网站Logo URL" />
            </el-form-item>
            
            <el-form-item label="备案信息" prop="icp_record">
              <el-input v-model="basicForm.icp_record" placeholder="ICP备案号" />
            </el-form-item>
            
            <el-form-item label="底部版权" prop="copyright">
              <el-input v-model="basicForm.copyright" placeholder="底部版权信息" />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="博客设置" name="blog">
          <el-form ref="blogFormRef" :model="blogForm" label-width="120px">
            <el-form-item label="文章列表显示" prop="posts_per_page">
              <el-input-number v-model="blogForm.posts_per_page" :min="1" :max="50" :step="1" />
              <span class="form-tip">每页显示的文章数量</span>
            </el-form-item>
            
            <el-form-item label="默认分类" prop="default_category">
              <el-input v-model="blogForm.default_category" placeholder="默认分类名称" />
            </el-form-item>
            
            <el-form-item label="允许评论">
              <el-switch v-model="blogForm.allow_comments" />
            </el-form-item>
            
            <el-form-item label="评论审核">
              <el-switch v-model="blogForm.moderate_comments" />
              <span class="form-tip">开启后，评论需要审核才能显示</span>
            </el-form-item>
            
            <el-form-item label="显示相关文章">
              <el-switch v-model="blogForm.show_related_posts" />
            </el-form-item>
            
            <el-form-item label="相关文章数量" prop="related_posts_count" v-if="blogForm.show_related_posts">
              <el-input-number v-model="blogForm.related_posts_count" :min="1" :max="10" :step="1" />
            </el-form-item>
            
            <el-form-item label="代码高亮主题" prop="code_highlight_theme">
              <el-select v-model="blogForm.code_highlight_theme" placeholder="选择代码高亮主题" style="width: 100%">
                <el-option label="Default" value="default" />
                <el-option label="Dark" value="dark" />
                <el-option label="Github" value="github" />
                <el-option label="Monokai" value="monokai" />
                <el-option label="Solarized Light" value="solarized-light" />
                <el-option label="Solarized Dark" value="solarized-dark" />
              </el-select>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="邮件设置" name="email">
          <el-form ref="emailFormRef" :model="emailForm" :rules="emailRules" label-width="120px">
            <el-form-item label="SMTP服务器" prop="smtp_host">
              <el-input v-model="emailForm.smtp_host" placeholder="SMTP服务器地址" />
            </el-form-item>
            
            <el-form-item label="SMTP端口" prop="smtp_port">
              <el-input v-model="emailForm.smtp_port" placeholder="SMTP端口号" />
            </el-form-item>
            
            <el-form-item label="邮箱账号" prop="smtp_user">
              <el-input v-model="emailForm.smtp_user" placeholder="邮箱账号" />
            </el-form-item>
            
            <el-form-item label="邮箱密码" prop="smtp_password">
              <el-input v-model="emailForm.smtp_password" type="password" placeholder="邮箱密码或授权码" show-password />
            </el-form-item>
            
            <el-form-item label="发件人" prop="smtp_sender">
              <el-input v-model="emailForm.smtp_sender" placeholder="发件人名称" />
            </el-form-item>
            
            <el-form-item label="使用SSL">
              <el-switch v-model="emailForm.smtp_ssl" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="success" @click="testEmail" :loading="testingEmail">测试邮件发送</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="系统维护" name="system">
          <el-form label-width="120px">
            <el-form-item label="网站缓存">
              <el-button type="danger" @click="clearCache('site')" :loading="clearingCache.site">清除网站缓存</el-button>
              <span class="form-tip">清除网站页面缓存</span>
            </el-form-item>
            
            <el-form-item label="图片缓存">
              <el-button type="danger" @click="clearCache('image')" :loading="clearingCache.image">清除图片缓存</el-button>
              <span class="form-tip">清除图片缓存</span>
            </el-form-item>
            
            <el-form-item label="数据库备份">
              <el-button type="primary" @click="backupDatabase" :loading="backingUp">备份数据库</el-button>
              <span class="form-tip">创建数据库备份</span>
            </el-form-item>
            
            <el-form-item label="系统日志">
              <el-button type="info" @click="viewLogs">查看系统日志</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 日志查看对话框 -->
    <el-dialog
      title="系统日志"
      v-model="logDialogVisible"
      width="80%"
    >
      <div v-loading="loadingLogs">
        <el-select v-model="selectedLogFile" placeholder="选择日志文件" style="width: 100%; margin-bottom: 15px;">
          <el-option
            v-for="log in logFiles"
            :key="log"
            :label="log"
            :value="log"
          />
        </el-select>
        
        <pre v-if="logContent" class="log-content">{{ logContent }}</pre>
        <div v-else class="empty-log">请选择日志文件查看内容</div>
      </div>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  getSystemSettings, 
  updateSystemSettings, 
  testEmailSettings,
  clearSystemCache,
  backupSystemDatabase,
  getSystemLogs,
  getSystemLogContent 
} from '@/api'

export default defineComponent({
  name: 'SystemSettings',
  setup() {
    const loading = ref(false)
    const saveLoading = ref(false)
    const activeTab = ref('basic')
    const testingEmail = ref(false)
    const backingUp = ref(false)
    const clearingCache = reactive({
      site: false,
      image: false
    })
    const logDialogVisible = ref(false)
    const loadingLogs = ref(false)
    const logFiles = ref<string[]>([])
    const logContent = ref('')
    const selectedLogFile = ref('')
    
    // 表单引用
    const basicFormRef = ref<any>(null)
    const blogFormRef = ref<any>(null)
    const emailFormRef = ref<any>(null)
    
    // 基本设置表单
    const basicForm = reactive({
      site_title: '',
      site_description: '',
      site_keywords: '',
      site_favicon: '',
      site_logo: '',
      icp_record: '',
      copyright: ''
    })
    
    // 博客设置表单
    const blogForm = reactive({
      posts_per_page: 10,
      default_category: '未分类',
      allow_comments: true,
      moderate_comments: false,
      show_related_posts: true,
      related_posts_count: 5,
      code_highlight_theme: 'github'
    })
    
    // 邮件设置表单
    const emailForm = reactive({
      smtp_host: '',
      smtp_port: '',
      smtp_user: '',
      smtp_password: '',
      smtp_sender: '',
      smtp_ssl: true
    })
    
    // 表单验证规则
    const basicRules = {
      site_title: [{ required: true, message: '请输入网站标题', trigger: 'blur' }]
    }
    
    const emailRules = {
      smtp_host: [{ required: true, message: '请输入SMTP服务器地址', trigger: 'blur' }],
      smtp_port: [{ required: true, message: '请输入SMTP端口号', trigger: 'blur' }],
      smtp_user: [{ required: true, message: '请输入邮箱账号', trigger: 'blur' }]
    }
    
    // 获取系统设置
    const getSettings = async () => {
      loading.value = true
      try {
        const res = await getSystemSettings() as any
        
        if (res) {
          // 填充基本设置
          Object.keys(basicForm).forEach(key => {
            if (res[key] !== undefined) {
              (basicForm as any)[key] = res[key]
            }
          })
          
          // 填充博客设置
          Object.keys(blogForm).forEach(key => {
            if (res[key] !== undefined) {
              (blogForm as any)[key] = res[key]
            }
          })
          
          // 填充邮件设置
          Object.keys(emailForm).forEach(key => {
            if (res[key] !== undefined && key !== 'smtp_password') {
              (emailForm as any)[key] = res[key]
            }
          })
        }
      } catch (error) {
        ElMessage.error('获取系统设置失败')
        console.error('获取系统设置失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    // 保存系统设置
    const handleSave = async () => {
      let formValid = true
      
      if (activeTab.value === 'basic' && basicFormRef.value) {
        try {
          await basicFormRef.value.validate()
        } catch (error) {
          formValid = false
        }
      }
      
      if (activeTab.value === 'email' && emailFormRef.value) {
        try {
          await emailFormRef.value.validate()
        } catch (error) {
          formValid = false
        }
      }
      
      if (!formValid) return
      
      saveLoading.value = true
      
      try {
        // 合并表单数据
        const settingsData = {
          ...basicForm,
          ...blogForm,
          ...emailForm
        }
        
        await updateSystemSettings(settingsData)
        ElMessage.success('系统设置更新成功')
      } catch (error) {
        ElMessage.error('系统设置更新失败')
        console.error('更新系统设置失败:', error)
      } finally {
        saveLoading.value = false
      }
    }
    
    // 测试邮件发送
    const testEmail = async () => {
      if (emailFormRef.value) {
        try {
          await emailFormRef.value.validate()
        } catch (error) {
          return
        }
      }
      
      testingEmail.value = true
      
      try {
        await testEmailSettings(emailForm)
        ElMessage.success('测试邮件发送成功')
      } catch (error) {
        ElMessage.error('测试邮件发送失败')
        console.error('测试邮件发送失败:', error)
      } finally {
        testingEmail.value = false
      }
    }
    
    // 清除缓存
    const clearCache = async (type: string) => {
      clearingCache[type as keyof typeof clearingCache] = true
      
      try {
        await clearSystemCache({ type })
        ElMessage.success(`${type === 'site' ? '网站' : '图片'}缓存清除成功`)
      } catch (error) {
        ElMessage.error(`${type === 'site' ? '网站' : '图片'}缓存清除失败`)
        console.error('清除缓存失败:', error)
      } finally {
        clearingCache[type as keyof typeof clearingCache] = false
      }
    }
    
    // 备份数据库
    const backupDatabase = async () => {
      backingUp.value = true
      
      try {
        const res = await backupSystemDatabase() as any
        if (res && res.file) {
          ElMessage.success(`数据库备份成功，文件名：${res.file}`)
        }
      } catch (error) {
        ElMessage.error('数据库备份失败')
        console.error('数据库备份失败:', error)
      } finally {
        backingUp.value = false
      }
    }
    
    // 查看系统日志
    const viewLogs = async () => {
      logDialogVisible.value = true
      loadingLogs.value = true
      
      try {
        const res = await getSystemLogs() as any
        if (res && Array.isArray(res)) {
          logFiles.value = res
          if (res.length > 0) {
            selectedLogFile.value = res[0]
          }
        }
      } catch (error) {
        ElMessage.error('获取日志列表失败')
        console.error('获取日志列表失败:', error)
      } finally {
        loadingLogs.value = false
      }
    }
    
    // 监听选择的日志文件变化
    watch(selectedLogFile, async (newFile) => {
      if (!newFile) {
        logContent.value = ''
        return
      }
      
      loadingLogs.value = true
      
      try {
        const res = await getSystemLogContent({ filename: newFile }) as any
        if (res && res.content) {
          logContent.value = res.content
        } else {
          logContent.value = '日志内容为空'
        }
      } catch (error) {
        ElMessage.error('获取日志内容失败')
        console.error('获取日志内容失败:', error)
        logContent.value = '获取日志内容失败'
      } finally {
        loadingLogs.value = false
      }
    })
    
    onMounted(() => {
      getSettings()
    })
    
    return {
      loading,
      saveLoading,
      activeTab,
      testingEmail,
      backingUp,
      clearingCache,
      logDialogVisible,
      loadingLogs,
      logFiles,
      logContent,
      selectedLogFile,
      basicForm,
      blogForm,
      emailForm,
      basicRules,
      emailRules,
      basicFormRef,
      blogFormRef,
      emailFormRef,
      handleSave,
      testEmail,
      clearCache,
      backupDatabase,
      viewLogs
    }
  }
})
</script>

<style scoped>
.setting-container {
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

.form-tip {
  margin-left: 10px;
  color: #666;
  font-size: 12px;
}

.log-content {
  max-height: 400px;
  overflow-y: auto;
  background: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
}

.empty-log {
  text-align: center;
  color: #999;
  padding: 50px 0;
}
</style> 