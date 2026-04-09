<template>
  <div class="auth-page page-shell">
    <div class="auth-card card-panel">
      <div class="auth-header">
        <div class="section-title">欢迎回来</div>
        <div class="section-subtitle">登录 PDF 文档扫描项目</div>
      </div>

      <el-form :model="form" label-position="top" @submit.prevent>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="密码">
          <el-input v-model="form.password" show-password placeholder="请输入密码" />
        </el-form-item>

        <el-button type="primary" style="width: 100%" :loading="loading" @click="onLogin">
          登录
        </el-button>
      </el-form>

      <div class="helper">
        <span>没有账号？</span>
        <RouterLink to="/register">去注册</RouterLink>
      </div>

      <div class="demo-tip">
        演示账号：admin@example.com / Admin123!
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { RouterLink, useRouter } from 'vue-router'
import { authApi } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const form = reactive({
  email: 'admin@example.com',
  password: 'Admin123!'
})

async function onLogin() {
  try {
    loading.value = true
    const result = await authApi.login(form)
    auth.setAuth(result.access_token, result.user)
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (error: any) {
    ElMessage.error(error.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
}

.auth-card {
  width: 460px;
  padding: 30px;
}

.auth-header {
  margin-bottom: 20px;
}

.helper {
  margin-top: 16px;
  color: #6b7280;
  display: flex;
  gap: 8px;
  justify-content: center;
}

.helper a {
  color: #3c67d6;
}

.demo-tip {
  margin-top: 18px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 12px;
  color: #475569;
  text-align: center;
  font-size: 13px;
}
</style>
