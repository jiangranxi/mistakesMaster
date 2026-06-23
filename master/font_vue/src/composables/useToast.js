import { ref } from 'vue'

const toasts = ref([])
let id = 0

export function useToast() {
  function show(message, type = 'info', duration = 3000) {
    const toast = { id: ++id, message, type }
    toasts.value.push(toast)
    if (duration > 0) {
      setTimeout(() => remove(toast.id), duration)
    }
  }

  function success(message) { show(message, 'success') }
  function error(message) { show(message, 'error') }
  function info(message) { show(message, 'info') }

  function remove(toastId) {
    const idx = toasts.value.findIndex(t => t.id === toastId)
    if (idx > -1) toasts.value.splice(idx, 1)
  }

  return { toasts, show, success, error, info, remove }
}
