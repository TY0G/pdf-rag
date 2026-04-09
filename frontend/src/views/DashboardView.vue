<template>
  <div class="dashboard">
    <section class="hero card-panel">
      <div>
        <div class="section-title">你好，{{ auth.user?.nickname }}</div>
        <div class="section-subtitle">
          这里是 PDF 文档扫描与智能问答工作台。你可以上传 PDF，系统会自动解析并生成可问答索引。
        </div>
      </div>
      <div class="light-tag">浅色风格界面</div>
    </section>

    <section class="stats-grid">
      <div class="stat card-panel">
        <div class="stat-label">当前用户</div>
        <div class="stat-value">{{ auth.user?.email }}</div>
      </div>
      <div class="stat card-panel">
        <div class="stat-label">角色</div>
        <div class="stat-value">{{ auth.user?.role }}</div>
      </div>
      <div class="stat card-panel">
        <div class="stat-label">核心能力</div>
        <div class="stat-value">PDF / 解析 / 检索 / 问答</div>
      </div>
    </section>

    <section class="grid-two">
      <div class="card-panel panel">
        <div class="section-title" style="font-size: 18px">系统流程</div>
        <ol class="flow-list">
          <li>上传 PDF 文档</li>
          <li>自动提取文本并清洗</li>
          <li>按 chunk 切分并向量化</li>
          <li>用户发起问题</li>
          <li>检索证据并生成回答</li>
          <li>附带页码和引用片段</li>
        </ol>
      </div>

      <div class="card-panel panel">
        <div class="section-title" style="font-size: 18px">建议演示顺序</div>
        <ol class="flow-list">
          <li>登录系统</li>
          <li>上传需求文档 PDF</li>
          <li>进入文档详情页查看解析结果</li>
          <li>切到智能问答页选择文档</li>
          <li>提问“这份文档的核心需求是什么？”</li>
        </ol>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hero {
  padding: 22px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.stat {
  padding: 18px;
}

.stat-label {
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #1f2937;
  word-break: break-all;
}

.grid-two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.panel {
  padding: 20px;
}

.flow-list {
  margin: 14px 0 0;
  padding-left: 20px;
  color: #475569;
  line-height: 1.9;
}

@media (max-width: 960px) {
  .stats-grid,
  .grid-two {
    grid-template-columns: 1fr;
  }
}
</style>
