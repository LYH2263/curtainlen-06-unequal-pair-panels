<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1>
<ul class="runs">
  <li v-for="r in items" :key="r.id" class="run">
    <span class="run-id">#{{ r.id }}</span>
    {{ r.window_name }} · {{ r.fabric_name }} —
    <template v-if="r.result?.left_panels !== undefined">
      左 {{ r.result.left_panels }} 幅 / 右 {{ r.result.right_panels }} 幅
      （左占比 {{ r.result.left_ratio }}）·
    </template>
    共 {{ r.result?.meters }} m
  </li>
</ul>
</div></template>
<style scoped>
.runs { list-style: none; padding: 0; }
.run { padding: .35rem 0; border-bottom: 1px solid #cfdce8; }
.run-id { font-weight: 700; color: #1a5276; margin-right: .5rem; }
</style>
