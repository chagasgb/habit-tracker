<script setup lang="ts">
defineProps({
  percent: Number
});
</script>

<template>
  <div class="progress-bar">
    <div
      class="progress-fill"
      :style="{ width: percent + '%' }"
    />
  </div>
</template>

<style scoped>
.progress-bar {
  height: 4px;
  background: #2a2a2f;
  border-radius: 999px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s ease;
}
</style>