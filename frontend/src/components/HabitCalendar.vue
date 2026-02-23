<script setup lang="ts">
/* ======================
   Tipos
====================== */

interface DayItem {
  day: number
  label: string
  date: string
  isSelected: boolean
  isToday: boolean
  percent: number
  completed: boolean
}

/* ======================
   Props
====================== */

const props = defineProps<{
  days: DayItem[]
}>()

/* ======================
   Emits
====================== */

const emit = defineEmits<{
  (e: 'select', date: string): void
}>()

/* ======================
   Handlers
====================== */

function selectDay(date: string) {
  emit('select', date)
}

function onKeySelect(e: KeyboardEvent, date: string) {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault()
    emit('select', date)
  }
}
</script>

<template>
  <section class="days">
    <div
      v-for="day in props.days"
      :key="day.date"
      class="day"
      :class="{
        active: day.isSelected,
        today: day.isToday
      }"
      role="button"
      tabindex="0"
      @click="selectDay(day.date)"
      @keydown="onKeySelect($event, day.date)"
    >
      <!-- 👑 COROA — hábito completo -->
      <svg
        v-if="day.completed"
        class="crown"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path
          d="M3 7l4 4 5-6 5 6 4-4v10H3V7z"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linejoin="round"
        />
      </svg>

      <!-- Hoje -->
      <span v-if="day.isToday" class="today-dot"></span>

      <span class="label">{{ day.label }}</span>
      <span class="number">{{ day.day }}</span>
    </div>
  </section>
</template>

<style scoped>
.days {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 8px 4px;
}

.day {
  min-width: 56px;
  padding: 10px 6px;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  position: relative;
  user-select: none;
  transition: background 0.15s ease, color 0.15s ease;
}

.day:hover {
  background: rgba(0, 0, 0, 0.05);
}

.day.active {
  background: rgba(0, 0, 0, 0.08);
  font-weight: 600;
}

.day.today .number {
  font-weight: 700;
}

.label {
  display: block;
  font-size: 12px;
  opacity: 0.7;
}

.number {
  display: block;
  font-size: 16px;
}

.today-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.crown {
  position: absolute;
  top: 6px;
  left: 6px;
  width: 14px;
  height: 14px;
}
</style>


<style scoped>
.days {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 5px;
}

.arrow {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 24px;
  cursor: pointer;
  padding: 0 5px;
}

.day {
  position: relative;
  flex: 1;
  background: #222226;
  border-radius: 16px;
  padding: 12px 0;
  text-align: center;
  cursor: pointer;
}

.day.active {
  outline: 2px solid #3b82f6;
  background: #1f2937;
}

/* 👑 SVG minimalista */
.crown {
  position: absolute;
  top: -16px;
  left: 50%;
  transform: translateX(-50%);
  width: 14px;
  height: 14px;
  color: #facc15; /* dourado suave */
  opacity: 0.9;
}

/* Hoje */
.today-dot {
  position: absolute;
  top: 6px;
  left: 50%;
  transform: translateX(-50%);
  width: 5px;
  height: 5px;
  background: #3b82f6;
  border-radius: 50%;
}

.label {
  display: block;
  font-size: 11px;
  color: #9ca3af;
  margin-top: 4px;
}

.number {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
}
</style>
