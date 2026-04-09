<template>
  <el-dialog v-model="visible" title="上传 PDF 文档" width="520px">
    <el-upload
      drag
      :show-file-list="false"
      :before-upload="() => false"
      :on-change="onFileChange"
      accept=".pdf"
      class="upload-box"
    >
      <div class="upload-inner">
        <div class="upload-title">点击或拖拽 PDF 到这里</div>
        <div class="upload-sub">仅支持 PDF，上传后自动解析</div>
      </div>
    </el-upload>

    <div v-if="file" class="selected-file">
      已选择：<strong>{{ file.name }}</strong>
    </div>

    <template #footer>
      <el-button @click="close">取消</el-button>
      <el-button type="primary" :loading="props.loading" @click="submit">开始上传</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'submit', file: File): void
}>()

const file = ref<File | null>(null)

const visible = defineModel<boolean>({ default: false })

function onFileChange(uploadFile: { raw?: File }) {
  file.value = uploadFile.raw || null
}

function close() {
  file.value = null
  emit('update:modelValue', false)
}

function submit() {
  if (!file.value) return
  emit('submit', file.value)
}
</script>

<style scoped>
.upload-box {
  width: 100%;
}

.upload-inner {
  padding: 20px 0;
}

.upload-title {
  font-size: 18px;
  font-weight: 700;
  color: #334155;
}

.upload-sub {
  margin-top: 8px;
  color: #6b7280;
}

.selected-file {
  margin-top: 16px;
  color: #475569;
}
</style>
