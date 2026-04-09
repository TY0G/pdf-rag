<template>
  <div class="auth-page page-shell">
    <div class="auth-card card-panel">
      <div class="auth-header">
        <div class="section-title">创建账号</div>
        <div class="section-subtitle">开发模式会直接回显验证码，便于演示</div>
      </div>

      <el-form :model="form" label-position="top" @submit.prevent>
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" placeholder="请输入昵称" />
        </el-form-item>

        <el-form-item label="邮箱">
          <div class="inline-row">
            <el-input v-model="form.email" placeholder="请输入邮箱" />
            <el-button :loading="sendingCode" @click="sendCode">发送验证码</el-button>
          </div>
        </el-form-item>

        <el-form-item label="验证码">
          <el-input v-model="form.code" placeholder="请输入验证码" />
        </el-form-item>

        <el-form-item label="密码">
          <el-input v-model="form.password" show-password placeholder="请输入密码" />
        </el-form-item>

        <el-button type="primary" style="width: 100%" :loading="loading" @click="onRegister">
          注册并登录
        </el-button>
      </el-form>

      <div v-if="devCode" class="dev-code">当前开发验证码：{{ devCode }}</div>

      <div class="helper">
        <span>已有账号？</span>
        <RouterLink to="/login">去登录</RouterLink>
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
const sendingCode = ref(false)
const devCode = ref('')
const form = reactive({
  nickname: '',
  email: '',
  code: '',
  password: ''
})

async function sendCode() {
  try {
    sendingCode.value = true
    const result = await authApi.sendCode(form.email)
    devCode.value = result.dev_code || ''
    if (result.dev_code) form.code = result.dev_code
    ElMessage.success(result.message)
  } catch (error: any) {
    ElMessage.error(error.message)
  } finally {
    sendingCode.value = false
  }
}

async function onRegister() {
  try {
    loading.value = true
    const result = await authApi.register(form)
    auth.setAuth(result.access_token, result.user)
    ElMessage.success('注册成功')
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
  width: 520px;
  padding: 30px;
}

.auth-header {
  margin-bottom: 20px;
}

.inline-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
}

.dev-code {
  margin-top: 16px;
  padding: 12px;
  border-radius: 12px;
  background: #eef4ff;
  color: #2f5cd4;
}

.helper {
  margin-top: 16px;
  color: #6b7280;
  display: flex;
  gap: 8px;
  justify-content: center;
}
</style>
