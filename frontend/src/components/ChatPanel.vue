<template>
  <div class="chat-panel card-panel">
    <div class="chat-messages">
      <div v-for="(item, index) in messages" :key="index" :class="['message', item.role]">
        <div class="bubble">
          <div class="role">{{ item.role === 'user' ? '你' : '助手' }}</div>
          <div class="content">{{ item.content }}</div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <el-input
        v-model="question"
        type="textarea"
        :rows="4"
        placeholder="请输入你的问题，例如：这份文档的核心需求是什么？"
      />
      <div class="actions">
        <el-button type="primary" :loading="loading" @click="submit">发送问题</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'submit', question: string): void
}>()

defineProps<{
  messages: Array<{ role: string; content: string }>
  loading?: boolean
}>()

const question = ref('')

function submit() {
  const value = question.value.trim()
  if (!value) return
  emit('submit', value)
  question.value = ''
}
</script>

<style scoped>
.chat-panel {
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 620px;
}

.chat-messages {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 520px;
  overflow: auto;
}

.message {
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.bubble {
  max-width: 80%;
  padding: 14px 16px;
  border-radius: 16px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  line-height: 1.7;
}

.message.user .bubble {
  background: #eef4ff;
  border-color: #dbe7ff;
}

.role {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 6px;
}

.content {
  white-space: pre-wrap;
}

.chat-input {
  border-top: 1px solid #eef2f7;
  padding-top: 16px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}
</style>
