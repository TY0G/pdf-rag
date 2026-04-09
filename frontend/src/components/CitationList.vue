<template>
  <div class="citation-wrap">
    <div class="section-title" style="font-size: 16px; margin-bottom: 12px">引用证据</div>
    <div v-if="!citations.length" class="empty">暂无引用</div>
    <div v-for="item in citations" :key="item.chunk_id" class="citation-item card-panel">
      <div class="citation-head">
        <strong>{{ item.document_name }}</strong>
        <span>第 {{ item.page_number }} 页</span>
        <span>相关度 {{ item.score }}</span>
      </div>
      <div class="citation-content">{{ item.content }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ citations: Array<any> }>()
</script>

<style scoped>
.citation-wrap {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.citation-item {
  padding: 14px;
}

.citation-head {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  color: #475569;
  font-size: 13px;
  margin-bottom: 10px;
}

.citation-content {
  white-space: pre-wrap;
  line-height: 1.7;
  color: #1f2937;
}

.empty {
  color: #6b7280;
}
</style>
