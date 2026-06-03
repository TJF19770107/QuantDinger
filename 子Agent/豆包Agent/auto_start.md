# auto_start.py

> 原始文件: `auto_start.py`  |  类型: `.py`  |  自动转换

```python
"""
auto_start.py - 豆包Agent一键启动脚本
版本: v6.0 (R06)
"""

import sys
import json
import time
import logging
from pathlib import Path

ROOT_DIR = Path(r"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent")
sys.path.insert(0, str(ROOT_DIR))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("AutoStart")

def main():
    logger.info("=" * 50)
    logger.info("豆包Agent v6.0 启动中...")
    start_time = time.time()

    results = {
        "startup_time": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "modules": {},
    }

    # T+0: AutoWake 启动
    try:
        from 技能库.AutoWake.code.auto_wake import AutoWake
        aw = AutoWake()
        wake_result = aw.trigger(reason="auto_start")
        results["modules"]["AutoWake"] = wake_result
        logger.info(f"AutoWake: wake_count={wake_result['wake_count']}")
    except Exception as e:
        logger.error(f"AutoWake 启动失败: {e}")
        results["modules"]["AutoWake"] = {"error": str(e)}

    # T+1: MemoryOS 初始化
    try:
        from 技能库.MemoryOS.code.memory_os import MemoryOS
        mos = MemoryOS()
        memory_stats = mos.auto_load()
        results["modules"]["MemoryOS"] = memory_stats
        logger.info(f"MemoryOS: long_term={memory_stats.get('long_term_loaded', 0)}")
    except Exception as e:
        logger.error(f"MemoryOS 启动失败: {e}")
        results["modules"]["MemoryOS"] = {"error": str(e)}

    # T+2: AutoFileScanner 扫描
    try:
        from 技能库.AutoFileScanner.code.auto_file_scanner import AutoFileScanner
        scanner = AutoFileScanner()
        scan_result = scanner.build_tree()
        results["modules"]["AutoFileScanner"] = {
            "total": scan_result.total_files,
            "new": scan_result.new_files,
            "deleted": scan_result.deleted_files,
        }
        logger.info(f"AutoFileScanner: {scan_result.total_files} files")
    except Exception as e:
        logger.error(f"AutoFileScanner 启动失败: {e}")
        results["modules"]["AutoFileScanner"] = {"error": str(e)}

    # T+3: SafeGuard 检查点
    try:
        from 技能库.SafeGuard.code.safe_guard import SafeGuard
        sg = SafeGuard()
        cp = sg.create_checkpoint(label="auto_start")
        results["modules"]["SafeGuard"] = {
            "checkpoint_id": cp.checkpoint_id,
            "files_hashed": len(cp.snapshot),
        }
        logger.info(f"SafeGuard: checkpoint={cp.checkpoint_id}")
    except Exception as e:
        logger.error(f"SafeGuard 启动失败: {e}")
        results["modules"]["SafeGuard"] = {"error": str(e)}

    duration = time.time() - start_time
    results["duration"] = f"{duration:.1f}s"
    logger.info(f"启动完成 ({duration:.1f}s)")

    # 输出摘要
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results

if __name__ == "__main__":
    main()

```
