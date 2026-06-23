<template>
  <div class="date-picker-wrapper" ref="wrapper">
    <input
      type="text"
      class="date-input"
      :value="modelValue"
      :placeholder="placeholder"
      readonly
      @click="open"
      @focus="open"
    />
    <i v-if="modelValue" class="ri-close-circle-line clear-icon" @click.stop="clear"></i>

    <Teleport to="body">
      <div v-if="visible" class="date-picker-overlay" @click="close">
        <div class="date-picker-popup" :style="popupStyle" @click.stop>
          <!-- 年/月导航 -->
          <div class="picker-header">
            <i class="ri-skip-left-line nav-arrow" @click="prevYear"></i>
            <i class="ri-arrow-left-s-line nav-arrow" @click="prevMonth"></i>
            <span class="year-month">{{ displayYear }}年 {{ displayMonth }}月</span>
            <i class="ri-arrow-right-s-line nav-arrow" @click="nextMonth"></i>
            <i class="ri-skip-right-line nav-arrow" @click="nextYear"></i>
          </div>

          <!-- 星期表头 -->
          <div class="week-row">
            <span v-for="d in weekDays" :key="d" class="week-day">{{ d }}</span>
          </div>

          <!-- 日期网格 -->
          <div class="date-grid">
            <span
              v-for="(day, i) in calendarDays"
              :key="i"
              class="date-cell"
              :class="{
                'other-month': !day.currentMonth,
                'selected': isSelected(day),
                'today': isToday(day)
              }"
              @click="selectDate(day)"
            >{{ day.date }}</span>
          </div>

          <!-- 底部按钮 -->
          <div class="picker-footer">
            <button class="btn-clear" @click="clear">清除</button>
            <button class="btn-now" @click="setNow">现在</button>
            <button class="btn-confirm" @click="confirm">确定</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: '请选择日期' }
})

const emit = defineEmits(['update:modelValue'])

const wrapper = ref(null)
const visible = ref(false)
const selectedYear = ref(new Date().getFullYear())
const selectedMonth = ref(new Date().getMonth() + 1)
const tempDate = ref('')

const weekDays = ['一', '二', '三', '四', '五', '六', '日']

const today = computed(() => {
  const d = new Date()
  return { year: d.getFullYear(), month: d.getMonth() + 1, date: d.getDate() }
})

// 弹出框定位
const popupStyle = computed(() => {
  if (!wrapper.value) return {}
  const rect = wrapper.value.getBoundingClientRect()
  return {
    position: 'absolute',
    top: rect.bottom + 4 + 'px',
    left: rect.left + 'px'
  }
})

// 可切换的显示年月
const displayYear = computed(() => selectedYear.value)
const displayMonth = computed(() => selectedMonth.value)

// 计算日历网格
const calendarDays = computed(() => {
  const year = selectedYear.value
  const month = selectedMonth.value
  const firstDay = new Date(year, month - 1, 1)
  const startDayOfWeek = firstDay.getDay() || 7 // 周日=7，转为周一=1

  const daysInMonth = new Date(year, month, 0).getDate()
  const prevMonthDays = new Date(year, month - 1, 0).getDate()

  const days = []

  // 上月末尾的几天
  const prevYear = month === 1 ? year - 1 : year
  const prevM = month === 1 ? 12 : month - 1
  for (let i = startDayOfWeek - 1; i > 0; i--) {
    days.push({
      year: prevYear,
      month: prevM,
      date: prevMonthDays - i + 1,
      currentMonth: false
    })
  }

  // 当月日期
  for (let d = 1; d <= daysInMonth; d++) {
    days.push({ year, month, date: d, currentMonth: true })
  }

  // 下月开头几天（补满 6 行）
  const remaining = 42 - days.length
  const nextYear = month === 12 ? year + 1 : year
  const nextM = month === 12 ? 1 : month + 1
  for (let d = 1; d <= remaining; d++) {
    days.push({ year: nextYear, month: nextM, date: d, currentMonth: false })
  }

  return days
})

function formatDate(y, m, d) {
  const mm = String(m).padStart(2, '0')
  const dd = String(d).padStart(2, '0')
  return `${y}-${mm}-${dd}`
}

function isSelected(day) {
  if (!tempDate.value) return false
  return tempDate.value === formatDate(day.year, day.month, day.date)
}

function isToday(day) {
  return day.year === today.value.year &&
    day.month === today.value.month &&
    day.date === today.value.date
}

function open() {
  if (props.modelValue) {
    const parts = props.modelValue.split('-')
    if (parts.length === 3) {
      selectedYear.value = parseInt(parts[0])
      selectedMonth.value = parseInt(parts[1])
      tempDate.value = props.modelValue
    } else {
      selectedYear.value = today.value.year
      selectedMonth.value = today.value.month
      tempDate.value = ''
    }
  } else {
    selectedYear.value = today.value.year
    selectedMonth.value = today.value.month
    tempDate.value = ''
  }
  visible.value = true
}

function close() {
  visible.value = false
}

function selectDate(day) {
  if (!day.currentMonth) return
  tempDate.value = formatDate(day.year, day.month, day.date)
}

function prevMonth() {
  if (selectedMonth.value === 1) {
    selectedMonth.value = 12
    selectedYear.value--
  } else {
    selectedMonth.value--
  }
}

function nextMonth() {
  if (selectedMonth.value === 12) {
    selectedMonth.value = 1
    selectedYear.value++
  } else {
    selectedMonth.value++
  }
}

function prevYear() {
  selectedYear.value--
}

function nextYear() {
  selectedYear.value++
}

function clear() {
  tempDate.value = ''
  emit('update:modelValue', '')
  visible.value = false
}

function setNow() {
  const d = today.value
  tempDate.value = formatDate(d.year, d.month, d.date)
  selectedYear.value = d.year
  selectedMonth.value = d.month
}

function confirm() {
  if (tempDate.value) {
    emit('update:modelValue', tempDate.value)
  }
  visible.value = false
}
</script>

<style scoped>
.date-picker-wrapper {
  position: relative;
  display: inline-block;
}

.date-input {
  width: 100%;
  height: 36px;
  padding: 0 28px 0 12px;
  border: 1px solid #E5E7EB;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  outline: none;
  cursor: pointer;
  background: #fff;
  box-sizing: border-box;
  font-family: inherit;
}
.date-input::placeholder { color: #999; }
.date-input:focus { box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }

.clear-icon {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  color: #9CA3AF;
  cursor: pointer;
  line-height: 1;
}
.clear-icon:hover { color: #6B7280; }

.date-picker-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
}

.date-picker-popup {
  position: fixed !important;
  width: 296px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  padding: 16px;
  z-index: 2001;
  font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
}

/* 头部年月导航 */
.picker-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.nav-arrow {
  font-size: 18px;
  color: #333;
  cursor: pointer;
  padding: 4px;
}
.nav-arrow:hover { color: #2563EB; }
.year-month {
  font-size: 16px;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
  color: #333;
}

/* 星期表头 */
.week-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  margin-bottom: 4px;
}
.week-day {
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #6B7280;
  font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif;
}

/* 日期网格 */
.date-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}
.date-cell {
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  border-radius: 4px;
}
.date-cell:hover { background: #EFF6FF; color: #2563EB; }
.date-cell.other-month { color: #D1D5DB; cursor: default; }
.date-cell.other-month:hover { background: transparent; color: #D1D5DB; }
.date-cell.today { color: #2563EB; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; }
.date-cell.selected { background: #2563EB; color: #fff; border-radius: 4px; }

/* 底部按钮 */
.picker-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #E5E7EB;
}
.picker-footer button {
  width: 20%;
  height: 32px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  font-family: 'SourceHanSans-Regular', 'Noto Sans SC', sans-serif;
}
.btn-clear {
  background: #F3F4F6;
  color: #6B7280;
}
.btn-clear:hover { background: #E5E7EB; }
.btn-now {
  background: #F3F4F6;
  color: #333;
}
.btn-now:hover { background: #E5E7EB; }
.btn-confirm {
  background: #2563EB;
  color: #fff;
}
.btn-confirm:hover { background: #3B82F6; }
</style>
