<template>
  <div class="table-template">
    <div class="table-search">
      <el-form :inline="true" :model="queryForm" class="search-form">
        <slot name="search"></slot>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="table-toolbar">
      <slot name="toolbar"></slot>
    </div>
    <el-table
      v-loading="loading"
      :data="tableData"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <slot></slot>
    </el-table>
    <div class="table-pagination">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const props = defineProps<{
  loading?: boolean
  data?: any[]
}>()

const emit = defineEmits(['search', 'reset', 'selection-change', 'size-change', 'current-change'])

const queryForm = reactive({})
const loading = ref(props.loading || false)
const tableData = ref(props.data || [])
const selectedRows = ref<any[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const handleSearch = () => {
  emit('search', queryForm)
}

const handleReset = () => {
  emit('reset', queryForm)
}

const handleSelectionChange = (rows: any[]) => {
  selectedRows.value = rows
  emit('selection-change', rows)
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  emit('size-change', size)
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  emit('current-change', page)
}
</script>

<style lang="scss" scoped>
.table-template {
  .table-search {
    margin-bottom: 20px;
    padding: 15px;
    background: #f5f7fa;
    border-radius: 4px;
  }

  .search-form {
    margin-bottom: 0;
  }

  .table-toolbar {
    margin-bottom: 15px;
  }

  .table-pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
