
&lt;template&gt;
  &lt;div class="report-container"&gt;
    &lt;el-card class="box-card"&gt;
      &lt;template #header&gt;
        &lt;div class="card-header"&gt;
          &lt;span&gt;报表分析&lt;/span&gt;
        &lt;/div&gt;
      &lt;/template&gt;
      
      &lt;el-row :gutter="20" class="stats-row"&gt;
        &lt;el-col :span="6"&gt;
          &lt;el-card class="stat-card"&gt;
            &lt;div class="stat-content"&gt;
              &lt;div class="stat-value"&gt;{{ stats.total_users }}&lt;/div&gt;
              &lt;div class="stat-label"&gt;用户总数&lt;/div&gt;
              &lt;div class="stat-trend"&gt;今日新增: {{ stats.today_users }}&lt;/div&gt;
            &lt;/div&gt;
          &lt;/el-card&gt;
        &lt;/el-col&gt;
        &lt;el-col :span="6"&gt;
          &lt;el-card class="stat-card"&gt;
            &lt;div class="stat-content"&gt;
              &lt;div class="stat-value"&gt;{{ stats.total_orders }}&lt;/div&gt;
              &lt;div class="stat-label"&gt;订单总数&lt;/div&gt;
              &lt;div class="stat-trend"&gt;今日订单: {{ stats.today_orders }}&lt;/div&gt;
            &lt;/div&gt;
          &lt;/el-card&gt;
        &lt;/el-col&gt;
        &lt;el-col :span="6"&gt;
          &lt;el-card class="stat-card"&gt;
            &lt;div class="stat-content"&gt;
              &lt;div class="stat-value"&gt;¥{{ stats.total_sales.toFixed(2) }}&lt;/div&gt;
              &lt;div class="stat-label"&gt;销售总额&lt;/div&gt;
              &lt;div class="stat-trend"&gt;今日销售: ¥{{ stats.today_sales.toFixed(2) }}&lt;/div&gt;
            &lt;/div&gt;
          &lt;/el-card&gt;
        &lt;/el-col&gt;
        &lt;el-col :span="6"&gt;
          &lt;el-card class="stat-card"&gt;
            &lt;div class="stat-content"&gt;
              &lt;div class="stat-value"&gt;{{ stats.total_products }}&lt;/div&gt;
              &lt;div class="stat-label"&gt;商品总数&lt;/div&gt;
              &lt;div class="stat-trend"&gt;上架商品: {{ stats.on_sale_products }}&lt;/div&gt;
            &lt;/div&gt;
          &lt;/el-card&gt;
        &lt;/el-col&gt;
      &lt;/el-row&gt;

      &lt;el-row :gutter="20" class="charts-row"&gt;
        &lt;el-col :span="12"&gt;
          &lt;el-card&gt;
            &lt;template #header&gt;
              &lt;div class="card-header"&gt;
                &lt;span&gt;销售趋势&lt;/span&gt;
              &lt;/div&gt;
            &lt;/template&gt;
            &lt;div ref="salesTrendRef" class="chart-container"&gt;&lt;/div&gt;
          &lt;/el-card&gt;
        &lt;/el-col&gt;
        &lt;el-col :span="12"&gt;
          &lt;el-card&gt;
            &lt;template #header&gt;
              &lt;div class="card-header"&gt;
                &lt;span&gt;用户增长&lt;/span&gt;
              &lt;/div&gt;
            &lt;/template&gt;
            &lt;div ref="userGrowthRef" class="chart-container"&gt;&lt;/div&gt;
          &lt;/el-card&gt;
        &lt;/el-col&gt;
      &lt;/el-row&gt;

      &lt;el-row :gutter="20" class="charts-row"&gt;
        &lt;el-col :span="12"&gt;
          &lt;el-card&gt;
            &lt;template #header&gt;
              &lt;div class="card-header"&gt;
                &lt;span&gt;订单状态统计&lt;/span&gt;
              &lt;/div&gt;
            &lt;/template&gt;
            &lt;div ref="orderStatsRef" class="chart-container"&gt;&lt;/div&gt;
          &lt;/el-card&gt;
        &lt;/el-col&gt;
        &lt;el-col :span="12"&gt;
          &lt;el-card&gt;
            &lt;template #header&gt;
              &lt;div class="card-header"&gt;
                &lt;span&gt;最近订单&lt;/span&gt;
              &lt;/div&gt;
            &lt;/template&gt;
            &lt;el-table :data="recentOrders" style="width: 100%"&gt;
              &lt;el-table-column prop="order_no" label="订单号" width="120" /&gt;
              &lt;el-table-column prop="total_amount" label="金额" width="100"&gt;
                &lt;template #default="{ row }"&gt;
                  ¥{{ row.total_amount.toFixed(2) }}
                &lt;/template&gt;
              &lt;/el-table-column&gt;
              &lt;el-table-column prop="status" label="状态"&gt;
                &lt;template #default="{ row }"&gt;
                  &lt;el-tag :type="getStatusType(row.status)"&gt;{{ getStatusText(row.status) }}&lt;/el-tag&gt;
                &lt;/template&gt;
              &lt;/el-table-column&gt;
            &lt;/el-table&gt;
          &lt;/el-card&gt;
        &lt;/el-col&gt;
      &lt;/el-row&gt;
    &lt;/el-card&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStats, getSalesTrend, getUserGrowth, getOrderStats } from '@/api/report'
import type { DashboardStats, SalesTrendResponse, UserGrowthResponse, OrderStatsResponse } from '@/api/report'

const stats = ref&lt;DashboardStats&gt;({
  total_users: 0,
  today_users: 0,
  total_orders: 0,
  today_orders: 0,
  total_products: 0,
  on_sale_products: 0,
  total_sales: 0,
  today_sales: 0
})

const salesTrendRef = ref&lt;HTMLElement&gt;()
const userGrowthRef = ref&lt;HTMLElement&gt;()
const orderStatsRef = ref&lt;HTMLElement&gt;()

let salesTrendChart: echarts.ECharts | null = null
let userGrowthChart: echarts.ECharts | null = null
let orderStatsChart: echarts.ECharts | null = null

const recentOrders = ref&lt;any[]&gt;([])

const getStatusType = (status: string) =&gt; {
  const types: Record&lt;string, any&gt; = {
    completed: 'success',
    shipped: 'warning',
    paid: 'primary'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) =&gt; {
  const texts: Record&lt;string, string&gt; = {
    completed: '已完成',
    shipped: '已发货',
    paid: '已支付'
  }
  return texts[status] || status
}

const loadStats = async () =&gt; {
  try {
    const res = await getDashboardStats()
    if (res.data) {
      stats.value = res.data
    }
  } catch (error) {
    console.error('加载统计数据失败', error)
  }
}

const loadSalesTrend = async () =&gt; {
  try {
    const res = await getSalesTrend(7)
    if (res.data &amp;&amp; salesTrendChart) {
      const data: SalesTrendResponse = res.data
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['销售额', '订单数']
        },
        xAxis: {
          type: 'category',
          data: data.trend.map(item =&gt; item.date)
        },
        yAxis: [
          {
            type: 'value',
            name: '销售额',
            position: 'left'
          },
          {
            type: 'value',
            name: '订单数',
            position: 'right'
          }
        ],
        series: [
          {
            name: '销售额',
            type: 'line',
            data: data.trend.map(item =&gt; item.amount),
            smooth: true
          },
          {
            name: '订单数',
            type: 'bar',
            yAxisIndex: 1,
            data: data.trend.map(item =&gt; item.order_count)
          }
        ]
      }
      salesTrendChart.setOption(option)
    }
  } catch (error) {
    console.error('加载销售趋势失败', error)
  }
}

const loadUserGrowth = async () =&gt; {
  try {
    const res = await getUserGrowth(7)
    if (res.data &amp;&amp; userGrowthChart) {
      const data: UserGrowthResponse = res.data
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['新增用户', '累计用户']
        },
        xAxis: {
          type: 'category',
          data: data.growth.map(item =&gt; item.date)
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '新增用户',
            type: 'bar',
            data: data.growth.map(item =&gt; item.count)
          },
          {
            name: '累计用户',
            type: 'line',
            data: data.growth.map(item =&gt; item.cumulative),
            smooth: true
          }
        ]
      }
      userGrowthChart.setOption(option)
    }
  } catch (error) {
    console.error('加载用户增长失败', error)
  }
}

const loadOrderStats = async () =&gt; {
  try {
    const res = await getOrderStats()
    if (res.data) {
      const data: OrderStatsResponse = res.data
      recentOrders.value = data.recent_orders
      
      if (orderStatsChart) {
        const option = {
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: '订单状态',
              type: 'pie',
              radius: '50%',
              data: [
                { value: data.stats.pending_payment, name: '待支付' },
                { value: data.stats.paid, name: '已支付' },
                { value: data.stats.shipped, name: '已发货' },
                { value: data.stats.completed, name: '已完成' },
                { value: data.stats.cancelled, name: '已取消' }
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
        orderStatsChart.setOption(option)
      }
    }
  } catch (error) {
    console.error('加载订单统计失败', error)
  }
}

const initCharts = () =&gt; {
  if (salesTrendRef.value) {
    salesTrendChart = echarts.init(salesTrendRef.value)
  }
  if (userGrowthRef.value) {
    userGrowthChart = echarts.init(userGrowthRef.value)
  }
  if (orderStatsRef.value) {
    orderStatsChart = echarts.init(orderStatsRef.value)
  }
}

const handleResize = () =&gt; {
  salesTrendChart?.resize()
  userGrowthChart?.resize()
  orderStatsChart?.resize()
}

onMounted(() =&gt; {
  initCharts()
  loadStats()
  loadSalesTrend()
  loadUserGrowth()
  loadOrderStats()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() =&gt; {
  salesTrendChart?.dispose()
  userGrowthChart?.dispose()
  orderStatsChart?.dispose()
  window.removeEventListener('resize', handleResize)
})
&lt;/script&gt;

&lt;style scoped&gt;
.report-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.stat-trend {
  font-size: 12px;
  color: #909399;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-container {
  width: 100%;
  height: 350px;
}
&lt;/style&gt;
