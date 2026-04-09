<template>
  <div class="detail-page" v-loading="loading">
    <section class="header card-panel">
      <div>
        <div class="section-title">{{ detail?.file_name || '文档详情' }}</div>
        <div class="section-subtitle">
          状态：<StatusTag v-if="detail" :status="detail.parse_status" />
        </div>
      </div>
      <el-button @click="reload">刷新</el-button>
    </section>

    <section class="grid">
      <div class="left-column">
        <div class="card-panel panel">
          <div class="meta-grid">
            <div><span class="meta-label">页数</span><strong>{{ detail?.page_count || 0 }}</strong></div>
            <div><span class="meta-label">大小</span><strong>{{ formatSize(detail?.file_size || 0) }}</strong></div>
            <div><span class="meta-label">类型</span><strong>{{ detail?.content_type }}</strong></div>
            <div><span class="meta-label">创建时间</span><strong>{{ detail?.created_at }}</strong></div>
          </div>

          <div class="summary-box">
            <div class="section-title" style="font-size: 16px">摘要</div>
            <div class="summary-text">{{ detail?.summary || '暂无摘要' }}</div>
          </div>
        </div>

        <div class="card-panel panel">
          <div class="section-title" style="font-size: 16px; margin-bottom: 12px">解析片段</div>
          <div v-if="!detail?.chunks?.length" class="empty">当前暂无 chunk，可能还在解析中。</div>
          <div v-for="chunk in detail?.chunks || []" :key="chunk.id" class="chunk-item">
            <div class="chunk-head">第 {{ chunk.page_number }} 页 · Chunk {{ chunk.chunk_index }}</div>
            <div class="chunk-content">{{ chunk.content }}</div>
          </div>
        </div>
      </div>

      <div class="card-panel panel preview-panel">
        <div class="section-title" style="font-size: 16px; margin-bottom: 12px">PDF 预览</div>
        <iframe v-if="detail" :src="fileUrl" class="pdf-frame"></iframe>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute } from 'vue-router'
import { documentApi } from '@/api/documents'
import StatusTag from '@/components/StatusTag.vue'

const route = useRoute()
const loading = ref(false)
const detail = ref<any>(null)

const documentId = computed(() => Number(route.params.id))
const fileUrl = computed(() => documentApi.fileUrl(documentId.value))

function formatSize(size: number) {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / 1024 / 1024).toFixed(2)} MB`
}

async function loadDetail() {
  try {
    loading.value = true
    detail.value = await documentApi.detail(documentId.value)
  } catch (error: any) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}

function reload() {
  loadDetail()
}

onMounted(loadDetail)
</script>

<style scoped>
.detail-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header,
.panel {
  padding: 20px;
}

.grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 18px;
  min-height: 720px;
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

.meta-label {
  display: block;
  color: #6b7280;
  font-size: 12px;
  margin-bottom: 6px;
}

.summary-box {
  margin-top: 18px;
}

.summary-text {
  margin-top: 10px;
  color: #334155;
  line-height: 1.7;
}

.chunk-item {
  padding: 14px;
  border: 1px solid #edf2f7;
  border-radius: 14px;
  background: #fafcff;
  margin-bottom: 12px;
}

.chunk-head {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 8px;
}

.chunk-content {
  white-space: pre-wrap;
  line-height: 1.75;
}

.preview-panel {
  min-height: 720px;
}

.pdf-frame {
  width: 100%;
  height: 640px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: white;
}

.empty {
  color: #6b7280;
}

@media (max-width: 1100px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
