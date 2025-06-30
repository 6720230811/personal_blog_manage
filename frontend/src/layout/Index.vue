<template>
  <div class="layout-container">
    <el-container>
      <el-aside :width="isCollapse ? '64px' : '200px'" class="aside-container">
        <div class="logo-container">
          <h2 v-if="!isCollapse">博客管理系统</h2>
          <h2 v-else>博</h2>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical"
          :collapse="isCollapse"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
          router
        >
          <el-menu-item index="/dashboard">
            <el-icon><el-icon-odometer /></el-icon>
            <template #title>仪表盘</template>
          </el-menu-item>
          
          <el-sub-menu index="/blog">
            <template #title>
              <el-icon><el-icon-notebook /></el-icon>
              <span>博客管理</span>
            </template>
            <el-menu-item index="/blog">博客列表</el-menu-item>
            <el-menu-item index="/blog/add">添加博客</el-menu-item>
          </el-sub-menu>
          
          <el-menu-item index="/project">
            <el-icon><el-icon-folder /></el-icon>
            <template #title>项目管理</template>
          </el-menu-item>
          
          <el-menu-item index="/skill">
            <el-icon><el-icon-opportunity /></el-icon>
            <template #title>技能管理</template>
          </el-menu-item>
          
          <el-menu-item index="/education">
            <el-icon><el-icon-school /></el-icon>
            <template #title>教育经历</template>
          </el-menu-item>
          
          <el-menu-item index="/work">
            <el-icon><el-icon-suitcase /></el-icon>
            <template #title>工作经历</template>
          </el-menu-item>
          
          <el-menu-item index="/achievement">
            <el-icon><el-icon-trophy /></el-icon>
            <template #title>成就管理</template>
          </el-menu-item>
          
          <el-menu-item index="/profile">
            <el-icon><el-icon-user /></el-icon>
            <template #title>个人信息</template>
          </el-menu-item>
          
          <el-menu-item index="/visitor">
            <el-icon><el-icon-data-line /></el-icon>
            <template #title>访客统计</template>
          </el-menu-item>
          
          <el-menu-item index="/setting">
            <el-icon><el-icon-setting /></el-icon>
            <template #title>系统设置</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header class="header">
          <div class="header-left">
            <el-button type="text" @click="toggleSidebar">
              <el-icon><el-icon-fold v-if="!isCollapse" /><el-icon-expand v-else /></el-icon>
            </el-button>
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item v-if="route.meta.title">{{ route.meta.title }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <el-dropdown trigger="click" @command="handleCommand">
              <div class="avatar-container">
                <span>管理员</span>
                <el-icon><el-icon-caret-bottom /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                  <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
// @ts-ignore
import { useStore } from 'vuex'

export default defineComponent({
  name: 'Layout',
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    
    const isCollapse = computed(() => store.state.isCollapse)
    
    const activeMenu = computed(() => {
      return route.path
    })
    
    const toggleSidebar = () => {
      store.dispatch('toggleSidebar')
    }
    
    const handleCommand = (command: string) => {
      if (command === 'logout') {
        store.dispatch('logout')
        router.push('/login')
      } else if (command === 'profile') {
        router.push('/profile')
      }
    }
    
    return {
      isCollapse,
      activeMenu,
      toggleSidebar,
      handleCommand,
      route
    }
  }
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
  min-height: 100vh;
}

.aside-container {
  background-color: #304156;
  transition: width 0.3s;
  overflow: hidden;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  background-color: #2b3649;
}

.header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.avatar-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.avatar-container span {
  margin-right: 5px;
}

.el-menu-vertical:not(.el-menu--collapse) {
  width: 200px;
}

.el-menu {
  border-right: none;
}
</style> 