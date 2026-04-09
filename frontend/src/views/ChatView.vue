<template>
  <div class="chat-page">
    <section class="toolbar card-panel">
      <div>
        <div class="section-title">智能问答</div>
        <div class="section-subtitle">选择一个或多个文档后提问，系统会附带原文引用</div>
      </div>

      <el-select
        v-model="selectedDocumentIds"
        multiple
        collapse-tags
        collapse-tags-tooltip
        placeholder="请选择文档"
        style="width: 360px"
      >
        <el-option
          v-for="item in readyDocuments"
          :key="item.id"
          :label="item.file_name"
          :value="item.id"
        />
      </el-select>
    </section>

    <section class="grid">
      <ChatPanel :messages="messages" :loading="asking" @submit="submitQuestion" />
      <CitationList :citations="citations" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import ChatPanel from '@/components/ChatPanel.vue'
import CitationList from '@/components/CitationList.vue'
import { documentApi, type DocumentItem } from '@/api/documents'
import { chatApi } from '@/api/chat'

const documents = ref<DocumentItem[]>([])
const selectedDocumentIds = ref<number[]>([])
const asking = ref(false)
const conversationId = ref<number | null>(null)
const citations = ref<any[]>([])
const messages = ref<Array<{ role: string; content: string }>>([
  {
    role: 'assistant',
    content: '你好，请先选择一个或多个已完成解析的文档，然后输入你的问题。'
  }
])

const readyDocuments = computed(() => documents.value.filter((item) => item.parse_status === 'ready'))

async function loadDocuments() {
  try {
    documents.value = await documentApi.list()
    if (!selectedDocumentIds.value.length && readyDocuments.value.length) {
      selectedDocumentIds.value = [readyDocuments.value[0].id]
    }
  } catch (error: any) {
    ElMessage.error(error.message)
  }
}

async function submitQuestion(question: string) {
  if (!selectedDocumentIds.value.length) {
    ElMessage.warning('请先选择文档')
    return
  }
  try {
    asking.value = true
    messages.value.push({ role: 'user', content: question })
    const result = await chatApi.ask({
      question,
      document_ids: selectedDocumentIds.value,
      conversation_id: conversationId.value
    })
    conversationId.value = result.conversation_id
    citations.value = result.citations
    messages.value.push({ role: 'assistant', content: result.answer })
  } catch (error: any) {
    ElMessage.error(error.message)
  } finally {
    asking.value = false
  }
}

onMounted(loadDocuments)
</script>

<style scoped>
.chat-page {
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

.grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 18px;
  align-items: start;
}

@media (max-width: 1100px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
