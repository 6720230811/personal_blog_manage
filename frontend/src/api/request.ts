import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const request = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

// 请求拦截
request.interceptors.request.use(
  config => {
    console.log(`发送请求: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`, config)
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截
request.interceptors.response.use(
  response => {
    console.log(`请求成功: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data)
    return response.data
  },
  error => {
    console.error('请求失败:', error)
    console.error('请求配置:', error.config)
    
    if (error.response) {
      console.error('响应状态:', error.response.status)
      console.error('响应数据:', error.response.data)
      
      switch (error.response.status) {
        case 401:
          ElMessage.error('未授权，请登录')
          localStorage.removeItem('token')
          router.push('/login')
          break
        case 403:
          ElMessage.error('拒绝访问')
          break
        case 404:
          ElMessage.error(`请求地址出错: ${error.config?.url}`)
          break
        case 500:
          ElMessage.error(`服务器内部错误: ${error.response.data?.detail || ''}`)
          break
        default:
          ElMessage.error(`未知错误: ${error.response.status}`)
      }
    } else if (error.request) {
      console.error('请求已发送但未收到响应')
      ElMessage.error('网络错误，服务器未响应')
    } else {
      console.error('请求设置错误:', error.message)
      ElMessage.error(`请求设置错误: ${error.message}`)
    }
    return Promise.reject(error)
  }
)

export default request 