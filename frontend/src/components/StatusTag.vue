<template>
  <el-tag :type="tagType" effect="light" round>{{ label }}</el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ status: string }>()

const map = {
  pending: { label: '待解析', type: 'info' },
  processing: { label: '解析中', type: 'warning' },
  ready: { label: '已完成', type: 'success' },
  failed: { label: '失败', type: 'danger' }
} as const

const label = computed(() => map[props.status as keyof typeof map]?.label || props.status)
const tagType = computed(() => map[props.status as keyof typeof map]?.type || 'info')
</script>
