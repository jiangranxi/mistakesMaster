// /**
//  * 获取或生成设备标识，持久化到 localStorage。
//  * 用于后端短信验证码每日发送次数限制。
//  * 异常时返回 null，不影响主流程。
//  */
// export function getDeviceId() {
//   try {
//     let id = localStorage.getItem('deviceId')
//     if (!id) {
//       id = crypto.randomUUID()
//       localStorage.setItem('deviceId', id)
//     }
//     return id
//   } catch {
//     // localStorage 不可用或无安全上下文时，返回 null 跳过设备限制
//     return null
//   }
// }
/**
 * 获取或生成设备标识，持久化到 localStorage。
 * 降级方案：当 crypto.randomUUID 不可用时（如 HTTP 环境），
 * 使用时间戳 + 随机字符串生成唯一 ID。
 */
export function getDeviceId() {
  try {
    let id = localStorage.getItem('deviceId');
    if (!id) {
      // 优先使用 crypto.randomUUID（仅 HTTPS）
      if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
        id = crypto.randomUUID();
      } else {
        // 降级：生成一个类似 UUID 的随机字符串
        const timestamp = Date.now().toString(36);
        const randomPart = Math.random().toString(36).slice(2, 10);
        id = `id-${timestamp}-${randomPart}`;
      }
      localStorage.setItem('deviceId', id);
    }
    return id;
  } catch {
    // 若 localStorage 不可用，返回 null（不影响主流程）
    return null;
  }
}

