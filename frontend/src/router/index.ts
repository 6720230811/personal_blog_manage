import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/',
    component: () => import('../layout/Index.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '仪表盘', icon: 'el-icon-s-home' }
      },
      {
        path: 'blog',
        name: 'Blog',
        component: () => import('../views/Blog/Index.vue'),
        meta: { title: '博客管理', icon: 'el-icon-notebook-1' }
      },
      {
        path: 'blog/add',
        name: 'AddBlog',
        component: () => import('../views/Blog/Add.vue'),
        meta: { title: '添加博客', icon: 'el-icon-plus' }
      },
      {
        path: 'blog/edit/:id',
        name: 'EditBlog',
        component: () => import('../views/Blog/Edit.vue'),
        meta: { title: '编辑博客', icon: 'el-icon-edit' },
        props: true
      },
      {
        path: 'project',
        name: 'Project',
        component: () => import('../views/Project/Index.vue'),
        meta: { title: '项目管理', icon: 'el-icon-folder' }
      },
      {
        path: 'skill',
        name: 'Skill',
        component: () => import('../views/Skill/Index.vue'),
        meta: { title: '技能管理', icon: 'el-icon-s-opportunity' }
      },
      {
        path: 'education',
        name: 'Education',
        component: () => import('../views/Education/Index.vue'),
        meta: { title: '教育经历', icon: 'el-icon-school' }
      },
      {
        path: 'work',
        name: 'Work',
        component: () => import('../views/Work/Index.vue'),
        meta: { title: '工作经历', icon: 'el-icon-suitcase' }
      },
      {
        path: 'achievement',
        name: 'Achievement',
        component: () => import('../views/Achievement/Index.vue'),
        meta: { title: '成就管理', icon: 'el-icon-trophy' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/Profile/Index.vue'),
        meta: { title: '个人信息', icon: 'el-icon-user' }
      },
      {
        path: 'visitor',
        name: 'Visitor',
        component: () => import('../views/Visitor/Index.vue'),
        meta: { title: '访客统计', icon: 'el-icon-s-data' }
      },
      {
        path: 'setting',
        name: 'Setting',
        component: () => import('../views/Setting/Index.vue'),
        meta: { title: '系统设置', icon: 'el-icon-setting' }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: '404' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 个人博客后台管理系统`
  }

  // 检查是否有token，除了登录页面其他页面都需要登录
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router 