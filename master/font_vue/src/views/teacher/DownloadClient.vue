<template>
  <div class="page-padded">
    <h3 class="page-title">下载客户端</h3>
    <div class="download-cards">
      <div class="download-card">
        <div class="card-logo">
          <img src="@/assets/logo.png" alt="ScienceWord" width="121" height="120" />
        </div>
        <div class="card-bottom">
          <span class="card-label">ScienceWord&Marking for Windows</span>
          <i class="ri-windows-fill card-platform-icon"></i>
        </div>
      </div>

      <div class="spacer-40"></div>

      <div class="download-card">
        <div class="card-logo">
          <img src="@/assets/logo.png" alt="Marking" width="121" height="120" />
        </div>
        <div class="card-bottom">
          <span class="card-label">Marking for Android</span>
          <i class="ri-android-fill card-platform-icon android"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-padded { padding: 64px; display: flex; flex-direction: column; align-items: center; }
.page-title { display: none; }
.download-cards { display: flex; align-items: center; justify-content: center; }
.download-card {
  width: 500px; height: 400px;
  border: 0.8px solid #E5E7EB;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 10px 15px rgba(0,0,0,0.1);
  background: #fff;
  display: flex; flex-direction: column;
}
.card-logo { flex: 1; display: flex; align-items: center; justify-content: center; }
.card-bottom { height: 80px; border-top: 0.8px solid #E5E7EB; display: flex; align-items: center; justify-content: center; gap: 12px; }
.card-label { font-size: 18px; font-family: 'SourceHanSans-Medium', 'Noto Sans SC', sans-serif; color: #333; }
.card-platform-icon { font-size: 32px; color: #333; }
.card-platform-icon.android { font-size: 32px; color: #16A34A; }
.spacer-40 { width: 40px; }
</style>
