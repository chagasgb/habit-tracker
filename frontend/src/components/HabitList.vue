<script setup lang="ts">
import { ref, watch, computed } from "vue"

interface Habit {
  id: number
  name: string
  done: boolean
}

/* 🔥 MOCK: streak fixo só para teste */
interface HabitWithStreak extends Habit {
  streak: number
}

const props = defineProps<{ date: Date }>()
const emit = defineEmits<{
  (e: "update:progress", value: number): void
}>()

const habits = ref<HabitWithStreak[]>([])
const cache = new Map<string, HabitWithStreak[]>()
let abortController: AbortController | null = null

function formatDate(d: Date) {
  return d.toISOString().slice(0, 10)
}

async function loadHabits(date: Date) {
  const key = formatDate(date)

  if (cache.has(key)) {
    habits.value = cache.get(key)!.map(h => ({ ...h }))
    emitProgress()
    return
  }

  if (abortController) abortController.abort()
  abortController = new AbortController()

  try {
    const res = await fetch(
      `http://localhost:8000/habits/scheduled?date=${key}`,
      { signal: abortController.signal }
    )

    const data = await res.json()

    /* 🔥 injeta streak = 2 para todos (mock) */
    const withStreak = data.map((h: Habit) => ({
      ...h,
      streak: 2
    }))

    habits.value = withStreak.map(h => ({ ...h }))
    cache.set(key, withStreak.map(h => ({ ...h })))
    emitProgress()
  } catch {}
}

function toggleHabit(h: HabitWithStreak) {
  habits.value = habits.value.map(habit =>
    habit.id === h.id ? { ...habit, done: !habit.done } : habit
  )
  emitProgress()
}

const progressPercent = computed(() => {
  if (!habits.value.length) return 0
  const done = habits.value.filter(h => h.done).length
  return Math.round((done / habits.value.length) * 100)
})

function emitProgress() {
  emit("update:progress", progressPercent.value)
}

watch(() => props.date, loadHabits, { immediate: true })
</script>

<template>
  <div class="habit-container">
    <div class="habits-list">
      <div
        v-for="habit in habits"
        :key="habit.id"
        class="habit-item"
        :class="{ 'is-done': habit.done }"
        @click="toggleHabit(habit)"
      >
        <!-- CHECK -->
        <div class="check-box">
          <div class="custom-check">
            <div class="dot"></div>
          </div>
        </div>

        <!-- CONTENT -->
        <div class="content">
          <span class="name">{{ habit.name }}</span>
        </div>

        <!-- 🔥 STREAK -->
        <div
          v-if="habit.streak > 0"
          class="streak"
          aria-hidden="true"
        >
          <svg
            class="flame"
            viewBox="0 0 24 24"
          >
            <path
              d="M12 3c2 3 5 4.5 5 8a5 5 0 1 1-10 0c0-2.5 1.5-4 3-5.5 0 2 1 3 2 4 0-2.5 1-4 0-6z"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linejoin="round"
            />
          </svg>
          <span class="streak-count">{{ habit.streak }}</span>
        </div>

        <!-- ACTIONS -->
        <div class="actions-group" @click.stop>
          <button class="tool-btn edit-btn">
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.habit-container {
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
}

.habits-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.habit-item {
  background: #1c1c1f;
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  cursor: pointer;
  border: 1px solid transparent;
  transition: background 0.25s ease, border-color 0.25s ease;
  position: relative;
}

.habit-item:hover {
  background: #242427;
  border-color: #2d2d30;
}

/* CHECK */
.check-box {
  margin-right: 12px;
}

.custom-check {
  width: 18px;
  height: 18px;
  border: 1.5px solid #3f3f46;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dot {
  width: 0;
  height: 0;
  background-color: #3b82f6;
  border-radius: 50%;
  transition: 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.is-done {
  opacity: 0.4;
}

.is-done .name {
  text-decoration: line-through;
  color: #52525b;
}

.is-done .dot {
  width: 10px;
  height: 10px;
}

.is-done .custom-check {
  border-color: #3b82f6;
}

/* CONTENT */
.content {
  flex: 1;
}

.name {
  font-size: 14px;
  color: #d4d4d8;
}

/* 🔥 STREAK */
.streak {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-right: 6px;
  color: #f59e0b;
  opacity: 0.9;
}

.flame {
  width: 14px;
  height: 14px;
  margin-top: 4px; /* ↓ alinha melhor com o número */
}

.streak-count {
  font-size: 12px;
  font-weight: 500;
}

/* ACTIONS */
.actions-group {
  display: flex;
  opacity: 0;
  transition: 0.2s ease;
}

.habit-item:hover .actions-group {
  opacity: 1;
}

.tool-btn {
  color: #3f3f46;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
}

.tool-btn:hover {
  color: #d4d4d8;
}
</style>
