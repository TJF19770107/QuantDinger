# workflow_dashboard_v2.0.html

> 原始文件: `workflow_dashboard_v2.0.html`  |  类型: `.html`  |  自动转换

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>工作流运行状态看板 v2.0 | 豆包Agent</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0d1117; color: #c9d1d9; font-family: 'SF Mono', 'Consolas', 'Microsoft YaHei Mono', monospace; padding: 24px; min-height: 100vh; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #21262d; }
.header h1 { font-size: 20px; font-weight: 600; color: #58a6ff; }
.header .badge { background: #238636; color: #fff; padding: 4px 12px; border-radius: 12px; font-size: 12px; }
.header .badge.error { background: #da3633; }

.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px; }
.card { background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 16px; }
.card .label { font-size: 12px; color: #8b949e; text-transform: uppercase; margin-bottom: 8px; }
.card .value { font-size: 28px; font-weight: 700; }
.card .value.success { color: #3fb950; }
.card .value.danger { color: #f85149; }
.card .value.warning { color: #d2991d; }
.card .value.info { color: #58a6ff; }

.progress-section { margin-bottom: 24px; }
.progress-bar { width: 100%; height: 8px; background: #21262d; border-radius: 4px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #238636, #3fb950); border-radius: 4px; transition: width 0.5s ease; }
.progress-text { font-size: 12px; color: #8b949e; margin-top: 8px; }

.node-list { background: #161b22; border: 1px solid #21262d; border-radius: 8px; overflow: hidden; }
.node-item { display: grid; grid-template-columns: 40px 1fr 80px 80px 60px; gap: 12px; padding: 12px 16px; border-bottom: 1px solid #21262d; align-items: center; font-size: 13px; }
.node-item:last-child { border-bottom: none; }
.node-item:hover { background: #1c2128; }
.node-item .icon { font-size: 18px; text-align: center; }
.node-item .name { font-weight: 500; }
.node-item .status { font-size: 11px; padding: 2px 8px; border-radius: 10px; text-align: center; }
.node-item .status.success { background: #23863633; color: #3fb950; }
.node-item .status.running { background: #1f6feb33; color: #58a6ff; }
.node-item .status.failed { background: #da363333; color: #f85149; }
.node-item .status.pending { background: #8b949e33; color: #8b949e; }
.node-item .time { text-align: right; color: #8b949e; font-size: 12px; }
.node-item .retries { text-align: center; font-size: 11px; color: #d2991d; }

.resource-section { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 24px; }
.resource-card { background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 16px; }
.resource-card .title { font-size: 12px; color: #8b949e; margin-bottom: 12px; }
.resource-card .meter { height: 6px; background: #21262d; border-radius: 3px; margin-bottom: 8px; }
.resource-card .meter-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }
.resource-card .meter-fill.cpu { background: #58a6ff; }
.resource-card .meter-fill.mem { background: #3fb950; }
.resource-card .meter-fill.parallel { background: #d2991d; }

.log-section { margin-top: 24px; background: #0d1117; border: 1px solid #21262d; border-radius: 8px; padding: 16px; max-height: 300px; overflow-y: auto; }
.log-section .title { font-size: 14px; font-weight: 600; margin-bottom: 12px; color: #58a6ff; }
.log-entry { font-size: 12px; padding: 4px 0; border-bottom: 1px solid #161b22; font-family: 'SF Mono', monospace; }
.log-entry .timestamp { color: #8b949e; margin-right: 12px; }
.log-entry .level-info { color: #58a6ff; }
.log-entry .level-warn { color: #d2991d; }
.log-entry .level-error { color: #f85149; }

.refresh-indicator { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #8b949e; }
.refresh-indicator .dot { width: 8px; height: 8px; border-radius: 50%; background: #3fb950; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }

/* 响应式 */
@media (max-width: 768px) {
  .node-item { grid-template-columns: 30px 1fr 60px; }
  .node-item .time, .node-item .retries { display: none; }
}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>⚙️ 工作流运行状态看板</h1>
    <span style="font-size:12px;color:#8b949e;">豆包Agent · R16 · v2.0</span>
  </div>
  <div style="display:flex;gap:12px;align-items:center;">
    <div class="refresh-indicator"><div class="dot"></div> 实时监控中</div>
    <span class="badge" id="statusBadge">▶ RUNNING</span>
  </div>
</div>

<!-- 统计卡片 -->
<div class="grid" id="statsGrid">
  <div class="card">
    <div class="label">总节点</div>
    <div class="value info" id="totalNodes">0</div>
  </div>
  <div class="card">
    <div class="label">✅ 成功</div>
    <div class="value success" id="successCount">0</div>
  </div>
  <div class="card">
    <div class="label">❌ 失败</div>
    <div class="value danger" id="failedCount">0</div>
  </div>
  <div class="card">
    <div class="label">⏳ 待定</div>
    <div class="value warning" id="pendingCount">0</div>
  </div>
  <div class="card">
    <div class="label">⏱ 总耗时</div>
    <div class="value" style="font-size:22px;" id="totalTime">--</div>
  </div>
</div>

<!-- 进度条 -->
<div class="progress-section">
  <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
  <div class="progress-text" id="progressText">进度: 0/0 节点 (0%)</div>
</div>

<!-- 节点列表 -->
<div class="node-list" id="nodeList">
  <div class="node-item" style="color:#8b949e;font-style:italic;">
    <div class="icon">—</div>
    <div class="name">等待工作流启动...</div>
    <div class="status pending">PENDING</div>
    <div class="time">—</div>
    <div class="retries">—</div>
  </div>
</div>

<!-- 资源面板 -->
<div class="resource-section">
  <div class="resource-card">
    <div class="title">🧠 推理引擎负载</div>
    <div class="meter"><div class="meter-fill cpu" id="cpuMeter" style="width:35%"></div></div>
    <span style="font-size:11px;color:#8b949e;" id="cpuText">3/5 并行路径 · 35%</span>
  </div>
  <div class="resource-card">
    <div class="title">💾 上下文缓存</div>
    <div class="meter"><div class="meter-fill mem" id="memMeter" style="width:45%"></div></div>
    <span style="font-size:11px;color:#8b949e;" id="memText">L1:3轮 L2:12快照 L3:48摘要 · 45%</span>
  </div>
  <div class="resource-card">
    <div class="title">🔀 并行度</div>
    <div class="meter"><div class="meter-fill parallel" id="parMeter" style="width:20%"></div></div>
    <span style="font-size:11px;color:#8b949e;" id="parText">1/5 最大并行 · 20%</span>
  </div>
</div>

<!-- 日志 -->
<div class="log-section">
  <div class="title">📋 实时日志流</div>
  <div id="logEntries">
    <div class="log-entry"><span class="timestamp">--:--:--</span>等待数据...</div>
  </div>
</div>

<script>
// 模拟数据更新函数
function updateDashboard(data) {
  const nodes = data.nodes || [];
  const total = nodes.length;
  let success = 0, failed = 0, pending = 0, running = 0;

  nodes.forEach(n => {
    if (n.status === 'success') success++;
    else if (n.status === 'failed' || n.status === 'timeout') failed++;
    else if (n.status === 'running') running++;
    else pending++;
  });

  const completed = success + failed;
  const progress = total > 0 ? (completed / total) * 100 : 0;

  // 统计卡片
  document.getElementById('totalNodes').textContent = total;
  document.getElementById('successCount').textContent = success;
  document.getElementById('failedCount').textContent = failed;
  document.getElementById('pendingCount').textContent = pending + running;
  document.getElementById('totalTime').textContent = (data.total_time_ms || 0).toFixed(0) + 'ms';

  // 进度条
  document.getElementById('progressFill').style.width = progress + '%';
  document.getElementById('progressText').textContent =
    `进度: ${completed}/${total} 节点 (${progress.toFixed(0)}%)` +
    (running > 0 ? ` · 🔄 ${running} 运行中` : '');

  // 状态徽章
  const badge = document.getElementById('statusBadge');
  if (failed > 0) {
    badge.textContent = '⚠ FAILED';
    badge.className = 'badge error';
  } else if (running > 0) {
    badge.textContent = '▶ RUNNING';
  } else if (pending === 0 && total > 0) {
    badge.textContent = '✓ COMPLETED';
  } else {
    badge.textContent = '⏳ PENDING';
  }

  // 节点列表
  const nodeList = document.getElementById('nodeList');
  if (nodes.length === 0) {
    nodeList.innerHTML = '<div class="node-item" style="color:#8b949e;font-style:italic;">暂无节点数据</div>';
  } else {
    nodeList.innerHTML = nodes.map(n => {
      const icon = n.status === 'success' ? '✅' : n.status === 'failed' ? '❌' :
                   n.status === 'running' ? '🔄' : n.status === 'timeout' ? '⏰' : '⏳';
      const statusClass = n.status === 'success' ? 'success' : n.status === 'failed' ? 'failed' :
                         n.status === 'running' ? 'running' : 'pending';
      const timeStr = n.time_ms ? n.time_ms.toFixed(0) + 'ms' : '—';
      const retryStr = n.retries > 0 ? '🔁' + n.retries : '—';
      return `<div class="node-item">
        <div class="icon">${icon}</div>
        <div class="name">${n.name || n.node_id || 'Unknown'}</div>
        <div class="status ${statusClass}">${n.status.toUpperCase()}</div>
        <div class="time">${timeStr}</div>
        <div class="retries">${retryStr}</div>
      </div>`;
    }).join('');
  }

  // 资源面板
  const cpuPct = data.resources?.cpu || 35;
  const memPct = data.resources?.memory || 45;
  const parPct = data.resources?.parallel || 20;

  document.getElementById('cpuMeter').style.width = cpuPct + '%';
  document.getElementById('memMeter').style.width = memPct + '%';
  document.getElementById('parMeter').style.width = parPct + '%';
  document.getElementById('cpuText').textContent = `推理引擎 · ${cpuPct}%`;
  document.getElementById('memText').textContent = `L1/L2/L3缓存 · ${memPct}%`;
  document.getElementById('parText').textContent = `并行节点 · ${parPct}%`;

  // 日志
  const logs = data.logs || [];
  const logDiv = document.getElementById('logEntries');
  if (logs.length === 0) {
    logDiv.innerHTML = '<div class="log-entry"><span class="timestamp">--:--:--</span>暂无日志</div>';
  } else {
    logDiv.innerHTML = logs.map(l => {
      const levelClass = l.level === 'WARN' ? 'level-warn' : l.level === 'ERROR' ? 'level-error' : 'level-info';
      return `<div class="log-entry">
        <span class="timestamp">${l.timestamp || '--:--:--'}</span>
        <span class="${levelClass}">[${l.level}]</span> ${l.msg || l.message || ''}
      </div>`;
    }).join('');
  }
}

// 示例数据（实际使用时替换为API调用）
const sampleData = {
  nodes: [
    { node_id: 'trigger_001', name: '定时触发', status: 'success', time_ms: 0, retries: 0 },
    { node_id: 'action_001', name: 'Phase1: 问题解析', status: 'success', time_ms: 120, retries: 0 },
    { node_id: 'action_002', name: 'Phase2: 条件拆解', status: 'success', time_ms: 85, retries: 0 },
    { node_id: 'action_003', name: 'Phase3: 逻辑推演', status: 'running', time_ms: 0, retries: 0 },
    { node_id: 'action_004', name: 'Phase4: 方案执行', status: 'pending', time_ms: 0, retries: 0 },
    { node_id: 'action_005', name: 'Phase5: 结果复盘', status: 'pending', time_ms: 0, retries: 0 },
  ],
  total_time_ms: 205,
  resources: { cpu: 35, memory: 45, parallel: 20 },
  logs: [
    { timestamp: '15:30:01', level: 'INFO', msg: '工作流启动: Claude推理v2.0 [wf_claude_v2]' },
    { timestamp: '15:30:01', level: 'INFO', msg: 'Phase1 问题解析完成 — 意图: general, 难度: L2' },
    { timestamp: '15:30:01', level: 'INFO', msg: 'Phase2 条件拆解完成 — 变量5个, 硬约束2个' },
    { timestamp: '15:30:01', level: 'INFO', msg: 'Phase3 逻辑推演中 — 生成4条推理路径' },
  ],
};

// 初始化
updateDashboard(sampleData);

// 模拟动态刷新
let counter = 0;
setInterval(() => {
  counter++;
  const updated = JSON.parse(JSON.stringify(sampleData));

  if (counter >= 3 && counter < 5) {
    updated.nodes[3].status = 'success';
    updated.nodes[3].time_ms = 450;
    updated.nodes[4].status = 'running';
    updated.logs.push({ timestamp: '15:30:03', level: 'INFO', msg: 'Phase3 逻辑推演完成 — 最优路径置信度: 0.75' });
    updated.logs.push({ timestamp: '15:30:03', level: 'INFO', msg: 'Phase4 方案执行中 — 工具联动回环启动' });
    updated.total_time_ms = 650 + counter * 100;
    updated.resources.cpu = 55;
    updated.resources.memory = 52;
    updated.resources.parallel = 40;
  } else if (counter >= 5 && counter < 7) {
    updated.nodes[4].status = 'success';
    updated.nodes[4].time_ms = 2300;
    updated.nodes[5].status = 'running';
    updated.logs.push({ timestamp: '15:30:05', level: 'INFO', msg: 'Phase4 执行完成 — 工具联动收敛于第3轮' });
    updated.total_time_ms = 2500 + counter * 50;
    updated.resources.cpu = 25;
  } else if (counter >= 7) {
    updated.nodes[5].status = 'success';
    updated.nodes[5].time_ms = 180;
    updated.logs.push({ timestamp: '15:30:05', level: 'INFO', msg: 'Phase5 复盘完成 — 质量评分: 0.87' });
    updated.logs.push({ timestamp: '15:30:05', level: 'INFO', msg: '工作流完成: 6/6节点成功, 总耗时2.7s' });
    updated.total_time_ms = 2700;
    updated.resources.cpu = 10;
    updated.resources.memory = 30;
    updated.resources.parallel = 0;
  }

  updateDashboard(updated);
}, 3000);
</script>

</body>
</html>
```
