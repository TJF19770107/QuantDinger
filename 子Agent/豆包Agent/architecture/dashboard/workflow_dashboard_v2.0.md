# workflow_dashboard_v2.0.html

> 原始文件: `workflow_dashboard_v2.0.html`  |  类型: `.html`  |  自动转换

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>豆包Agent · 可视化工作流运行状态看板 v2.0</title>
<style>
/* ===== 暗色主题设计系统 ===== */
:root {
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --bg-tertiary: #21262d;
  --border: #30363d;
  --text-primary: #c9d1d9;
  --text-secondary: #8b949e;
  --text-link: #58a6ff;
  --success: #3fb950;
  --danger: #f85149;
  --warning: #d29922;
  --running: #58a6ff;
  --pending: #8b949e;
  --skipped: #6e7681;
  --timeout: #f0883e;
  --accent: #7c3aed;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  min-height: 100vh;
}

/* ===== 顶部导航栏 ===== */
.header {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, var(--accent), #a78bfa);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 16px; color: white;
}

.header h1 { font-size: 18px; font-weight: 600; }

.status-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot.running { background: var(--running); animation: pulse 2s infinite; }
.status-dot.idle { background: var(--text-secondary); }
.status-dot.error { background: var(--danger); }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* ===== 统计卡片区 ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  padding: 24px;
}

.stat-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: transform 0.2s, border-color 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.stat-value.success { color: var(--success); }
.stat-value.danger { color: var(--danger); }
.stat-value.warning { color: var(--warning); }
.stat-value.running { color: var(--running); }

/* ===== 进度条 ===== */
.progress-section {
  padding: 0 24px 24px;
}

.progress-bar-wrapper {
  background: var(--bg-tertiary);
  border-radius: 4px;
  height: 8px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--success), var(--running));
  transition: width 0.3s ease;
}

.progress-bar-fill.complete { background: var(--success); }
.progress-bar-fill.error { background: var(--danger); }

.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--text-secondary);
}

/* ===== 节点列表 ===== */
.nodes-section {
  padding: 0 24px 24px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0.5px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

.node-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.node-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: border-color 0.2s;
}

.node-card:hover { border-color: var(--accent); }

.node-icon {
  width: 36px; height: 36px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.node-icon.action { background: rgba(88, 166, 255, 0.15); color: var(--running); }
.node-icon.agent { background: rgba(163, 113, 247, 0.15); color: #a371f7; }
.node-icon.condition { background: rgba(210, 153, 34, 0.15); color: var(--warning); }
.node-icon.merge { background: rgba(108, 117, 125, 0.15); color: var(--text-secondary); }
.node-icon.terminal { background: rgba(63, 185, 80, 0.15); color: var(--success); }

.node-info { flex: 1; min-width: 0; }

.node-name {
  font-size: 14px; font-weight: 500;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.node-meta {
  font-size: 11px; color: var(--text-secondary);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.node-right { text-align: right; flex-shrink: 0; }

.node-time {
  font-size: 13px; font-variant-numeric: tabular-nums;
  font-family: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
}

.node-retry {
  font-size: 11px;
}

.node-retry.has-retry { color: var(--warning); }

/* ===== 状态徽章 ===== */
.badge {
  font-size: 11px; padding: 2px 8px;
  border-radius: 12px; font-weight: 500;
  display: inline-block;
}

.badge.success { background: rgba(63,185,80,0.15); color: var(--success); }
.badge.failed { background: rgba(248,81,73,0.15); color: var(--danger); }
.badge.running { background: rgba(88,166,255,0.15); color: var(--running); }
.badge.pending { background: rgba(139,148,158,0.15); color: var(--pending); }
.badge.timeout { background: rgba(240,136,62,0.15); color: var(--timeout); }
.badge.skipped { background: rgba(110,118,129,0.15); color: var(--skipped); }

/* ===== 日志面板 ===== */
.log-section { padding: 0 24px 24px; }

.log-panel {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.log-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 16px;
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border);
}

.log-tabs { display: flex; gap: 4px; }

.log-tab {
  font-size: 12px; padding: 4px 12px;
  border-radius: 4px; border: none; cursor: pointer;
  background: transparent; color: var(--text-secondary);
  font-family: inherit;
}

.log-tab.active {
  background: var(--accent); color: white;
}

.log-content {
  padding: 12px 16px;
  max-height: 300px; overflow-y: auto;
  font-family: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
  font-size: 12px; line-height: 1.8;
}

.log-line { display: flex; gap: 12px; }

.log-timestamp { color: var(--text-secondary); flex-shrink: 0; }
.log-level.error { color: var(--danger); }
.log-level.warn { color: var(--warning); }
.log-level.info { color: var(--running); }
.log-level.debug { color: var(--text-secondary); }

/* ===== 底部状态栏 ===== */
.footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border);
  padding: 8px 24px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 12px; color: var(--text-secondary);
}

.footer-left, .footer-right { display: flex; gap: 16px; align-items: center; }

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .header { padding: 10px 16px; }
  .stats-grid, .progress-section, .nodes-section, .log-section { padding: 12px 16px; }
}
</style>
</head>
<body>

<!-- 顶部导航 -->
<header class="header">
  <div class="header-left">
    <div class="logo">豆</div>
    <h1>豆包Agent · 工作流运行状态看板</h1>
  </div>
  <div>
    <span class="status-dot" id="globalStatus"></span>
    <span id="statusText" style="margin-left:8px;font-size:14px;">就绪</span>
  </div>
</header>

<!-- 统计卡片 -->
<div class="stats-grid" id="statsGrid">
  <div class="stat-card">
    <span class="stat-label">成功率</span>
    <span class="stat-value success" id="statSuccessRate">--</span>
  </div>
  <div class="stat-card">
    <span class="stat-label">已完成 / 总数</span>
    <span class="stat-value" id="statCompleted">--</span>
  </div>
  <div class="stat-card">
    <span class="stat-label">总耗时</span>
    <span class="stat-value" id="statTotalTime">--</span>
  </div>
  <div class="stat-card">
    <span class="stat-label">平均节点耗时</span>
    <span class="stat-value running" id="statAvgNodeTime">--</span>
  </div>
  <div class="stat-card">
    <span class="stat-label">重试次数</span>
    <span class="stat-value warning" id="statRetries">--</span>
  </div>
</div>

<!-- 进度条 -->
<div class="progress-section">
  <div class="progress-bar-wrapper">
    <div class="progress-bar-fill" id="progressBar" style="width:0%"></div>
  </div>
  <div class="progress-label">
    <span>进度 <span id="progressPercent">0%</span></span>
    <span><span id="progressDone">0</span> / <span id="progressTotal">0</span> 节点</span>
  </div>
</div>

<!-- 节点列表 -->
<div class="nodes-section">
  <div class="section-title">📋 节点执行详情</div>
  <div class="node-list" id="nodeList">
    <!-- JS动态生成 -->
  </div>
</div>

<!-- 日志面板 -->
<div class="log-section">
  <div class="log-panel">
    <div class="log-header">
      <div class="log-tabs">
        <button class="log-tab active" onclick="switchLogTab('all')">全部</button>
        <button class="log-tab" onclick="switchLogTab('error')">❌ 错误</button>
        <button class="log-tab" onclick="switchLogTab('warn')">⚠️ 警告</button>
        <button class="log-tab" onclick="switchLogTab('info')">ℹ️ 信息</button>
      </div>
      <span style="font-size:12px;color:var(--text-secondary)">共 <span id="logCount">0</span> 条</span>
    </div>
    <div class="log-content" id="logPanel">
      <div class="log-line">
        <span class="log-timestamp">--:--:--</span>
        <span style="color:var(--text-secondary)">等待工作流执行...</span>
      </div>
    </div>
  </div>
</div>

<!-- 底部状态栏 -->
<footer class="footer">
  <div class="footer-left">
    <span>引擎版本: v2.0</span>
    <span>执行模式: <span id="execMode">-</span></span>
  </div>
  <div class="footer-right">
    <span>更新时间: <span id="lastUpdate">-</span></span>
    <span>执行ID: <span id="execId">-</span></span>
  </div>
</footer>

<script>
// ===== 节点状态枚举 =====
const NodeStatus = {
  PENDING: 'pending', RUNNING: 'running', SUCCESS: 'success',
  FAILED: 'failed', SKIPPED: 'skipped', TIMEOUT: 'timeout'
};

const StatusIcons = {
  pending: '⏳', running: '🔄', success: '✅',
  failed: '❌', skipped: '⏭️', timeout: '⏰'
};

const StatusNames = { pending: '待定', running: '运行中', success: '成功',
  failed: '失败', skipped: '跳过', timeout: '超时' };

const NodeIcons = { action: '⚡', agent: '🤖', condition: '🔀',
  merge: '🔗', terminal: '🏁' };

const BadgeClass = { pending: 'pending', running: 'running', success: 'success',
  failed: 'failed', skipped: 'skipped', timeout: 'timeout' };

// ===== 状态数据 =====
let currentData = null;
let currentLogTab = 'all';

// 加载数据
function loadData(data) {
  currentData = data;

  // 全局状态
  const statusDot = document.getElementById('globalStatus');
  const statusText = document.getElementById('statusText');
  const totalNodes = data.nodes ? data.nodes.length : 0;
  const successCount = data.nodes ? data.nodes.filter(n => n.status === 'success').length : 0;
  const failedCount = data.nodes ? data.nodes.filter(n => n.status === 'failed').length : 0;
  const runningCount = data.nodes ? data.nodes.filter(n => n.status === 'running').length : 0;

  if (runningCount > 0) {
    statusDot.className = 'status-dot running';
    statusText.textContent = `运行中 · ${data.name || ''}`;
  } else if (failedCount > 0) {
    statusDot.className = 'status-dot error';
    statusText.textContent = `异常 · ${failedCount}个节点失败`;
  } else {
    statusDot.className = 'status-dot idle';
    statusText.textContent = `完成 · ${data.name || ''}`;
  }

  // 统计数据
  const successRate = totalNodes > 0 ? ((successCount / (successCount + failedCount || 1)) * 100).toFixed(0) : 0;
  const totalTime = data.nodes ? data.nodes.reduce((s, n) => s + (n.execution_time_ms || 0), 0) : 0;
  const avgNodeTime = totalNodes > 0 ? (totalTime / totalNodes).toFixed(0) : 0;
  const totalRetries = data.nodes ? data.nodes.reduce((s, n) => s + (n.retries || 0), 0) : 0;

  document.getElementById('statSuccessRate').textContent = successRate + '%';
  document.getElementById('statCompleted').textContent = `${successCount} / ${totalNodes}`;
  document.getElementById('statTotalTime').textContent = `${(totalTime/1000).toFixed(1)}s`;
  document.getElementById('statAvgNodeTime').textContent = `${avgNodeTime}ms`;
  document.getElementById('statRetries').textContent = totalRetries;

  // 进度条
  const done = successCount + failedCount;
  const progress = totalNodes > 0 ? (done / totalNodes * 100) : 0;
  const bar = document.getElementById('progressBar');
  bar.style.width = progress + '%';
  bar.className = 'progress-bar-fill';
  if (failedCount > 0 && runningCount === 0) bar.classList.add('error');
  if (done === totalNodes && failedCount === 0) bar.classList.add('complete');

  document.getElementById('progressPercent').textContent = Math.round(progress) + '%';
  document.getElementById('progressDone').textContent = done;
  document.getElementById('progressTotal').textContent = totalNodes;

  // 节点列表
  renderNodes(data.nodes || []);

  // 日志
  renderLogs(data.logs || []);
  document.getElementById('logCount').textContent = (data.logs || []).length;

  // 底部信息
  document.getElementById('execMode').textContent = data.execution_mode || '-';
  document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString('zh-CN');
  document.getElementById('execId').textContent = (data.execution_id || '-').substring(0, 16);
}

function renderNodes(nodes) {
  const container = document.getElementById('nodeList');
  container.innerHTML = nodes.map(node => `
    <div class="node-card">
      <div class="node-icon ${node.node_type || 'action'}">
        ${NodeIcons[node.node_type] || '⚡'}
      </div>
      <div class="node-info">
        <div class="node-name">${escapeHtml(node.display_name || node.node_id || '-')}</div>
        <div class="node-meta">ID: ${escapeHtml((node.node_id || '-').substring(0, 16))}</div>
      </div>
      <div class="node-right">
        <div class="node-time">${formatTime(node.execution_time_ms)}</div>
        ${node.retries > 0 ? `<div class="node-retry has-retry">重试 ×${node.retries}</div>` : ''}
        <span class="badge ${BadgeClass[node.status] || 'pending'}">${StatusNames[node.status] || '未知'}</span>
      </div>
    </div>
  `).join('');
}

function renderLogs(logs) {
  const container = document.getElementById('logPanel');
  let filtered = logs;
  if (currentLogTab !== 'all') {
    filtered = logs.filter(l => l.level === currentLogTab);
  }

  if (filtered.length === 0) {
    container.innerHTML = `<div style="color:var(--text-secondary);font-style:italic;">暂无日志</div>`;
    return;
  }

  container.innerHTML = filtered.map(l => `
    <div class="log-line">
      <span class="log-timestamp">${l.timestamp || '--:--:--'}</span>
      <span class="log-level ${l.level || 'info'}">[${(l.level || 'INFO').toUpperCase()}]</span>
      <span>${escapeHtml(l.node_id ? `[${l.node_id.substring(0,8)}] ` : '')}${escapeHtml(l.message || '')}</span>
    </div>
  `).join('');
}

function switchLogTab(tab) {
  currentLogTab = tab;
  document.querySelectorAll('.log-tab').forEach(btn => {
    btn.classList.toggle('active', btn.textContent.includes(
      tab === 'all' ? '全部' : tab === 'error' ? '错误' : tab === 'warn' ? '警告' : '信息'
    ));
  });
  if (currentData) renderLogs(currentData.logs || []);
}

function formatTime(ms) {
  if (!ms && ms !== 0) return '--';
  if (ms < 1000) return `${ms.toFixed(0)}ms`;
  return `${(ms/1000).toFixed(1)}s`;
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML.replace(/\n/g, '<br>');
}

// ===== 数据拉取定时器 =====
// 通过 Python/Flask 提供 JSON API 时启用
const UPDATE_INTERVAL = 5000; // 5秒刷新

function fetchStatus() {
  // 本地开发时可使用示例数据
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // 尝试从 /api/workflow/status 拉取
    fetch('/api/workflow/status')
      .then(r => r.json())
      .then(data => loadData(data))
      .catch(() => console.log('开发模式：等待API就绪'));
  } else {
    // 静态模式：通过 window.__WORKFLOW_DATA__ 注入数据
    if (window.__WORKFLOW_DATA__) {
      loadData(window.__WORKFLOW_DATA__);
    }
  }
}

// 初始加载
document.addEventListener('DOMContentLoaded', () => {
  fetchStatus();
  setInterval(fetchStatus, UPDATE_INTERVAL);
});

// 暴露全局函数供外部调用
window.loadWorkflowData = loadData;
window.updateNodeStatus = function(nodeId, status, timeMs) {
  if (!currentData || !currentData.nodes) return;
  const node = currentData.nodes.find(n => n.node_id === nodeId);
  if (node) {
    node.status = status;
    node.execution_time_ms = timeMs;
    renderNodes(currentData.nodes);
  }
};
window.addLog = function(timestamp, level, nodeId, message) {
  if (!currentData) currentData = { nodes: [], logs: [] };
  if (!currentData.logs) currentData.logs = [];
  currentData.logs.push({ timestamp, level, node_id: nodeId, message });
  document.getElementById('logCount').textContent = currentData.logs.length;
  renderLogs(currentData.logs);
};

// 示例数据（开发用）
window.__DEMO_DATA__ = {
  execution_id: 'exec_20260531_R13_001',
  name: 'R13全域缺口专项补全',
  execution_mode: 'PARALLEL',
  nodes: [
    { node_id: 'node_claude_reasoning', display_name: 'Claude推理增强v2.0', node_type: 'action',
      status: 'success', execution_time_ms: 2450, retries: 0 },
    { node_id: 'node_workflow_dashboard', display_name: '可视化看板生成', node_type: 'action',
      status: 'success', execution_time_ms: 1800, retries: 0 },
    { node_id: 'node_skill_extractor', display_name: '技能自动萃取', node_type: 'agent',
      status: 'success', execution_time_ms: 3200, retries: 1 },
    { node_id: 'node_obsidian_bridge', display_name: 'Obsidian双向同步', node_type: 'agent',
      status: 'success', execution_time_ms: 1100, retries: 0 },
    { node_id: 'node_integration_test', display_name: '集成验证', node_type: 'action',
      status: 'running', execution_time_ms: 1200, retries: 0 },
    { node_id: 'node_final_report', display_name: '迭代报告生成', node_type: 'terminal',
      status: 'pending', execution_time_ms: 0, retries: 0 },
  ],
  logs: [
    { timestamp: '14:30:01', level: 'info', node_id: 'node_claude_reasoning', message: 'Claude推理引擎v2.0加载完成' },
    { timestamp: '14:30:03', level: 'info', node_id: 'node_claude_reasoning', message: '中文意图分类器初始化：6大领域' },
    { timestamp: '14:30:05', level: 'info', node_id: 'node_workflow_dashboard', message: '可视化看板HTML模板已生成' },
    { timestamp: '14:30:07', level: 'warn', node_id: 'node_skill_extractor', message: '首次执行失败，自动重试 (1/2)' },
    { timestamp: '14:30:09', level: 'info', node_id: 'node_skill_extractor', message: '技能萃取：发现3个可萃取模式' },
    { timestamp: '14:30:10', level: 'info', node_id: 'node_obsidian_bridge', message: 'Obsidian桥接器已就绪' },
    { timestamp: '14:30:11', level: 'info', node_id: 'node_integration_test', message: '开始集成验证...' },
  ]
};

// 如果页面是通过 file:// 打开的，加载示例数据
if (window.location.protocol === 'file:') {
  document.addEventListener('DOMContentLoaded', () => {
    loadData(window.__DEMO_DATA__);
  });
}
</script>

</body>
</html>
```
