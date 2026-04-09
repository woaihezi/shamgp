<template>
  <div class="permission-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>权限管理</span>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="角色管理" name="roles">
          <div class="tab-content">
            <div class="action-bar">
              <el-button type="primary" @click="handleAddRole">添加角色</el-button>
            </div>

            <el-table :data="roleList" stripe style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="角色名称" />
              <el-table-column prop="code" label="角色编码" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
              <el-table-column prop="sort" label="排序" width="80" />
              <el-table-column prop="created_at" label="创建时间" width="180" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link @click="handleEditRole(row)">编辑</el-button>
                  <el-button type="danger" link @click="handleDeleteRole(row)" v-if="row.code !== 'superadmin'">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="权限管理" name="permissions">
          <div class="tab-content">
            <div class="action-bar">
              <el-button type="primary" @click="handleAddPermission">添加权限</el-button>
            </div>

            <el-table :data="permissionList" stripe style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="权限名称" />
              <el-table-column prop="code" label="权限编码" />
              <el-table-column prop="type" label="类型" width="100" />
              <el-table-column prop="path" label="路径" show-overflow-tooltip />
              <el-table-column prop="method" label="方法" width="100" />
              <el-table-column prop="sort" label="排序" width="80" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link @click="handleEditPermission(row)">编辑</el-button>
                  <el-button type="danger" link @click="handleDeletePermission(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 添加/编辑角色对话框 -->
    <el-dialog
      v-model="roleDialogVisible"
      :title="isEditRole ? '编辑角色' : '添加角色'"
      width="600px"
      @close="handleRoleDialogClose"
    >
      <el-form :model="roleForm" ref="roleFormRef" label-width="100px">
        <el-form-item label="角色名称" prop="name" :rules="[{ required: true, message: '请输入角色名称', trigger: 'blur' }]">
          <el-input v-model="roleForm.name" />
        </el-form-item>
        <el-form-item label="角色编码" prop="code" :rules="[{ required: true, message: '请输入角色编码', trigger: 'blur' }]">
          <el-input v-model="roleForm.code" :disabled="isEditRole" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="roleForm.description" type="textarea" />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="roleForm.sort" :min="0" />
        </el-form-item>
        <el-form-item label="权限" prop="permissions">
          <el-checkbox-group v-model="roleForm.permission_ids">
            <el-checkbox v-for="perm in permissionList" :key="perm.id" :label="perm.id">
              {{ perm.name }} ({{ perm.code }})
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRoleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑权限对话框 -->
    <el-dialog
      v-model="permissionDialogVisible"
      :title="isEditPermission ? '编辑权限' : '添加权限'"
      width="500px"
      @close="handlePermissionDialogClose"
    >
      <el-form :model="permissionForm" ref="permissionFormRef" label-width="100px">
        <el-form-item label="权限名称" prop="name" :rules="[{ required: true, message: '请输入权限名称', trigger: 'blur' }]">
          <el-input v-model="permissionForm.name" />
        </el-form-item>
        <el-form-item label="权限编码" prop="code" :rules="[{ required: true, message: '请输入权限编码', trigger: 'blur' }]">
          <el-input v-model="permissionForm.code" :disabled="isEditPermission" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="permissionForm.type" placeholder="请选择类型">
            <el-option label="API" value="api" />
            <el-option label="菜单" value="menu" />
            <el-option label="按钮" value="button" />
          </el-select>
        </el-form-item>
        <el-form-item label="路径" prop="path">
          <el-input v-model="permissionForm.path" placeholder="如: /api/v1/users" />
        </el-form-item>
        <el-form-item label="方法" prop="method">
          <el-select v-model="permissionForm.method" placeholder="请选择方法">
            <el-option label="GET" value="GET" />
            <el-option label="POST" value="POST" />
            <el-option label="PUT" value="PUT" />
            <el-option label="DELETE" value="DELETE" />
          </el-select>
        </el-form-item>
        <el-form-item label="父权限" prop="parent_id">
          <el-select v-model="permissionForm.parent_id" placeholder="请选择父权限">
            <el-option label="无" :value="0" />
            <el-option v-for="perm in permissionList" :key="perm.id" :label="perm.name" :value="perm.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="permissionForm.sort" :min="0" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="permissionForm.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handlePermissionSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { 
  getRoleList, createRole, updateRole, deleteRole,
  getPermissionList, createPermission, updatePermission, deletePermission
} from '@/api/permission'
import type { Role, Permission } from '@/api/permission'

const activeTab = ref('roles')
const roleList = ref<Role[]>([])
const permissionList = ref<Permission[]>([])

const roleDialogVisible = ref(false)
const permissionDialogVisible = ref(false)
const roleFormRef = ref<FormInstance>()
const permissionFormRef = ref<FormInstance>()
const isEditRole = ref(false)
const isEditPermission = ref(false)
const currentRoleId = ref<number | null>(null)
const currentPermissionId = ref<number | null>(null)

const roleForm = reactive({
  name: '',
  code: '',
  description: '',
  sort: 0,
  permission_ids: [] as number[]
})

const permissionForm = reactive({
  name: '',
  code: '',
  type: 'api',
  path: '',
  method: '',
  parent_id: 0,
  sort: 0,
  description: ''
})

const loadRoles = async () => {
  try {
    const res = await getRoleList()
    if (res.data) {
      roleList.value = res.data.data
    }
  } catch (error) {
    console.error('加载角色列表失败', error)
  }
}

const loadPermissions = async () => {
  try {
    const res = await getPermissionList()
    if (res.data) {
      permissionList.value = res.data.data
    }
  } catch (error) {
    console.error('加载权限列表失败', error)
  }
}

const handleAddRole = () => {
  isEditRole.value = false
  Object.assign(roleForm, {
    name: '',
    code: '',
    description: '',
    sort: 0,
    permission_ids: []
  })
  roleDialogVisible.value = true
}

const handleEditRole = (row: Role) => {
  isEditRole.value = true
  currentRoleId.value = row.id
  Object.assign(roleForm, {
    name: row.name,
    code: row.code,
    description: row.description || '',
    sort: row.sort,
    permission_ids: row.permissions.map(p => p.id)
  })
  roleDialogVisible.value = true
}

const handleDeleteRole = async (row: Role) => {
  try {
    await ElMessageBox.confirm('确定要删除该角色吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteRole(row.id)
    ElMessage.success('删除成功')
    loadRoles()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除角色失败', error)
    }
  }
}

const handleRoleSubmit = async () => {
  if (!roleFormRef.value) return
  await roleFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEditRole.value && currentRoleId.value) {
          await updateRole(currentRoleId.value, roleForm)
          ElMessage.success('更新成功')
        } else {
          await createRole(roleForm)
          ElMessage.success('添加成功')
        }
        roleDialogVisible.value = false
        loadRoles()
      } catch (error) {
        console.error('操作失败', error)
      }
    }
  })
}

const handleAddPermission = () => {
  isEditPermission.value = false
  Object.assign(permissionForm, {
    name: '',
    code: '',
    type: 'api',
    path: '',
    method: '',
    parent_id: 0,
    sort: 0,
    description: ''
  })
  permissionDialogVisible.value = true
}

const handleEditPermission = (row: Permission) => {
  isEditPermission.value = true
  currentPermissionId.value = row.id
  Object.assign(permissionForm, {
    name: row.name,
    code: row.code,
    type: row.type,
    path: row.path || '',
    method: row.method || '',
    parent_id: row.parent_id,
    sort: row.sort,
    description: row.description || ''
  })
  permissionDialogVisible.value = true
}

const handleDeletePermission = async (row: Permission) => {
  try {
    await ElMessageBox.confirm('确定要删除该权限吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deletePermission(row.id)
    ElMessage.success('删除成功')
    loadPermissions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除权限失败', error)
    }
  }
}

const handlePermissionSubmit = async () => {
  if (!permissionFormRef.value) return
  await permissionFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEditPermission.value && currentPermissionId.value) {
          await updatePermission(currentPermissionId.value, permissionForm)
          ElMessage.success('更新成功')
        } else {
          await createPermission(permissionForm)
          ElMessage.success('添加成功')
        }
        permissionDialogVisible.value = false
        loadPermissions()
      } catch (error) {
        console.error('操作失败', error)
      }
    }
  })
}

const handleRoleDialogClose = () => {
  roleFormRef.value?.resetFields()
}

const handlePermissionDialogClose = () => {
  permissionFormRef.value?.resetFields()
}

watch(activeTab, (newTab) => {
  if (newTab === 'permissions') {
    loadPermissions()
  } else if (newTab === 'roles') {
    loadRoles()
  }
})

onMounted(() => {
  loadRoles()
})
</script>

<style scoped>
.permission-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.tab-content {
  margin-top: 20px;
}

.action-bar {
  margin-bottom: 20px;
}

.el-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>