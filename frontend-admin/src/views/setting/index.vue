
&lt;template&gt;
  &lt;div class="setting-container"&gt;
    &lt;el-card class="box-card"&gt;
      &lt;template #header&gt;
        &lt;div class="card-header"&gt;
          &lt;span&gt;系统配置管理&lt;/span&gt;
          &lt;el-button type="primary" @click="handleAdd"&gt;新增配置&lt;/el-button&gt;
        &lt;/div&gt;
      &lt;/template&gt;

      &lt;el-form :inline="true" :model="queryParams" class="search-form"&gt;
        &lt;el-form-item label="配置键"&gt;
          &lt;el-input v-model="queryParams.config_key" placeholder="请输入配置键" clearable /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="配置分组"&gt;
          &lt;el-input v-model="queryParams.config_group" placeholder="请输入配置分组" clearable /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="状态"&gt;
          &lt;el-select v-model="queryParams.status" placeholder="请选择状态" clearable&gt;
            &lt;el-option label="启用" :value="1" /&gt;
            &lt;el-option label="禁用" :value="0" /&gt;
          &lt;/el-select&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item&gt;
          &lt;el-button type="primary" @click="handleQuery"&gt;查询&lt;/el-button&gt;
          &lt;el-button @click="handleReset"&gt;重置&lt;/el-button&gt;
        &lt;/el-form-item&gt;
      &lt;/el-form&gt;

      &lt;el-table :data="tableData" stripe style="width: 100%"&gt;
        &lt;el-table-column prop="id" label="ID" width="80" /&gt;
        &lt;el-table-column prop="config_key" label="配置键" width="200" /&gt;
        &lt;el-table-column prop="config_value" label="配置值" show-overflow-tooltip /&gt;
        &lt;el-table-column prop="config_type" label="配置类型" width="100"&gt;
          &lt;template #default="{ row }"&gt;
            &lt;el-tag&gt;{{ row.config_type }}&lt;/el-tag&gt;
          &lt;/template&gt;
        &lt;/el-table-column&gt;
        &lt;el-table-column prop="config_group" label="配置分组" width="120" /&gt;
        &lt;el-table-column prop="description" label="描述" show-overflow-tooltip /&gt;
        &lt;el-table-column prop="is_public" label="是否公开" width="100"&gt;
          &lt;template #default="{ row }"&gt;
            &lt;el-tag :type="row.is_public ? 'success' : 'info'"&gt;
              {{ row.is_public ? '是' : '否' }}
            &lt;/el-tag&gt;
          &lt;/template&gt;
        &lt;/el-table-column&gt;
        &lt;el-table-column prop="sort" label="排序" width="80" /&gt;
        &lt;el-table-column prop="status" label="状态" width="100"&gt;
          &lt;template #default="{ row }"&gt;
            &lt;el-tag :type="row.status === 1 ? 'success' : 'danger'"&gt;
              {{ row.status === 1 ? '启用' : '禁用' }}
            &lt;/el-tag&gt;
          &lt;/template&gt;
        &lt;/el-table-column&gt;
        &lt;el-table-column prop="created_at" label="创建时间" width="180" /&gt;
        &lt;el-table-column label="操作" width="200" fixed="right"&gt;
          &lt;template #default="{ row }"&gt;
            &lt;el-button type="primary" link @click="handleEdit(row)"&gt;编辑&lt;/el-button&gt;
            &lt;el-button type="danger" link @click="handleDelete(row)"&gt;删除&lt;/el-button&gt;
          &lt;/template&gt;
        &lt;/el-table-column&gt;
      &lt;/el-table&gt;

      &lt;el-pagination
        v-model:current-page="queryParams.page"
        v-model:page-size="queryParams.page_size"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleQuery"
        @current-change="handleQuery"
      /&gt;
    &lt;/el-card&gt;

    &lt;el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    &gt;
      &lt;el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px"&gt;
        &lt;el-form-item label="配置键" prop="config_key"&gt;
          &lt;el-input v-model="formData.config_key" :disabled="isEdit" placeholder="请输入配置键" /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="配置值" prop="config_value"&gt;
          &lt;el-input v-model="formData.config_value" type="textarea" :rows="3" placeholder="请输入配置值" /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="配置类型" prop="config_type"&gt;
          &lt;el-select v-model="formData.config_type" placeholder="请选择配置类型"&gt;
            &lt;el-option label="字符串" value="string" /&gt;
            &lt;el-option label="整数" value="int" /&gt;
            &lt;el-option label="布尔" value="bool" /&gt;
            &lt;el-option label="JSON" value="json" /&gt;
          &lt;/el-select&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="配置分组" prop="config_group"&gt;
          &lt;el-input v-model="formData.config_group" placeholder="请输入配置分组" /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="描述" prop="description"&gt;
          &lt;el-input v-model="formData.description" placeholder="请输入描述" /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="是否公开" prop="is_public"&gt;
          &lt;el-switch v-model="formData.is_public" /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="排序" prop="sort"&gt;
          &lt;el-input-number v-model="formData.sort" :min="0" /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="状态" prop="status"&gt;
          &lt;el-radio-group v-model="formData.status"&gt;
            &lt;el-radio :label="1"&gt;启用&lt;/el-radio&gt;
            &lt;el-radio :label="0"&gt;禁用&lt;/el-radio&gt;
          &lt;/el-radio-group&gt;
        &lt;/el-form-item&gt;
      &lt;/el-form&gt;
      &lt;template #footer&gt;
        &lt;el-button @click="dialogVisible = false"&gt;取消&lt;/el-button&gt;
        &lt;el-button type="primary" @click="handleSubmit"&gt;确定&lt;/el-button&gt;
      &lt;/template&gt;
    &lt;/el-dialog&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { getConfigList, createConfig, updateConfig, deleteConfig } from '@/api/setting'
import type { SystemConfig } from '@/api/setting'

const queryParams = reactive({
  page: 1,
  page_size: 10,
  config_key: '',
  config_group: '',
  status: undefined as number | undefined
})

const tableData = ref&lt;SystemConfig[]&gt;([])
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const formRef = ref&lt;FormInstance&gt;()

const formData = reactive&lt;SystemConfig&gt;({
  config_key: '',
  config_value: '',
  config_type: 'string',
  config_group: '',
  description: '',
  is_public: false,
  sort: 0,
  status: 1
})

const formRules: FormRules = {
  config_key: [{ required: true, message: '请输入配置键', trigger: 'blur' }],
  config_type: [{ required: true, message: '请选择配置类型', trigger: 'change' }],
  sort: [{ required: true, message: '请输入排序', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

const loadData = async () =&gt; {
  try {
    const res = await getConfigList(queryParams)
    if (res.data) {
      tableData.value = res.data.items
      total.value = res.data.total
    }
  } catch (error) {
    console.error('加载配置列表失败', error)
  }
}

const handleQuery = () =&gt; {
  queryParams.page = 1
  loadData()
}

const handleReset = () =&gt; {
  queryParams.config_key = ''
  queryParams.config_group = ''
  queryParams.status = undefined
  handleQuery()
}

const handleAdd = () =&gt; {
  dialogTitle.value = '新增配置'
  isEdit.value = false
  Object.assign(formData, {
    config_key: '',
    config_value: '',
    config_type: 'string',
    config_group: '',
    description: '',
    is_public: false,
    sort: 0,
    status: 1
  })
  dialogVisible.value = true
}

const handleEdit = (row: SystemConfig) =&gt; {
  dialogTitle.value = '编辑配置'
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

const handleDelete = async (row: SystemConfig) =&gt; {
  try {
    await ElMessageBox.confirm('确定要删除该配置吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteConfig(row.id!)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除配置失败', error)
    }
  }
}

const handleSubmit = async () =&gt; {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) =&gt; {
    if (valid) {
      try {
        if (isEdit.value) {
          await updateConfig(formData.id!, formData)
          ElMessage.success('更新成功')
        } else {
          await createConfig(formData)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadData()
      } catch (error) {
        console.error('提交失败', error)
      }
    }
  })
}

const handleDialogClose = () =&gt; {
  formRef.value?.resetFields()
}

onMounted(() =&gt; {
  loadData()
})
&lt;/script&gt;

&lt;style scoped&gt;
.setting-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.search-form {
  margin-bottom: 20px;
}

.el-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
&lt;/style&gt;
