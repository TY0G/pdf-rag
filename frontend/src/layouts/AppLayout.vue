<template>
  <div class="layout page-shell">
    <aside class="sidebar card-panel">
      <div class="brand">
        <div class="logo">PDF</div>
        <div>
          <div class="brand-title">文档扫描项目</div>
          <div class="brand-sub">Light UI / RAG Demo</div>
        </div>
      </div>

      <nav class="nav-list">
        <RouterLink v-for="item in navItems" :key="item.path" class="nav-item" :to="item.path">
          {{ item.label }}
        </RouterLink>
      </nav>
    </aside>

    <main class="content">
      <header class="topbar card-panel">
        <div>
          <div class="section-title" style="font-size: 18px">PDF 文档扫描与问答平台</div>
          <div class="section-subtitle">上传、解析、检索、问答，一条链路跑通</div>
        </div>

        <div class="topbar-right">
          <div class="light-tag">{{ auth.user?.nickname || '未登录' }}</div>
          <el-button plain @click="logout">退出登录</el-button>
        </div>
      </header>

      <section class="router-body">
        <router-view />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const navItems = [
  { path: '/dashboard', label: '概览' },
  { path: '/documents', label: '文档中心' },
  { path: '/chat', label: '智能问答' },
  { path: '/profile', label: '个人中心' }
]

function logout() {
  auth.clearAuth()
  router.push('/login')
}
</script>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 20px;
  padding: 20px;
}

.sidebar {
  padding: 22px;
  position: sticky;
  top: 20px;
  height: calc(100vh - 40px);
}

.brand {
  display: flex;
  gap: 14px;
  align-items: center;
  padding-bottom: 22px;
  border-bottom: 1px solid #eef2f7;
}

.logo {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: linear-gradient(135deg, #5b83ff, #7ba9ff);
  color: white;
  font-weight: 800;
}

.brand-title {
  font-weight: 700;
  font-size: 18px;
}

.brand-sub {
  color: #6b7280;
  font-size: 12px;
  margin-top: 4px;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 22px;
}

.nav-item {
  padding: 14px 16px;
  border-radius: 14px;
  color: #374151;
  background: #f8fafc;
  border: 1px solid transparent;
  transition: 0.2s ease;
}

.nav-item.router-link-active {
  background: #eef4ff;
  color: #2957d5;
  border-color: #dbe7ff;
}

.content {
  min-width: 0;
}

.topbar {
  padding: 18px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.router-body {
  margin-top: 20px;
}

@media (max-width: 960px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    height: auto;
    position: static;
  }
}
</style>
