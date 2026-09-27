<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const props = defineProps({ id: String })
const w = ref(null)
const runs = ref([])
onMounted(async () => {
  w.value = await getJSON(`/api/windows/${props.id}`)
  runs.value = (await getJSON(`/api/runs?window_id=${props.id}`)).items
})
</script>
<template><div class="page" v-if="w"><h1>{{ w.name }}</h1>
<p v-if="w.data_quality==='dirty'" class="bad">{{ w.note }}</p>
<p>宽 {{ w.width }} 高 {{ w.height }} 褶倍 {{ w.fullness }}</p>
<h2 v-if="runs.length">最近一次分幅</h2>
<div v-if="runs.length" class="last-run">
  <p>第 {{ runs[0].id }} 单 · {{ runs[0].fabric_name }}</p>
  <p v-if="runs[0].result?.left_panels !== undefined">左占比 {{ runs[0].result.left_ratio }} · 左 {{ runs[0].result.left_panels }} 幅 / 右 {{ runs[0].result.right_panels }} 幅 · 共 {{ runs[0].result.meters }} m</p>
  <p v-else>共 {{ runs[0].result?.meters }} m（旧单未记录分幅）</p>
</div>
</div></template>
<style scoped>
.last-run { padding: .5rem .75rem; background: #d4e6f1; border-radius: 4px; max-width: 28rem; }
</style>
