<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <h2>博客管理系统</h2>
        </div>
      </template>
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="0">
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="用户名" 
            autocomplete="off"
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            placeholder="密码" 
            type="password"
            show-password
            autocomplete="off"
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="loading" 
            class="login-button" 
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
// @ts-ignore
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { login } from '@/api'

export default defineComponent({
  name: 'Login',
  components: {
    User,
    Lock
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const loading = ref(false)
    const loginForm = reactive({
      username: '',
      password: ''
    })
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    }
    
    const loginFormRef = ref<any>(null)
    
    const handleLogin = () => {
      if (!loginFormRef.value) return
      
      loginFormRef.value.validate((valid: boolean) => {
        if (!valid) return
        
        loading.value = true
        
        login(loginForm)
          .then((res: any) => {
            // 注意: API 响应已经在 axios.ts 中被转换为直接的数据 (response.data)
            if (res && res.access) {
              store.dispatch('login', {
                token: res.access,
                refreshToken: res.refresh,
                user: res.user || { username: loginForm.username }
              })
              ElMessage({
                message: '登录成功',
                type: 'success'
              })
              router.push('/')
            } else {
              ElMessage.error('登录失败，请检查用户名和密码')
            }
          })
          .catch(error => {
            ElMessage.error('登录失败，请稍后重试')
            console.error(error)
          })
          .finally(() => {
            loading.value = false
          })
      })
    }
    
    return {
      loginForm,
      loginRules,
      loading,
      loginFormRef,
      handleLogin
    }
  }
})
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f3f4f6;
}

.login-card {
  width: 400px;
}

.login-header {
  text-align: center;
}

.login-button {
  width: 100%;
}
</style> 