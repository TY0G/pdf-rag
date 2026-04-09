<template>
  <div class="doc-page">
    <section class="toolbar card-panel">
      <div>
        <div class="section-title">文档中心</div>
        <div class="section-subtitle">上传后会自动触发解析和索引构建</div>
      </div>
      <el-button type="primary" @click="dialogVisible = true">上传 PDF</el-button>
    </section>

    <section class="card-panel list-panel">
      <el-table :data="documents" style="width: 100%" v-loading="loading">
        <el-table-column prop="file_name" label="文档名" min-width="240" />
        <el-table-column prop="file_size" label="大小" width="120">
          <template #default="{ row }">{{ formatSize(row.file_size) }}</template>
        </el-table-column>
        <el-table-column prop="page_count" label="页数" width="100" />
        <el-table-column prop="parse_status" label="状态" width="120">
          <template #default="{ row }">
            <StatusTag :status="row.parse_status" />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" min-width="180" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-space>
              <el-button link type="primary" @click="goDetail(row.id)">详情</el-button>
              <el-button link @click="reparse(row.id)">重新解析</el-button>
            </el-space>
          </template>
        </el-table-column>
      </el-table>
    </section>

    <FileUploadDialog v-model="dialogVisible" :loading="uploading" @submit="handleUpload" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import FileUploadDialog from '@/components/FileUploadDialog.vue'
import StatusTag from '@/components/StatusTag.vue'
import { documentApi, type DocumentItem } from '@/api/documents'

const router = useRouter()
const documents = ref<DocumentItem[]>([])
const loading = ref(false)
const uploading = ref(false)
const dialogVisible = ref(false)

function formatSize(size: number) {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / 1024 / 1024).toFixed(2)} MB`
}

async function loadDocuments() {
  try {
    loading.value = true
    documents.value = await documentApi.list()
  } catch (error: any) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}

async function handleUpload(file: File) {
  try {
    uploading.value = true
    await documentApi.upload(file)
    ElMessage.success('上传成功，已开始后台解析')
    dialogVisible.value = false
    await loadDocuments()
  } catch (error: any) {
    ElMessage.error(error.message)
  } finally {
    uploading.value = false
  }
}

async function reparse(id: number) {
  try {
    await documentApi.reparse(id)
    ElMessage.success('已重新触发解析')
    await loadDocuments()
  } catch (error: any) {
    ElMessage.error(error.message)
  }
}

function goDetail(id: number) {
  router.push(`/documents/${id}`)
}

onMounted(loadDocuments)
</script>

<style scoped>
.doc-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.toolbar {
  padding: 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.list-panel {
  padding: 16px;
}
</style>
