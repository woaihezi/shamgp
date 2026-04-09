<template>
  <div class="user-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleAddUser">添加用户</el-button>
        </div>
      </template>

      <el-form :inline="true" :model="queryParams" class="search-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="queryParams.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-select v-model="queryParams.is_active" placeholder="请选择状态" clearable>
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="头像" width="100">
          <template #default="{ row }">
            <el-avatar :src="row.avatar || ''" :size="40">
              {{ row.username?.charAt(0).toUpperCase() }}
            </el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" show-overflow-tooltip />
        <el-table-column prop="email" label="邮箱" show-overflow-tooltip />
        <el-table-column prop="phone" label="电话" show-overflow-tooltip />
        <el-table-column prop="nickname" label="昵称" show-overflow-tooltip />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_superuser" label="角色" width="100">
          <template #default="{ row }">
            <el-tag type="warning" v-if="row.is_superuser">管理员</el-tag>
            <el-tag v-else>普通用户</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEditUser(row)">编辑</el-button>
            <el-button type="primary" link @click="handleChangePassword(row)">修改密码</el-button>
            <el-button type="danger" link @click="handleDeleteUser(row)" v-if="!row.is_superuser">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="queryParams.page"
        v-model:page-size="queryParams.page_size"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleQuery"
        @current-change="handleQuery"
      />
    </el-card>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用户' : '添加用户'"
      width="500px"
      @close="handleDialogClose"
    >
      <el-form :model="form" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
          <el-input v-model="form.username" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="密码" v-if="!isEdit" prop="password" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
          <el-input v-model="form.password" type="password" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="passwordDialogVisible" title="修改密码" width="400px">
      <el-form :model="passwordForm" ref="passwordFormRef" label-width="100px">
        <el-form-item label="旧密码" prop="old_password" :rules="[{ required: true, message: '请输入旧密码', trigger: 'blur' }]">
          <el-input v-model="passwordForm.old_password" type="password" />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password" :rules="[{ required: true, message: '请输入新密码', trigger: 'blur' }]">
          <el-input v-model="passwordForm.new_password" type="password" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handlePasswordSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { getUserList, createUser, updateUser, deleteUser, updateUserPassword } from '@/api/user'
import type { UserInfo, UserCreate, UserUpdate, UserPasswordUpdate } from '@/api/user'

const queryParams = reactive({
  page: 1,
  page_size: 10,
  username: '',
  is_active: undefined as boolean | undefined
})

const tableData = ref<UserInfo[]>([])
const total = ref(0)
const dialogVisible = ref(false)
const passwordDialogVisible = ref(false)
const formRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()
const isEdit = ref(false)
const currentUserId = ref<number | null>(null)

const form = reactive<UserCreate & UserUpdate>({
  username: '',
  password: '',
  email: '',
  phone: '',
  nickname: '',
  is_active: true
})

const passwordForm = reactive<UserPasswordUpdate>({
  old_password: '',
  new_password: ''
})

const loadData = async () => {
  try {
    const res = await getUserList({
      page: queryParams.page,
      page_size: queryParams.page_size
    })
    if (res.data) {
      tableData.value = res.data.items
      total.value = res.data.total
    }
  } catch (error) {
    console.error('加载用户列表失败', error)
  }
}

const handleQuery = () => {
  queryParams.page = 1
  loadData()
}

const handleReset = () => {
  queryParams.username = ''
  queryParams.is_active = undefined
  handleQuery()
}

const handleAddUser = () => {
  isEdit.value = false
  Object.assign(form, {
    username: '',
    password: '',
    email: '',
    phone: '',
    nickname: '',
    is_active: true
  })
  dialogVisible.value = true
}

const handleEditUser = (row: UserInfo) => {
  isEdit.value = true
  currentUserId.value = row.id
  Object.assign(form, {
    username: row.username,
    email: row.email || '',
    phone: row.phone || '',
    nickname: row.nickname || '',
    is_active: row.is_active ?? true
  })
  dialogVisible.value = true
}

const handleChangePassword = (row: UserInfo) => {
  currentUserId.value = row.id
  Object.assign(passwordForm, {
    old_password: '',
    new_password: ''
  })
  passwordDialogVisible.value = true
}

const handleDeleteUser = async (row: UserInfo) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteUser(row.id!)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用户失败', error)
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value && currentUserId.value) {
          await updateUser(currentUserId.value, form)
          ElMessage.success('更新成功')
        } else {
          await createUser(form)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        loadData()
      } catch (error) {
        console.error('操作失败', error)
      }
    }
  })
}

const handlePasswordSubmit = async () => {
  if (!passwordFormRef.value || !currentUserId.value) return
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await updateUserPassword(currentUserId.value, passwordForm)
        ElMessage.success('密码修改成功')
        passwordDialogVisible.value = false
      } catch (error) {
        console.error('密码修改失败', error)
      }
    }
  })
}

const handleDialogClose = () => {
  formRef.value?.resetFields()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.user-container {
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
</style>