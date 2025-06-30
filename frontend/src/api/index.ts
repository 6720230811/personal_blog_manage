import request from './request'
import axios from 'axios'

// 登录相关
export const login = (data: { username: string; password: string }) => {
  return request({
    url: '/login/',
    method: 'post',
    data
  })
}

// 博客相关
export const getBlogList = (params?: any) => {
  return request({
    url: '/blogs/',
    method: 'get',
    params
  })
}

export const getBlogDetail = (id: number) => {
  console.log(`获取博客详情API调用，ID: ${id}`)
  return request({
    url: `/blogs/${id}/`,
    method: 'get'
  }).then(res => {
    console.log(`获取博客详情API返回:`, res)
    return res
  }).catch(error => {
    console.error(`获取博客详情API错误:`, error)
    throw error
  })
}

export const createBlog = (data: any) => {
  return request({
    url: '/blogs/',
    method: 'post',
    data
  })
}

export const updateBlog = (id: number, data: any) => {
  console.log(`更新博客API调用，ID: ${id}，数据:`, data)
  return request({
    url: `/blogs/${id}/`,
    method: 'put',
    data
  }).then(res => {
    console.log(`更新博客API返回:`, res)
    return res
  }).catch(error => {
    console.error(`更新博客API错误:`, error)
    throw error
  })
}

export const deleteBlog = (id: number) => {
  return request({
    url: `/blogs/${id}/`,
    method: 'delete'
  })
}

// 博客标签相关
export const getBlogTagList = () => {
  return request({
    url: '/blog-tags/',
    method: 'get'
  })
}

export const addBlogTag = (data: any) => {
  return request({
    url: '/blog-tags/',
    method: 'post',
    data
  })
}

export const addTagToBlog = (blogId: number, tagId: number) => {
  console.log(`添加标签到博客API调用，博客ID: ${blogId}，标签ID: ${tagId}`)
  return request({
    url: `/blogs/${blogId}/add_tag/`,
    method: 'post',
    data: { tag_id: tagId }
  }).then(res => {
    console.log(`添加标签到博客API返回:`, res)
    return res
  }).catch(error => {
    console.error(`添加标签到博客API错误:`, error)
    throw error
  })
}

export const removeTagFromBlog = (blogId: number, tagId: number) => {
  console.log(`从博客移除标签API调用，博客ID: ${blogId}，标签ID: ${tagId}`)
  return request({
    url: `/blogs/${blogId}/remove_tag/`,
    method: 'post',
    data: { tag_id: tagId }
  }).then(res => {
    console.log(`从博客移除标签API返回:`, res)
    return res
  }).catch(error => {
    console.error(`从博客移除标签API错误:`, error)
    throw error
  })
}

// 项目相关
export const getProjectList = (params?: any) => {
  return request({
    url: '/projects/',
    method: 'get',
    params
  })
}

export const getProjectDetail = (id: number) => {
  return request({
    url: `/projects/${id}/`,
    method: 'get'
  })
}

export const createProject = (data: any) => {
  return request({
    url: '/projects/',
    method: 'post',
    data
  })
}

export const updateProject = (id: number, data: any) => {
  return request({
    url: `/projects/${id}/`,
    method: 'put',
    data
  })
}

export const deleteProject = (id: number) => {
  return request({
    url: `/projects/${id}/`,
    method: 'delete'
  })
}

// 项目标签相关
export const getProjectTagList = () => {
  return request({
    url: '/project-tags/',
    method: 'get'
  })
}

export const addProjectTag = (data: any) => {
  return request({
    url: '/project-tags/',
    method: 'post',
    data
  })
}

export const addTagToProject = (projectId: number, tagId: number) => {
  console.log(`添加标签到项目API调用，项目ID: ${projectId}，标签ID: ${tagId}`)
  return request({
    url: `/projects/${projectId}/add_tag/`,
    method: 'post',
    data: { tag_id: tagId }
  }).then(res => {
    console.log(`添加标签到项目API返回:`, res)
    return res
  }).catch(error => {
    console.error(`添加标签到项目API错误:`, error)
    throw error
  })
}

export const removeTagFromProject = (projectId: number, tagId: number) => {
  console.log(`从项目移除标签API调用，项目ID: ${projectId}，标签ID: ${tagId}`)
  return request({
    url: `/projects/${projectId}/remove_tag/`,
    method: 'post',
    data: { tag_id: tagId }
  }).then(res => {
    console.log(`从项目移除标签API返回:`, res)
    return res
  }).catch(error => {
    console.error(`从项目移除标签API错误:`, error)
    throw error
  })
}

// 技能相关
export const getSkillList = (params?: any) => {
  return request({
    url: '/skills/',
    method: 'get',
    params
  })
}

export const createSkill = (data: any) => {
  return request({
    url: '/skills/',
    method: 'post',
    data
  })
}

export const updateSkill = (id: number, data: any) => {
  return request({
    url: `/skills/${id}/`,
    method: 'put',
    data
  })
}

export const deleteSkill = (id: number) => {
  return request({
    url: `/skills/${id}/`,
    method: 'delete'
  })
}

// 教育经历相关
export const getEducationList = (params?: any) => {
  return request({
    url: '/education/',
    method: 'get',
    params
  })
}

export const createEducation = (data: any) => {
  return request({
    url: '/education/',
    method: 'post',
    data
  })
}

export const updateEducation = (id: number, data: any) => {
  return request({
    url: `/education/${id}/`,
    method: 'put',
    data
  })
}

export const deleteEducation = (id: number) => {
  return request({
    url: `/education/${id}/`,
    method: 'delete'
  })
}

// 工作经历相关
export const getWorkList = (params?: any) => {
  return request({
    url: '/work-experiences/',
    method: 'get',
    params
  })
}

export const createWork = (data: any) => {
  return request({
    url: '/work-experiences/',
    method: 'post',
    data
  })
}

export const updateWork = (id: number, data: any) => {
  return request({
    url: `/work-experiences/${id}/`,
    method: 'put',
    data
  })
}

export const deleteWork = (id: number) => {
  return request({
    url: `/work-experiences/${id}/`,
    method: 'delete'
  })
}

// 成就相关
export const getAchievementList = (params?: any) => {
  return request({
    url: '/achievements/',
    method: 'get',
    params
  })
}

export const createAchievement = (data: any) => {
  return request({
    url: '/achievements/',
    method: 'post',
    data
  })
}

export const updateAchievement = (id: number, data: any) => {
  return request({
    url: `/achievements/${id}/`,
    method: 'put',
    data
  })
}

export const deleteAchievement = (id: number) => {
  return request({
    url: `/achievements/${id}/`,
    method: 'delete'
  })
}

// 个人资料相关
export const getProfileInfo = () => {
  console.log('调用获取个人资料API')
  return request({
    url: '/blog-owner/1/',
    method: 'get'
  }).then(res => {
    console.log('获取个人资料返回数据:', res)
    return res
  }).catch(error => {
    console.error('获取个人资料失败:', error)
    throw error
  })
}

export const updateProfileInfo = (data: any) => {
  return request({
    url: '/blog-owner/update_profile/',
    method: 'put',
    data
  })
}

// 系统设置相关
export const getSystemSettings = () => {
  return request({
    url: '/settings/',
    method: 'get'
  })
}

export const updateSystemSettings = (data: any) => {
  return request({
    url: '/settings/update/',
    method: 'put',
    data
  })
}

// 测试邮件设置
export const testEmailSettings = (data: any) => {
  return request({
    url: '/settings/test-email/',
    method: 'post',
    data
  })
}

// 清除系统缓存
export const clearSystemCache = (data: any) => {
  return request({
    url: '/settings/clear-cache/',
    method: 'post',
    data
  })
}

// 备份数据库
export const backupSystemDatabase = () => {
  return request({
    url: '/settings/backup-database/',
    method: 'post'
  })
}

// 获取系统日志列表
export const getSystemLogs = () => {
  return request({
    url: '/settings/logs/',
    method: 'get'
  })
}

// 获取系统日志内容
export const getSystemLogContent = (params: any) => {
  return request({
    url: '/settings/logs/content/',
    method: 'get',
    params
  })
}

// 访客统计相关
export const getVisitorOverview = () => {
  return request({
    url: '/visitor-stats/overview/',
    method: 'get'
  })
}

export const getVisitorTrends = (params: any) => {
  return request({
    url: '/visitor-stats/trends/',
    method: 'get',
    params
  })
}

export const getDeviceStats = () => {
  return request({
    url: '/visitor-stats/devices/',
    method: 'get'
  })
}

export const getBrowserStats = () => {
  return request({
    url: '/visitor-stats/browsers/',
    method: 'get'
  })
}

export const getPageViewStats = (params: any) => {
  return request({
    url: '/visitor-stats/pages/',
    method: 'get',
    params
  })
}
// 访客详情
export const getVisitorList = (params?: any) => {
  return request({
    url: '/visitors/',
    method: 'get',
    params
  })
}

// 在 axios 配置中
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

