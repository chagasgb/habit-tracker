<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import HabitList from './components/HabitList.vue'
import ProgressBar from './components/HabitProgress.vue'
import HabitCalendar from './components/HabitCalendar.vue'

/* ======================
   Abas / apps
====================== */

const activeTab = ref('habits')
const showAppNav = ref(true)

/* ======================
   Datas base
====================== */

const today = new Date()
today.setHours(0, 0, 0, 0)

const selectedDate = ref(new Date(today))
const progress = ref(0)

/* ======================
   Tipos da API
====================== */

interface CalendarDay {
  date: string
  day: number
  weekday: string
  completed: boolean
  percent: number
}

/* ======================
   Estado do calendário (API)
====================== */

const calendarCenter = ref<CalendarDay | null>(null)
const calendarDaysBefore = ref<CalendarDay[]>([])
const calendarDaysAfter = ref<CalendarDay[]>([])

/* ======================
   Labels
====================== */

const monthLabels = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril',
  'Maio', 'Junho', 'Julho', 'Agosto',
  'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

/* ======================
   Helpers
====================== */

function mapWeekday(weekday: string): string {
  const map: Record<string, string> = {
    Sun: 'Dom',
    Mon: 'Seg',
    Tue: 'Ter',
    Wed: 'Qua',
    Thu: 'Qui',
    Fri: 'Sex',
    Sat: 'Sáb'
  }
  return map[weekday] ?? ''
}

function formatISO(date: Date) {
  return date.toISOString().split('T')[0]
}

/* ======================
   Header mês / ano
====================== */

const monthYearLabel = computed(() => {
  return `${monthLabels[selectedDate.value.getMonth()]} ${selectedDate.value.getFullYear()}`
})

const showTodayButton = computed(() => {
  return formatISO(selectedDate.value) !== formatISO(today)
})

function goToToday() {
  selectedDate.value = new Date(today)
}

/* ======================
   Fetch Calendar API (HARDCODED)
====================== */

async function fetchCalendar(centerDate: Date) {
  const center = formatISO(centerDate)

  console.log('📅 Fetch calendar:', center)

  const res = await fetch(
    `http://localhost:8000/calendar/range?center=${center}&days_before=30&days_after=30`
  )

  console.log('📡 Status:', res.status)

  const data = await res.json()
  console.log('📦 Calendar data:', data)

  calendarCenter.value = data.center
  calendarDaysBefore.value = data.days_before ?? []
  calendarDaysAfter.value = data.days_after ?? []

  progress.value = data.center?.percent ?? 0
}

/* ======================
   Dias do calendário (API)
====================== */

const days = computed(() => {
  if (!calendarCenter.value) {
    console.warn('⚠️ calendarCenter vazio')
    return []
  }

  const allDays = [
    ...calendarDaysBefore.value,
    calendarCenter.value,
    ...calendarDaysAfter.value
  ]

  console.log('🗓️ Render days:', allDays.length)

  return allDays.map(d => ({
    date: d.date,
    day: d.day,
    label: mapWeekday(d.weekday),
    isToday: d.date === formatISO(today),
    isSelected: d.date === formatISO(selectedDate.value),
    percent: d.percent,
    completed: d.completed
  }))
})

/* ======================
   Ações
====================== */

function selectDay(dateISO: string) {
  selectedDate.value = new Date(dateISO)
}

/* ======================
   Progresso vindo do HabitList
====================== */

function onProgressUpdate(value: number) {
  progress.value = value
}

/* ======================
   Lifecycle
====================== */

onMounted(() => {
  fetchCalendar(selectedDate.value)
})

watch(selectedDate, (newDate) => {
  fetchCalendar(newDate)
})
</script>

<template>
  <div class="app">
    <div class="card">
      <template v-if="activeTab === 'habits'">
        <header class="calendar-header">
          <div class="month-container">
            <span class="month-year">
              {{ monthYearLabel }}
            </span>

            <button
              class="today-icon"
              :class="{ hidden: !showTodayButton }"
              title="Voltar para hoje"
              aria-label="Voltar para hoje"
              @click="goToToday"
            >
              ↻
            </button>
          </div>
        </header>

        <HabitCalendar
          :days="days"
          @select="selectDay"
        />

        <ProgressBar :percent="progress" />

        <section class="habits">
          <HabitList
            :date="selectedDate"
            @update:progress="onProgressUpdate"
          />
        </section>
      </template>
    </div>

    <button
      class="add-habit-btn"
      aria-label="Criar hábito"
      title="Criar hábito"
    >
      +
    </button>
  </div>
</template>


<style scoped>
/* CSS ORIGINAL — INALTERADO */
.app {
  min-height: 100vh;
  background: #0e0e11;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 24px;
  font-family: Inter, system-ui, sans-serif;
  position: relative;
  flex-wrap: wrap;
}

.card {
  width: 100%;
  max-width: 560px;
  height: 90vh;
  background: #18181b;
  border-radius: 28px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 22px;
  flex-shrink: 0;
}

.calendar-header {
  text-align: center;
}

.month-container {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.month-year {
  font-size: 14px;
  font-weight: 500;
  color: #a1a1aa;
  letter-spacing: 0.04em;
}

.today-icon {
  background: transparent;
  border: none;
  font-size: 13px;
  line-height: 1;
  color: #71717a;
  cursor: pointer;
  padding: 0;
}

.today-icon.hidden {
  visibility: hidden;
  pointer-events: none;
}

.today-icon:hover {
  color: #e5e7eb;
}

.habits {
  flex: 1;
  overflow-y: auto;
  scrollbar-gutter: stable;
}

.habits::-webkit-scrollbar {
  width: 6px;
}

.habits::-webkit-scrollbar-track {
  background: transparent;
}

.habits::-webkit-scrollbar-thumb {
  background-color: #2a2a2e;
  border-radius: 6px;
}

.habits {
  scrollbar-width: thin;
  scrollbar-color: #2a2a2e transparent;
}

/* ➕ BOTÃO FLUTUANTE GLOBAL */
.add-habit-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;

  width: 56px;
  height: 56px;
  border-radius: 18px;

  background: #27272a;
  border: none;
  color: #e5e7eb;

  font-size: 32px;
  font-weight: 300;
  line-height: 1;

  display: flex;
  align-items: center;
  justify-content: center;

  cursor: pointer;
  z-index: 50;

  transition: background 0.2s ease, transform 0.15s ease;
}

.add-habit-btn:hover {
  background: #3f3f46;
  transform: scale(1.1);
}

@media(min-width: 768px) {
  .app {
    flex-wrap: nowrap;
    justify-content: center;
    align-items: flex-start;
  }
}
</style>
