<template>
  <ul class="chapter-tree">
    <li v-for="node in nodes" :key="node.id" class="chapter-node">
      <div class="chapter-row">
        <!-- 折叠按钮：有子节点时显示 +/- -->
        <button
          v-if="node.children?.length"
          class="toggle-btn"
          @click="toggle(node.id)"
        >{{ expanded.has(node.id) ? '−' : '+' }}</button>
        <!-- 无子节点时显示占位，保持对齐 -->
        <span v-else class="toggle-placeholder"></span>
        <a href="#" class="chapter-link">{{ node.name }}</a>
      </div>
      <!-- 展开时渲染子节点 -->
      <ChapterTree
        v-if="expanded.has(node.id) && node.children?.length"
        :nodes="node.children"
      />
    </li>
  </ul>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  nodes: {
    type: Array,
    default: () => []
  }
})

const expanded = ref(new Set())

function toggle(id) {
  if (expanded.value.has(id)) {
    expanded.value.delete(id)
  } else {
    expanded.value.add(id)
  }
  // 触发响应式更新
  expanded.value = new Set(expanded.value)
}
</script>

<style scoped>
.chapter-tree {
  list-style: none;
  padding-left: 24px;
  margin: 0;
}
.chapter-node {
  margin: 4px 0;
}
.chapter-row {
  display: flex;
  align-items: center;
  gap: 4px;
}
.toggle-btn {
  width: 14px;
  height: 14px;
  border: none;
  border-radius: 2px;
  background: #D1D5DB;
  color: #6B7280;
  font-size: 10px;
  font-family: monospace;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  line-height: 1;
  flex-shrink: 0;
}
.toggle-btn:hover {
  background: #9CA3AF;
  color: #374151;
}
.toggle-placeholder {
  width: 14px;
  flex-shrink: 0;
}
.chapter-link {
  font-size: 16px;
  color: #2B7CD3;
  text-decoration: none;
  line-height: 24px;
}
.chapter-link:hover {
  text-decoration: underline;
}
</style>
