<template>
  <div class="not-found-container">
    <h1>404</h1>
    <h2>页面不存在</h2>
    <p>您访问的页面不存在或已被删除</p>
    <el-button type="primary" @click="router.push('/')">返回首页</el-button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'NotFound',
  setup() {
    const router = useRouter()
    
    return {
      router
    }
  }
})
</script>

<style scoped>
.not-found-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

h1 {
  font-size: 100px;
  color: #409EFF;
  margin: 0;
}

h2 {
  font-size: 36px;
  margin: 10px 0;
}

p {
  font-size: 18px;
  color: #606266;
  margin-bottom: 30px;
}
</style> 