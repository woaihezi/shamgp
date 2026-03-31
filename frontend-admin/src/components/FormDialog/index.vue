<template>
  <el-dialog
    :title="title"
    v-model="visible"
    :width="width"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      :label-width="labelWidth"
    >
      <slot></slot>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: boolean
  title?: string
  width?: string
  labelWidth?: string
  rules?: any
}>()

const emit = defineEmits(['update:modelValue', 'submit', 'close'])

const formRef = ref()
const visible = ref(props.modelValue)
const submitting = ref(false)
const formData = ref<any>({})

watch(
  () => props.modelValue,
  (val) => {
    visible.value = val
  }
)

watch(
  visible,
  (val) => {
    emit('update:modelValue', val)
  }
)

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitting.value = true
      emit('submit', formData.value)
      submitting.value = false
    }
  })
}

const handleCancel = () => {
  visible.value = false
}

const handleClose = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  emit('close')
}

defineExpose({
  formRef,
  formData
})
</script>

<style lang="scss" scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
