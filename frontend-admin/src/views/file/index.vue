
&lt;template&gt;
  &lt;div class="file-container"&gt;
    &lt;el-card class="box-card"&gt;
      &lt;template #header&gt;
        &lt;div class="card-header"&gt;
          &lt;span&gt;文件管理&lt;/span&gt;
          &lt;el-button type="primary" @click="handleUpload"&gt;上传文件&lt;/el-button&gt;
        &lt;/div&gt;
      &lt;/template&gt;

      &lt;el-form :inline="true" :model="queryParams" class="search-form"&gt;
        &lt;el-form-item label="文件名"&gt;
          &lt;el-input v-model="queryParams.filename" placeholder="请输入文件名" clearable /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="文件分类"&gt;
          &lt;el-input v-model="queryParams.category" placeholder="请输入文件分类" clearable /&gt;
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
        &lt;el-table-column label="预览" width="100"&gt;
          &lt;template #default="{ row }"&gt;
            &lt;el-image
              v-if="isImage(row.file_ext)"
              :src="row.file_url"
              :preview-src-list="[row.file_url]"
              fit="cover"
              style="width: 60px; height: 60px"
            /&gt;
            &lt;el-icon v-else style="font-size: 40px; color: #909399"&gt;
              &lt;Document /&gt;
            &lt;/el-icon&gt;
          &lt;/template&gt;
        &lt;/el-table-column&gt;
        &lt;el-table-column prop="filename" label="文件名" show-overflow-tooltip /&gt;
        &lt;el-table-column prop="file_size" label="文件大小" width="120"&gt;
          &lt;template #default="{ row }"&gt;
            {{ formatFileSize(row.file_size) }}
          &lt;/template&gt;
        &lt;/el-table-column&gt;
        &lt;el-table-column prop="file_type" label="文件类型" width="150" /&gt;
        &lt;el-table-column prop="category" label="文件分类" width="120" /&gt;
        &lt;el-table-column prop="storage_type" label="存储类型" width="100"&gt;
          &lt;template #default="{ row }"&gt;
            &lt;el-tag&gt;{{ row.storage_type }}&lt;/el-tag&gt;
          &lt;/template&gt;
        &lt;/el-table-column&gt;
        &lt;el-table-column prop="status" label="状态" width="100"&gt;
          &lt;template #default="{ row }"&gt;
            &lt;el-tag :type="row.status === 1 ? 'success' : 'danger'"&gt;
              {{ row.status === 1 ? '启用' : '禁用' }}
            &lt;/el-tag&gt;
          &lt;/template&gt;
        &lt;/el-table-column&gt;
        &lt;el-table-column prop="created_at" label="上传时间" width="180" /&gt;
        &lt;el-table-column label="操作" width="250" fixed="right"&gt;
          &lt;template #default="{ row }"&gt;
            &lt;el-button type="primary" link @click="handleDownload(row)"&gt;下载&lt;/el-button&gt;
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

    &lt;el-dialog v-model="uploadDialogVisible" title="上传文件" width="500px"&gt;
      &lt;el-upload
        ref="uploadRef"
        class="upload-demo"
        drag
        action="#"
        :auto-upload="false"
        :on-change="handleFileChange"
        :limit="1"
      &gt;
        &lt;el-icon class="el-icon--upload"&gt;&lt;UploadFilled /&gt;&lt;/el-icon&gt;
        &lt;div class="el-upload__text"&gt;
          将文件拖到此处，或&lt;em&gt;点击上传&lt;/em&gt;
        &lt;/div&gt;
        &lt;template #tip&gt;
          &lt;div class="el-upload__tip"&gt;
            支持 jpg, jpeg, png, gif, pdf, doc, docx, xls, xlsx 格式，最大 10MB
          &lt;/div&gt;
        &lt;/template&gt;
      &lt;/el-upload&gt;
      &lt;el-form label-width="100px" style="margin-top: 20px"&gt;
        &lt;el-form-item label="文件分类"&gt;
          &lt;el-input v-model="uploadCategory" placeholder="请输入文件分类" /&gt;
        &lt;/el-form-item&gt;
      &lt;/el-form&gt;
      &lt;template #footer&gt;
        &lt;el-button @click="uploadDialogVisible = false"&gt;取消&lt;/el-button&gt;
        &lt;el-button type="primary" @click="handleUploadSubmit" :loading="uploadLoading"&gt;
          上传
        &lt;/el-button&gt;
      &lt;/template&gt;
    &lt;/el-dialog&gt;

    &lt;el-dialog
      v-model="editDialogVisible"
      title="编辑文件"
      width="500px"
      @close="handleEditDialogClose"
    &gt;
      &lt;el-form :model="editForm" ref="editFormRef" label-width="100px"&gt;
        &lt;el-form-item label="文件名"&gt;
          &lt;el-input v-model="editForm.filename" /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="文件分类"&gt;
          &lt;el-input v-model="editForm.category" /&gt;
        &lt;/el-form-item&gt;
        &lt;el-form-item label="状态"&gt;
          &lt;el-radio-group v-model="editForm.status"&gt;
            &lt;el-radio :label="1"&gt;启用&lt;/el-radio&gt;
            &lt;el-radio :label="0"&gt;禁用&lt;/el-radio&gt;
          &lt;/el-radio-group&gt;
        &lt;/el-form-item&gt;
      &lt;/el-form&gt;
      &lt;template #footer&gt;
        &lt;el-button @click="editDialogVisible = false"&gt;取消&lt;/el-button&gt;
        &lt;el-button type="primary" @click="handleEditSubmit"&gt;确定&lt;/el-button&gt;
      &lt;/template&gt;
    &lt;/el-dialog&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type UploadFile, type UploadUserFile } from 'element-plus'
import { Document, UploadFilled } from '@element-plus/icons-vue'
import { getFileList, uploadFile, updateFile, deleteFile } from '@/api/file'
import type { FileInfo } from '@/api/file'

const queryParams = reactive({
  page: 1,
  page_size: 10,
  filename: '',
  category: '',
  status: undefined as number | undefined
})

const tableData = ref&lt;FileInfo[]&gt;([])
const total = ref(0)
const uploadDialogVisible = ref(false)
const editDialogVisible = ref(false)
const uploadRef = ref()
const editFormRef = ref&lt;FormInstance&gt;()
const uploadLoading = ref(false)
const uploadCategory = ref('')
const selectedFile = ref&lt;File | null&gt;(null)

const editForm = reactive&lt;Partial&lt;FileInfo&gt;&gt;({
  filename: '',
  category: '',
  status: 1
})

const formatFileSize = (bytes: number) =&gt; {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]
}

const isImage = (ext?: string) =&gt; {
  const imageExts = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
  return ext &amp;&amp; imageExts.includes(ext.toLowerCase())
}

const loadData = async () =&gt; {
  try {
    const res = await getFileList(queryParams)
    if (res.data) {
      tableData.value = res.data.items
      total.value = res.data.total
    }
  } catch (error) {
    console.error('加载文件列表失败', error)
  }
}

const handleQuery = () =&gt; {
  queryParams.page = 1
  loadData()
}

const handleReset = () =&gt; {
  queryParams.filename = ''
  queryParams.category = ''
  queryParams.status = undefined
  handleQuery()
}

const handleUpload = () =&gt; {
  uploadCategory.value = ''
  selectedFile.value = null
  uploadRef.value?.clearFiles()
  uploadDialogVisible.value = true
}

const handleFileChange = (file: UploadUserFile) =&gt; {
  selectedFile.value = file.raw as File
}

const handleUploadSubmit = async () =&gt; {
  if (!selectedFile.value) {
    ElMessage.warning('请选择要上传的文件')
    return
  }
  
  uploadLoading.value = true
  try {
    await uploadFile(selectedFile.value, uploadCategory.value)
    ElMessage.success('上传成功')
    uploadDialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('上传失败', error)
  } finally {
    uploadLoading.value = false
  }
}

const handleDownload = (row: FileInfo) =&gt; {
  if (row.file_url) {
    window.open(row.file_url, '_blank')
  }
}

const handleEdit = (row: FileInfo) =&gt; {
  Object.assign(editForm, {
    filename: row.filename,
    category: row.category,
    status: row.status
  })
  editForm.id = row.id
  editDialogVisible.value = true
}

const handleEditSubmit = async () =&gt; {
  if (!editForm.id) return
  try {
    await updateFile(editForm.id, editForm)
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    loadData()
  } catch (error) {
    console.error('更新失败', error)
  }
}

const handleEditDialogClose = () =&gt; {
  editFormRef.value?.resetFields()
}

const handleDelete = async (row: FileInfo) =&gt; {
  try {
    await ElMessageBox.confirm('确定要删除该文件吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteFile(row.id!)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除文件失败', error)
    }
  }
}

onMounted(() =&gt; {
  loadData()
})
&lt;/script&gt;

&lt;style scoped&gt;
.file-container {
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
