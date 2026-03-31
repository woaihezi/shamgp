<template>
  <PageContainer title="表单示例">
    <el-card>
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="formData.username" placeholder="请输入用户名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="formData.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="formData.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门" prop="department">
              <el-select v-model="formData.department" placeholder="请选择部门" style="width: 100%">
                <el-option label="技术部" value="tech" />
                <el-option label="产品部" value="product" />
                <el-option label="运营部" value="operation" />
                <el-option label="市场部" value="marketing" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="formData.gender">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-switch v-model="formData.status" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="入职日期" prop="hireDate">
          <el-date-picker
            v-model="formData.hireDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="技能" prop="skills">
          <el-checkbox-group v-model="formData.skills">
            <el-checkbox label="Vue" />
            <el-checkbox label="React" />
            <el-checkbox label="Angular" />
            <el-checkbox label="Node.js" />
            <el-checkbox label="Python" />
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="formData.remark" type="textarea" :rows="4" placeholder="请输入备注" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-divider />

    <el-card>
      <template #header>
        <div class="card-header">
          <span>弹窗表单示例</span>
          <el-button type="primary" @click="dialogVisible = true">打开弹窗</el-button>
        </div>
      </template>
      <p>点击上方按钮查看弹窗表单效果</p>
    </el-card>

    <FormDialog
      v-model="dialogVisible"
      title="新增用户"
      width="600px"
      :rules="dialogRules"
      @submit="handleDialogSubmit"
      ref="dialogRef"
    >
      <el-form-item label="用户名" prop="username">
        <el-input v-model="dialogFormData.username" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="dialogFormData.email" placeholder="请输入邮箱" />
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="dialogFormData.phone" placeholder="请输入手机号" />
      </el-form-item>
    </FormDialog>
  </PageContainer>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import PageContainer from '@/components/PageContainer/index.vue'
import FormDialog from '@/components/FormDialog/index.vue'

const formRef = ref()
const dialogRef = ref()
const dialogVisible = ref(false)

const formData = reactive({
  username: '',
  email: '',
  phone: '',
  department: '',
  gender: 'male',
  status: true,
  hireDate: '',
  skills: [],
  remark: ''
})

const dialogFormData = reactive({
  username: '',
  email: '',
  phone: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  department: [{ required: true, message: '请选择部门', trigger: 'change' }]
}

const dialogRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid: boolean) => {
    if (valid) {
      ElMessage.success('提交成功')
    }
  })
}

const handleReset = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
}

const handleDialogSubmit = (formData: any) => {
  console.log('表单数据:', formData)
  ElMessage.success('提交成功')
  dialogVisible.value = false
}
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
