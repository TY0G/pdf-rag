<template>
  <div class="profile-page">
    <section class="card-panel profile-card">
      <div class="section-title">个人中心</div>
      <div class="section-subtitle">当前登录账号信息</div>

      <div class="profile-grid">
        <div class="item">
          <span>昵称</span>
          <strong>{{ auth.user?.nickname }}</strong>
        </div>
        <div class="item">
          <span>邮箱</span>
          <strong>{{ auth.user?.email }}</strong>
        </div>
        <div class="item">
          <span>角色</span>
          <strong>{{ auth.user?.role }}</strong>
        </div>
        <div class="item">
          <span>创建时间</span>
          <strong>{{ auth.user?.created_at }}</strong>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.profile-card {
  padding: 24px;
}

.profile-grid {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.item {
  padding: 18px;
  background: #f8fafc;
  border-radius: 16px;
}

.item span {
  display: block;
  color: #6b7280;
  margin-bottom: 8px;
  font-size: 13px;
}
</style>
