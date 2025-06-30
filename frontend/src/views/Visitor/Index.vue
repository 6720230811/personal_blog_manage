·<template>
  <div class="visitor-container">
    <div class="page-header">
      <h2>访客统计</h2>
    </div>

    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-number">{{ overview.total_visitors }}</div>
          <div class="stat-title">总访客数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-number">{{ overview.total_pageviews }}</div>
          <div class="stat-title">总浏览量</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-number">{{ overview.today_visitors }}</div>
          <div class="stat-title">今日访客</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-number">{{ overview.today_pageviews }}</div>
          <div class="stat-title">今日浏览量</div>
        </el-card>
      </el-col>
    </el-row>

    <div class="chart-container">
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card class="chart-card" v-loading="loadingChart">
            <div class="chart-header">
              <h3>访问量趋势</h3>
              <el-radio-group v-model="timeRange" size="small" @change="handleRangeChange">
                <el-radio-button label="week">近7天</el-radio-button>
                <el-radio-button label="month">近30天</el-radio-button>
                <el-radio-button label="year">近一年</el-radio-button>
              </el-radio-group>
            </div>
            <div ref="visitorChart" class="chart"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="data-section">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="chart-card" v-loading="loadingDevices">
            <h3>设备类型分布</h3>
            <div ref="deviceChart" class="pie-chart"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="chart-card" v-loading="loadingBrowsers">
            <h3>浏览器分布</h3>
            <div ref="browserChart" class="pie-chart"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="data-section">
      <el-card v-loading="loadingTable">
        <div class="table-header">
          <h3>热门页面</h3>
          <el-input
            v-model="searchQuery"
            placeholder="搜索页面"
            suffix-icon="el-icon-search"
            style="width: 250px"
            clearable
          />
        </div>
        
        <el-table
          :data="filteredPageData"
          border
          style="width: 100%"
        >
          <el-table-column prop="page_url" label="页面路径" min-width="250" />
          <el-table-column prop="page_title" label="页面标题" min-width="250" />
          <el-table-column prop="views" label="浏览量" width="120" align="center" />
          <el-table-column prop="unique_visitors" label="独立访客" width="120" align="center" />
          <el-table-column prop="avg_time" label="平均停留时间" width="150" align="center" />
          <el-table-column prop="bounce_rate" label="跳出率" width="120" align="center">
            <template #default="{ row }">
              {{ row.bounce_rate }}%
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination-container">
          <el-pagination
            background
            layout="total, sizes, prev, pager, next"
            :current-page="currentPage"
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pageSize"
            :total="totalPages"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getVisitorOverview, getVisitorTrends, getDeviceStats, getBrowserStats, getPageViewStats } from '@/api'

export default defineComponent({
  name: 'VisitorStats',
  setup() {
    // 图表引用
    const visitorChart = ref<HTMLDivElement | null>(null)
    const deviceChart = ref<HTMLDivElement | null>(null)
    const browserChart = ref<HTMLDivElement | null>(null)
    
    // 图表实例
    let visitorChartInstance: echarts.ECharts | null = null
    let deviceChartInstance: echarts.ECharts | null = null
    let browserChartInstance: echarts.ECharts | null = null
    
    // 加载状态
    const loadingChart = ref(false)
    const loadingDevices = ref(false)
    const loadingBrowsers = ref(false)
    const loadingTable = ref(false)
    
    // 时间范围选择
    const timeRange = ref('week')
    
    // 页面数据
    const pageData = ref<any[]>([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalPages = ref(0)
    const searchQuery = ref('')
    
    // 统计概览数据
    const overview = reactive({
      total_visitors: 0,
      total_pageviews: 0,
      today_visitors: 0,
      today_pageviews: 0
    })
    
    // 过滤后的页面数据
    const filteredPageData = computed(() => {
      if (!searchQuery.value) {
        return pageData.value
      }
      
      const query = searchQuery.value.toLowerCase()
      return pageData.value.filter(item => {
        return item.page_url.toLowerCase().includes(query) || 
               (item.page_title && item.page_title.toLowerCase().includes(query))
      })
    })
    
    // 初始化访客趋势图表
    const initVisitorChart = () => {
      if (visitorChart.value) {
        visitorChartInstance = echarts.init(visitorChart.value)
        
        const option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: ['访客数', '浏览量']
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: []
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '访客数',
              type: 'line',
              data: [],
              smooth: true
            },
            {
              name: '浏览量',
              type: 'bar',
              data: []
            }
          ]
        }
        
        visitorChartInstance.setOption(option as any)
        
        // 监听窗口大小变化，调整图表大小
        window.addEventListener('resize', () => {
          visitorChartInstance?.resize()
        })
      }
    }
    
    // 初始化设备类型图表
    const initDeviceChart = () => {
      if (deviceChart.value) {
        deviceChartInstance = echarts.init(deviceChart.value)
        
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 10,
            data: []
          },
          series: [
            {
              name: '设备类型',
              type: 'pie',
              radius: ['50%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: false,
                position: 'center'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 14,
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              data: []
            }
          ]
        }
        
        deviceChartInstance.setOption(option as any)
        
        window.addEventListener('resize', () => {
          deviceChartInstance?.resize()
        })
      }
    }
    
    // 初始化浏览器图表
    const initBrowserChart = () => {
      if (browserChart.value) {
        browserChartInstance = echarts.init(browserChart.value)
        
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 10,
            data: []
          },
          series: [
            {
              name: '浏览器',
              type: 'pie',
              radius: ['50%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: false,
                position: 'center'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 14,
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              data: []
            }
          ]
        }
        
        browserChartInstance.setOption(option as any)
        
        window.addEventListener('resize', () => {
          browserChartInstance?.resize()
        })
      }
    }
    
    // 获取访问概况
    const fetchVisitorOverview = async () => {
      try {
        const res = await getVisitorOverview() as any
        if (res) {
          overview.total_visitors = res.total_visitors || 0
          overview.total_pageviews = res.total_pageviews || 0
          overview.today_visitors = res.today_visitors || 0
          overview.today_pageviews = res.today_pageviews || 0
        }
      } catch (error) {
        console.error('获取访问概况失败:', error)
      }
    }
    
    // 获取访问趋势
    const fetchVisitorTrends = async () => {
      loadingChart.value = true
      
      try {
        const res = await getVisitorTrends({ range: timeRange.value }) as any
        
        if (res && res.data) {
          // 更新图表数据
          visitorChartInstance?.setOption({
            xAxis: {
              data: res.data.dates
            },
            series: [
              {
                name: '访客数',
                data: res.data.visitors
              },
              {
                name: '浏览量',
                data: res.data.pageviews
              }
            ]
          })
        }
      } catch (error) {
        console.error('获取访问趋势失败:', error)
      } finally {
        loadingChart.value = false
      }
    }
    
    // 获取设备统计
    const fetchDeviceStats = async () => {
      loadingDevices.value = true
      
      try {
        const res = await getDeviceStats() as any
        
        if (res && res.data) {
          const legendData = res.data.map((item: any) => item.name)
          
          // 更新图表数据
          deviceChartInstance?.setOption({
            legend: {
              data: legendData
            },
            series: [
              {
                name: '设备类型',
                data: res.data
              }
            ]
          })
        }
      } catch (error) {
        console.error('获取设备统计失败:', error)
      } finally {
        loadingDevices.value = false
      }
    }
    
    // 获取浏览器统计
    const fetchBrowserStats = async () => {
      loadingBrowsers.value = true
      
      try {
        const res = await getBrowserStats() as any
        
        if (res && res.data) {
          const legendData = res.data.map((item: any) => item.name)
          
          // 更新图表数据
          browserChartInstance?.setOption({
            legend: {
              data: legendData
            },
            series: [
              {
                name: '浏览器',
                data: res.data
              }
            ]
          })
        }
      } catch (error) {
        console.error('获取浏览器统计失败:', error)
      } finally {
        loadingBrowsers.value = false
      }
    }
    
    // 获取页面数据
    const fetchPageStats = async () => {
      loadingTable.value = true
      
      try {
        const res = await getPageViewStats({
          page: currentPage.value,
          page_size: pageSize.value
        }) as any
        
        if (res) {
          pageData.value = res.results || []
          totalPages.value = res.count || 0
        }
      } catch (error) {
        ElMessage.error('获取页面数据失败')
        console.error('获取页面数据失败:', error)
      } finally {
        loadingTable.value = false
      }
    }
    
    // 处理时间范围变化
    const handleRangeChange = () => {
      fetchVisitorTrends()
    }
    
    // 处理页码变化
    const handleCurrentChange = (val: number) => {
      currentPage.value = val
      fetchPageStats()
    }
    
    // 处理每页显示数量变化
    const handleSizeChange = (val: number) => {
      pageSize.value = val
      currentPage.value = 1
      fetchPageStats()
    }
    
    onMounted(() => {
      // 初始化并加载数据
      nextTick(() => {
        initVisitorChart()
        initDeviceChart()
        initBrowserChart()
        
        fetchVisitorOverview()
        fetchVisitorTrends()
        fetchDeviceStats()
        fetchBrowserStats()
        fetchPageStats()
      })
    })
    
    return {
      visitorChart,
      deviceChart,
      browserChart,
      loadingChart,
      loadingDevices,
      loadingBrowsers,
      loadingTable,
      timeRange,
      overview,
      pageData,
      filteredPageData,
      currentPage,
      pageSize,
      totalPages,
      searchQuery,
      handleRangeChange,
      handleCurrentChange,
      handleSizeChange
    }
  }
})
</script>

<style scoped>
.visitor-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.stat-card {
  text-align: center;
  padding: 20px 0;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
}

.stat-title {
  font-size: 16px;
  color: #606266;
  margin-top: 10px;
}

.chart-container {
  margin-top: 20px;
}

.data-section {
  margin-top: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.chart-header h3 {
  margin: 0;
}

.chart {
  height: 350px;
}

.pie-chart {
  height: 300px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.table-header h3 {
  margin: 0;
}

.pagination-container {
  margin-top: 15px;
  text-align: right;
}
</style> 