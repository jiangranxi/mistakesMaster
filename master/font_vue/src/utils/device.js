/**
 * 获取或生成设备标识，持久化到 localStorage。
 * 用于后端短信验证码每日发送次数限制。
 * 异常时返回 null，不影响主流程。
 */
export function getDeviceId() {
  try {
    let id = localStorage.getItem('deviceId')
    if (!id) {
      id = crypto.randomUUID()
      localStorage.setItem('deviceId', id)
    }
    return id
  } catch {
    // localStorage 不可用或无安全上下文时，返回 null 跳过设备限制
    return null
  }
}
