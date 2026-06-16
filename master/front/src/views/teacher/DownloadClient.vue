<template>
  <div class="download-page">
    <div class="card">
      <h3 class="page-title">下载客户端</h3>
      <div class="download-grid">
        <!-- Windows 版本 -->
        <div class="download-card">
          <div class="card-header">
            <div class="platform-logo">🖥️ ScienceWord</div>
          </div>
          <div class="card-body">
            <div class="os-icon">⊞</div>
            <h4>Windows 版本</h4>
            <p class="version">最新版本 v6.5</p>
            <p class="desc">支持 Windows 10/11 系统</p>
          </div>
          <div class="card-footer">
            <button class="btn btn-primary btn-lg" style="width:100%">下载 Windows 版</button>
          </div>
        </div>

        <!-- Android 版本 -->
        <div class="download-card">
          <div class="card-header">
            <div class="platform-logo">📱 Marking</div>
          </div>
          <div class="card-body">
            <div class="os-icon">🤖</div>
            <h4>Android 版本</h4>
            <p class="version">最新版本 v1.2.0</p>
            <p class="desc">支持 Android 8.0 及以上</p>
          </div>
          <div class="card-footer">
            <button class="btn btn-primary btn-lg" style="width:100%">下载 Android 版</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.page-title { font-size: 18px; margin-bottom: 24px; }
.download-grid { display: flex; gap: 40px; justify-content: center; flex-wrap: wrap; }
.download-card { width: 500px; background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,.06); overflow: hidden; }
.card-header { padding: 20px; background: #f0f5ff; text-align: center; }
.platform-logo { font-size: 24px; font-weight: 500; }
.card-body { padding: 40px 20px; text-align: center; }
.os-icon { font-size: 48px; margin-bottom: 16px; }
.card-body h4 { font-size: 20px; margin-bottom: 8px; }
.version { font-size: 14px; color: #4A90D9; margin-bottom: 4px; }
.desc { font-size: 13px; color: #999; }
.card-footer { padding: 20px; border-top: 1px solid #f0f0f0; }
</style>
