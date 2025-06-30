<template>
  <div class="profile-container">
    <div class="page-header">
      <h2>个人资料</h2>
      <el-button type="primary" @click="handleSave" :loading="saveLoading">保存更改</el-button>
    </div>

    <el-card v-loading="loading">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本信息" name="basic">
          <el-form ref="basicFormRef" :model="basicForm" :rules="basicRules" label-width="120px">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="basicForm.name" placeholder="您的姓名" />
            </el-form-item>
            
            <el-form-item label="头像" prop="avatar">
              <el-input v-model="basicForm.avatar" placeholder="头像URL" />
            </el-form-item>
            
            <el-form-item label="职业" prop="profession">
              <el-input v-model="basicForm.profession" placeholder="您的职业" />
            </el-form-item>
            
            <el-form-item label="个人简介" prop="bio">
              <el-input
                v-model="basicForm.bio"
                type="textarea"
                :rows="4"
                placeholder="简短的个人介绍"
              />
            </el-form-item>
            
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="basicForm.email" placeholder="电子邮箱地址" />
            </el-form-item>
            
            <!-- 注释掉后端不支持的字段 -->
            <!-- <el-form-item label="电话" prop="phone">
              <el-input v-model="basicForm.phone" placeholder="联系电话" />
            </el-form-item>
            
            <el-form-item label="地址" prop="address">
              <el-input v-model="basicForm.address" placeholder="所在地址" />
            </el-form-item>
            
            <el-form-item label="生日" prop="birthday">
              <el-date-picker
                v-model="basicForm.birthday"
                type="date"
                placeholder="选择生日"
                style="width: 100%"
              />
            </el-form-item> -->
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="社交链接" name="social">
          <el-form ref="socialFormRef" :model="socialForm" label-width="120px">
            <el-form-item label="GitHub" prop="github">
              <el-input v-model="socialForm.github" placeholder="GitHub个人主页链接" />
            </el-form-item>
            
            <!-- 注释掉后端不支持的字段 -->
            <!-- <el-form-item label="LinkedIn" prop="linkedin">
              <el-input v-model="socialForm.linkedin" placeholder="LinkedIn个人主页链接" />
            </el-form-item>
            
            <el-form-item label="Twitter" prop="twitter">
              <el-input v-model="socialForm.twitter" placeholder="Twitter个人主页链接" />
            </el-form-item>
            
            <el-form-item label="微信" prop="wechat">
              <el-input v-model="socialForm.wechat" placeholder="微信号" />
            </el-form-item>
            
            <el-form-item label="个人网站" prop="website">
              <el-input v-model="socialForm.website" placeholder="个人网站链接" />
            </el-form-item>
            
            <el-form-item label="其他链接">
              <div v-for="(link, index) in socialForm.other_links" :key="index" class="other-link">
                <el-input v-model="link.name" placeholder="名称" style="width: 30%; margin-right: 10px;" />
                <el-input v-model="link.url" placeholder="链接" style="width: 60%;" />
                <el-button type="danger" icon="el-icon-delete" circle size="small" @click="removeLink(index)" />
              </div>
              <el-button type="primary" @click="addLink" style="margin-top: 10px;">添加链接</el-button>
            </el-form-item> -->
          </el-form>
        </el-tab-pane>
        
        <!-- 注释掉后端不支持的标签页 -->
        <!-- <el-tab-pane label="个人简历" name="resume">
          <el-form ref="resumeFormRef" :model="resumeForm" label-width="120px">
            <el-form-item label="简历标题" prop="title">
              <el-input v-model="resumeForm.title" placeholder="简历标题" />
            </el-form-item>
            
            <el-form-item label="简历内容" prop="content">
              <el-input
                v-model="resumeForm.content"
                type="textarea"
                :rows="15"
                placeholder="简历内容（支持Markdown格式）"
              />
            </el-form-item>
            
            <el-form-item label="简历附件" prop="attachment">
              <el-input v-model="resumeForm.attachment" placeholder="简历附件URL" />
            </el-form-item>
          </el-form>
        </el-tab-pane> -->
      </el-tabs>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getProfileInfo, updateProfileInfo } from '@/api'

export default defineComponent({
  name: 'Profile',
  setup() {
    const loading = ref(false)
    const saveLoading = ref(false)
    const activeTab = ref('basic')
    
    // 表单引用
    const basicFormRef = ref<any>(null)
    const socialFormRef = ref<any>(null)
    const resumeFormRef = ref<any>(null)
    
    // 基本信息表单
    const basicForm = reactive({
      id: null as number | null,
      name: '',
      avatar: '',
      profession: '',
      bio: '',
      email: '',
      phone: '',
      address: '',
      birthday: ''
    })
    
    // 社交链接表单
    const socialForm = reactive({
      github: '',
      linkedin: '',
      twitter: '',
      wechat: '',
      website: '',
      other_links: [] as { name: string; url: string }[]
    })
    
    // 简历表单
    const resumeForm = reactive({
      title: '',
      content: '',
      attachment: ''
    })
    
    // 基本信息验证规则
    const basicRules = {
      name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ]
    }
    
    // 添加其他链接
    const addLink = () => {
      socialForm.other_links.push({ name: '', url: '' })
    }
    
    // 移除其他链接
    const removeLink = (index: number) => {
      socialForm.other_links.splice(index, 1)
    }
    
    // 获取个人资料信息
    const getProfile = async () => {
      loading.value = true
      try {
        const res = await getProfileInfo() as any
        console.log('获取到的个人资料数据:', res)
        
        if (res) {
          // 映射后端字段到前端表单
          basicForm.id = res.id || null
          basicForm.name = res.username || ''
          basicForm.avatar = res.avatar_url || ''
          basicForm.bio = res.bio || ''
          basicForm.email = res.email || ''
          basicForm.profession = res.identity || ''
          
          // 映射社交链接
          socialForm.github = res.github_url || ''
          
          // 如果需要其他字段，可以在这里添加映射
          console.log('表单数据已更新:', { basicForm, socialForm })
        }
      } catch (error) {
        ElMessage.error('获取个人资料失败')
        console.error('获取个人资料失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    // 保存个人资料
    const handleSave = async () => {
      if (activeTab.value === 'basic' && basicFormRef.value) {
        try {
          await basicFormRef.value.validate()
        } catch (error) {
          return
        }
      }
      
      saveLoading.value = true
      
      try {
        // 根据后端模型字段构建数据
        const profileData = {
          name: basicForm.name,  // 前端使用name，后端映射到username
          avatar: basicForm.avatar,  // 前端使用avatar，后端映射到avatar_url
          bio: basicForm.bio,
          email: basicForm.email,
          profession: basicForm.profession,  // 前端使用profession，后端映射到identity
          github_url: socialForm.github,
          github_username: socialForm.github ? socialForm.github.split('/').pop() : ''
        }
        
        console.log('准备发送的个人资料数据:', profileData)
        
        await updateProfileInfo(profileData)
        ElMessage.success('个人资料更新成功')
      } catch (error) {
        ElMessage.error('个人资料更新失败')
        console.error('更新个人资料失败:', error)
      } finally {
        saveLoading.value = false
      }
    }
    
    onMounted(() => {
      getProfile()
    })
    
    return {
      loading,
      saveLoading,
      activeTab,
      basicForm,
      socialForm,
      resumeForm,
      basicRules,
      basicFormRef,
      socialFormRef,
      resumeFormRef,
      addLink,
      removeLink,
      handleSave
    }
  }
})
</script>

<style scoped>
.profile-container {
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

.other-link {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
</style> 