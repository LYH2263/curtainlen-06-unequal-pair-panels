<script setup>
import { computed } from 'vue'
const props = defineProps({
  leftPanels: Number,
  rightPanels: Number,
  cutHeight: Number,
  meters: Number,
  leftRatio: Number,
})
const total = computed(() => (props.leftPanels || 0) + (props.rightPanels || 0))
const pct = computed(() => `${Math.round((props.leftRatio ?? 0.5) * 100)}%`)
const shown = (n) => Math.min(n || 0, 8)
</script>
<template>
  <div class="panel-cut">
    <div class="panel-col">
      <div class="panel-row">
        <div v-for="n in shown(leftPanels)" :key="'l' + n" class="panel panel-left" :style="{height: `${(cutHeight||1)*40}px`}"></div>
      </div>
      <span class="col-label">左 {{ leftPanels }} 幅</span>
    </div>
    <div class="panel-split"></div>
    <div class="panel-col">
      <div class="panel-row">
        <div v-for="n in shown(rightPanels)" :key="'r' + n" class="panel panel-right" :style="{height: `${(cutHeight||1)*40}px`}"></div>
      </div>
      <span class="col-label">右 {{ rightPanels }} 幅</span>
    </div>
    <p class="panel-sum">共 {{ total }} 幅 × {{ cutHeight }} m = {{ meters }} m（左占比 {{ pct }}）</p>
  </div>
</template>
<style scoped>
.panel-cut { display: block; margin-top: 1rem; }
.panel-col { display: inline-flex; flex-direction: column; gap: 4px; vertical-align: bottom; }
.panel-row { display: flex; gap: 6px; align-items: flex-end; }
.panel-split { display: inline-block; width: 2px; height: 120px; margin: 0 14px; background: #1a5276; vertical-align: bottom; }
.panel-left { background: #5dade2; border-color: #2874a6; }
.panel-right { background: #a9d3f0; border-color: #5dade2; }
.col-label { font-size: .85rem; color: #154360; }
.panel-sum { margin: .75rem 0 0; color: #154360; }
</style>
