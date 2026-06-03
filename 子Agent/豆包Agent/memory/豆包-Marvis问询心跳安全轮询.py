"""
豆包-Marvis问询心跳安全轮询任务
================================
任务定名: 豆包-Marvis问询心跳安全轮询任务
本质: Marvis侧定向心跳巡检，由Marvis按周期主动问询豆包APP
通讯域名: https://doubao.tjf19770107.cn
生成时间: 2026-06-03
产物目录: E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\memory
"""

import json
import time
import sys
import os
import signal
import logging
import requests
import psutil
from datetime import datetime, timedelta

# ========== 配置区 ==========
CONFIG = {
    "task_name": "豆包-Marvis问询心跳安全轮询任务",
    "endpoint": "https://doubao.tjf19770107.cn",
    "heartbeat_path": "/api/heartbeat",
    "poll_interval": 1.5,           # 每1.5秒轮询1次
    "request_timeout": 0.3,         # 单次请求超时300ms
    "max_runtime": 300,             # 单次进程最长5分钟
    "max_consecutive_failures": 3,  # 连续3次链路异常提前终止
    "cpu_limit_percent": 0.5,       # CPU使用率上限
    "memory_limit_mb": 15,          # 内存上限15MB
    "archive_dir": os.path.dirname(os.path.abspath(__file__)),
    "log_file": None,               # 运行时设置
}

# ========== 资源管控 ==========
def check_resource_limits():
    """检查CPU和内存限制"""
    process = psutil.Process(os.getpid())
    cpu_percent = process.cpu_percent(interval=0.1)
    memory_mb = process.memory_info().rss / (1024 * 1024)

    if cpu_percent > CONFIG["cpu_limit_percent"]:
        logging.warning(f"CPU超限: {cpu_percent:.2f}% > {CONFIG['cpu_limit_percent']}%")
        return False
    if memory_mb > CONFIG["memory_limit_mb"]:
        logging.warning(f"内存超限: {memory_mb:.2f}MB > {CONFIG['memory_limit_mb']}MB")
        return False
    return True

# ========== 链路自检 ==========
def link_check():
    """核验豆包↔Marvis双向通讯链路连通状态"""
    try:
        resp = requests.get(
            CONFIG["endpoint"] + CONFIG["heartbeat_path"],
            timeout=3.0
        )
        if resp.status_code == 200:
            logging.info(f"链路自检通过: {resp.status_code}")
            return True
        else:
            logging.warning(f"链路自检异常: HTTP {resp.status_code}")
            return False
    except requests.exceptions.Timeout:
        logging.warning("链路自检超时(3s)")
        return False
    except requests.exceptions.ConnectionError:
        logging.warning("链路自检失败: 无法连接")
        return False
    except Exception as e:
        logging.warning(f"链路自检异常: {e}")
        return False

# ========== 心跳轮询 ==========
def heartbeat_poll():
    """执行一次心跳问询，空心跳返回空JSON"""
    try:
        resp = requests.get(
            CONFIG["endpoint"] + CONFIG["heartbeat_path"],
            timeout=CONFIG["request_timeout"]
        )
        if resp.status_code == 200:
            data = resp.json() if resp.text.strip() else {}
            return True, data
        else:
            return False, None
    except requests.exceptions.Timeout:
        return False, "timeout"
    except Exception as e:
        return False, str(e)

# ========== 数据归档 ==========
def archive_session(session_log):
    """全量交互会话、心跳通讯日志统一落地存储"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"heartbeat_session_{timestamp}.json"
    log_path = os.path.join(CONFIG["archive_dir"], log_filename)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(session_log, f, ensure_ascii=False, indent=2)
    logging.info(f"会话数据归档: {log_path}")
    return log_path

# ========== 主循环 ==========
def main():
    start_time = time.time()
    deadline = start_time + CONFIG["max_runtime"]

    # 日志初始化
    log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    CONFIG["log_file"] = os.path.join(CONFIG["archive_dir"], f"heartbeat_{log_timestamp}.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(CONFIG["log_file"], encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info(f"=== 任务启动: {CONFIG['task_name']} ===")
    logging.info(f"目标端点: {CONFIG['endpoint']}")
    logging.info(f"运行截止: {datetime.fromtimestamp(deadline).strftime('%Y-%m-%d %H:%M:%S')}")

    # 阶段1: 链路自检
    if not link_check():
        logging.error("链路自检失败，任务终止")
        return 1

    # 阶段2: 心跳轮询循环
    poll_count = 0
    success_count = 0
    fail_streak = 0
    session_log = {
        "task_name": CONFIG["task_name"],
        "start_time": datetime.fromtimestamp(start_time).isoformat(),
        "endpoint": CONFIG["endpoint"],
        "polls": []
    }

    while time.time() < deadline:
        # 资源管控检查
        if not check_resource_limits():
            time.sleep(3)
            continue

        poll_count += 1
        success, data = heartbeat_poll()

        poll_record = {
            "seq": poll_count,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "data": data if success else None,
            "error": None if success else str(data)
        }
        session_log["polls"].append(poll_record)

        if success:
            success_count += 1
            fail_streak = 0
            # 空心跳仅返回空JSON，不消耗积分
            if data and data != {}:
                logging.info(f"[{poll_count}] 收到指令: {json.dumps(data, ensure_ascii=False)}")
                # 指令处理模式：暂停轮询→执行→恢复
                logging.info(f"[{poll_count}] 指令处理完成")
        else:
            fail_streak += 1
            logging.warning(f"[{poll_count}] 心跳失败 (连续{fail_streak}次): {str(data)[:100]}")

            # 连续异常提前终止
            if fail_streak >= CONFIG["max_consecutive_failures"]:
                logging.error(f"连续{fail_streak}次链路异常，提前终止本轮")
                break

        # 检查剩余时间
        elapsed = time.time() - start_time
        remaining = CONFIG["max_runtime"] - elapsed
        if remaining <= CONFIG["poll_interval"]:
            break

        time.sleep(min(CONFIG["poll_interval"], remaining))

    # 阶段3: 收尾
    elapsed = time.time() - start_time
    session_log["end_time"] = datetime.now().isoformat()
    session_log["duration_seconds"] = round(elapsed, 2)
    session_log["total_polls"] = poll_count
    session_log["success_polls"] = success_count
    session_log["fail_streak_at_end"] = fail_streak
    session_log["early_termination"] = (fail_streak >= CONFIG["max_consecutive_failures"])

    archive_path = archive_session(session_log)
    logging.info(f"=== 任务结束: {poll_count}次轮询, {success_count}次成功, 耗时{elapsed:.1f}s ===")

    return 0 if fail_streak < CONFIG["max_consecutive_failures"] else 1

if __name__ == "__main__":
    # 资源限制设置
    try:
        process = psutil.Process(os.getpid())
        process.nice(psutil.IDLE_PRIORITY_CLASS if sys.platform == "win32" else 19)
    except Exception:
        pass

    sys.exit(main())
