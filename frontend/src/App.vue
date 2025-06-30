<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background: #f5f7fa;
}

.app-container {
  width: 100%;
  height: 100vh;
}

/* 确保下拉菜单正确显示 */
.el-popper {
  z-index: 9999 !important;
  min-width: 160px !important;
}

.el-select__popper {
  z-index: 9999 !important;
  min-width: 160px !important;
}

.el-select-dropdown {
  z-index: 9999 !important;
  min-width: 160px !important;
}

/* 调整下拉选项的宽度 */
.blog-select-dropdown {
  min-width: 160px !important;
}

/* 确保下拉选项文字不会被截断 */
.el-select-dropdown__item {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 20px;
}
</style> 