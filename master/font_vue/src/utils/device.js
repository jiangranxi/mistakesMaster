/**
 * 获取或生成设备标识，持久化到 localStorage。
 * 用于后端短信验证码每日发送次数限制。
 */
export function getDeviceId() {
  let id = localStorage.getItem('deviceId')
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem('deviceId', id)
  }
  return id
}
