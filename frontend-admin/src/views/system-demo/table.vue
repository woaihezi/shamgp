<template>
  <PageContainer title="表格示例">
    <TableTemplate
      :loading="loading"
      :data="tableData"
      @search="handleSearch"
      @reset="handleReset"
      @selection-change="handleSelectionChange"
    >
      <template #search>
        <el-form-item label="用户名">
          <el-input v-model="queryForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" placeholder="请选择状态" clearable>
            <el-option label="启用" value="1" />
            <el-option label="禁用" value="0" />
          </el-select>
        </el-form-item>
      </template>

      <template #toolbar>
        <el-button type="primary" :icon="Plus">新增</el-button>
        <el-button type="danger" :icon="Delete" :disabled="selectedRows.length === 0">批量删除</el-button>
      </template>

      <el-table-column type="selection" width="55" />
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="150" />
      <el-table-column prop="email" label="邮箱" width="200" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === '1' ? 'success' : 'danger'">
            {{ row.status === '1' ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="创建时间" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link size="small">编辑</el-button>
          <el-button type="danger" link size="small">删除</el-button>
        </template>
      </el-table-column>
    </TableTemplate>
  </PageContainer>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus, Delete } from '@element-plus/icons-vue'
import PageContainer from '@/components/PageContainer/index.vue'
import TableTemplate from '@/components/TableTemplate/index.vue'

const loading = ref(false)
const selectedRows = ref<any[]>([])
const tableData = ref<any[]>([])

const queryForm = reactive({
  username: '',
  status: ''
})

const generateMockData = () => {
  const data = []
  for (let i = 1; i <= 10; i++) {
    data.push({
      id: i,
      username: `user${i}`,
      email: `user${i}@example.com`,
      phone: `1380013800${i.toString().padStart(2, '0')}`,
      status: i % 2 === 0 ? '1' : '0',
      createTime: '2024-01-01 12:00:00'
    })
  }
  return data
}

const handleSearch = (form: any) => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
}

const handleReset = (form: any) => {
  queryForm.username = ''
  queryForm.status = ''
}

const handleSelectionChange = (rows: any[]) => {
  selectedRows.value = rows
}

onMounted(() => {
  tableData.value = generateMockData()
})
</script>
