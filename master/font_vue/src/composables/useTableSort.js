import { ref, computed } from 'vue'

/**
 * 表格多列排序 composable
 *
 * 规则：
 * - 默认两箭头都不激活，按后端返回顺序展示
 * - 点击上三角 → 升序（上三角激活蓝色）
 * - 点击下三角 → 降序（下三角激活蓝色）
 * - 再点击 → 取消排序（两箭头均灰色）
 * - 多列排序：按点击顺序决定优先级，先点的优先；仅在前列值相同时才比较后列
 */
export function useTableSort(dataRef) {
  // 有序列表，第一项 = 最高优先级
  const sortEntries = ref([])

  /** 切换某列的排序状态：'' → asc → desc → '' */
  function toggleSort(key) {
    const idx = sortEntries.value.findIndex(e => e.key === key)
    if (idx === -1) {
      // 未排序 → 升序，追加到末尾（最低优先级，仅影响前列值相同的行）
      sortEntries.value = [...sortEntries.value, { key, direction: 'asc' }]
    } else if (sortEntries.value[idx].direction === 'asc') {
      // 升序 → 降序
      sortEntries.value = sortEntries.value.map((e, i) =>
        i === idx ? { key, direction: 'desc' } : e
      )
    } else {
      // 降序 → 移除
      sortEntries.value = sortEntries.value.filter((_, i) => i !== idx)
    }
  }

  /** 获取某列的当前排序方向：'' | 'asc' | 'desc' */
  function getSortState(key) {
    const entry = sortEntries.value.find(e => e.key === key)
    return entry ? entry.direction : ''
  }

  /** 按 sortEntries 顺序依次比较的多列排序结果 */
  const sortedData = computed(() => {
    const arr = dataRef.value
    if (!sortEntries.value.length || !arr) return arr || []
    return [...arr].sort((a, b) => {
      for (const { key, direction } of sortEntries.value) {
        let va = a[key]; let vb = b[key]
        if (va == null) va = ''
        if (vb == null) vb = ''
        if (va === vb) continue
        const cmp = va > vb ? 1 : -1
        return direction === 'asc' ? cmp : -cmp
      }
      return 0
    })
  })

  return { sortEntries, toggleSort, getSortState, sortedData }
}
