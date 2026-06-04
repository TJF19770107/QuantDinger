# 龙虾AI主控中心 - GitHub自动备份脚本
# 任务ID: GitHub_Backup_AI_Clone
# 仓库: https://github.com/TJF19770107/my-ai-clone.git

$repoPath = "E:\龙虾AI主控中心\我的AI分身"
$logDir = "E:\龙虾AI主控中心\备份日志"
$maxRetries = 3
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 确保日志目录存在
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = Join-Path $logDir "backup_$(Get-Date -Format 'yyyyMMdd').log"

function Write-Log {
    param([string]$msg)
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Write-Output $line
    Add-Content -Path $logFile -Value $line
}

Write-Log "========== 备份任务启动 =========="

Set-Location $repoPath

# 检查网络连通性
$networkOk = Test-Connection -ComputerName github.com -Count 1 -Quiet -ErrorAction SilentlyContinue
if (-not $networkOk) {
    Write-Log "ERROR: GitHub 不可达，放弃本次备份"
    exit 1
}

# 拉取远程更新
git pull origin main 2>&1 | ForEach-Object { Write-Log "PULL: $_" }

# 暂存所有变更
git add -A 2>&1 | ForEach-Object { Write-Log "ADD: $_" }

# 检查是否有变更
$status = git status --porcelain
if (-not $status) {
    Write-Log "无变更，跳过提交"
    Write-Log "========== 备份任务结束（无变更） =========="
    exit 0
}

# 提交
$commitMsg = "自动备份 $timestamp"
git commit -m $commitMsg 2>&1 | ForEach-Object { Write-Log "COMMIT: $_" }

# 推送（含重试）
$pushSuccess = $false
for ($i = 1; $i -le $maxRetries; $i++) {
    Write-Log "推送尝试 $i / $maxRetries"
    $pushResult = git push origin main 2>&1
    $pushResult | ForEach-Object { Write-Log "PUSH: $_" }
    if ($LASTEXITCODE -eq 0) {
        $pushSuccess = $true
        Write-Log "推送成功"
        break
    }
    if ($i -lt $maxRetries) {
        Write-Log "推送失败，等待 30 秒后重试..."
        Start-Sleep -Seconds 30
    }
}

if (-not $pushSuccess) {
    Write-Log "ERROR: 推送失败，已重试 $maxRetries 次"
}

Write-Log "========== 备份任务结束 =========="
exit $(if ($pushSuccess) { 0 } else { 1 })
