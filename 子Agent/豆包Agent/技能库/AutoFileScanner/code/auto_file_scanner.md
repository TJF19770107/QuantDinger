# auto_file_scanner.py

原始格式: Python

```python
"""
AutoFileScanner v2.0 - 自动文件扫描与索引引擎
路径: 豆包Agent/技能库/AutoFileScanner/code/auto_file_scanner.py
对标: Karpathy autoresearch + OpenClaw File Gateway
"""

import json
import hashlib
import logging
import threading
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum

logger = logging.getLogger("AutoFileScanner")

class FileCategory(Enum):
    DOCUMENT = "document"     # .md .txt .pdf .docx
    CODE = "code"             # .py .js .json .yaml
    IMAGE = "image"           # .png .jpg .svg
    DATA = "data"             # .csv .db .sqlite
    ARCHIVE = "archive"       # .zip .tar
    UNKNOWN = "unknown"

@dataclass
class FileEntry:
    """文件索引条目"""
    path: str
    rel_path: str
    category: FileCategory
    size: int
    md5: str
    mtime: float
    extension: str
    tags: List[str] = field(default_factory=list)

@dataclass
class ScanResult:
    """扫描结果"""
    scan_time: str
    total_files: int
    new_files: int
    modified_files: int
    deleted_files: int
    entries: List[FileEntry] = field(default_factory=list)

class FileIndex:
    """文件索引数据库"""

    CATEGORY_MAP = {
        '.md': FileCategory.DOCUMENT, '.txt': FileCategory.DOCUMENT,
        '.pdf': FileCategory.DOCUMENT, '.docx': FileCategory.DOCUMENT,
        '.py': FileCategory.CODE, '.js': FileCategory.CODE,
        '.json': FileCategory.CODE, '.yaml': FileCategory.CODE,
        '.yml': FileCategory.CODE, '.toml': FileCategory.CODE,
        '.png': FileCategory.IMAGE, '.jpg': FileCategory.IMAGE,
        '.jpeg': FileCategory.IMAGE, '.svg': FileCategory.IMAGE,
        '.gif': FileCategory.IMAGE, '.webp': FileCategory.IMAGE,
        '.csv': FileCategory.DATA, '.db': FileCategory.DATA,
        '.sqlite': FileCategory.DATA, '.sqlite3': FileCategory.DATA,
        '.zip': FileCategory.ARCHIVE, '.tar': FileCategory.ARCHIVE,
        '.gz': FileCategory.ARCHIVE, '.7z': FileCategory.ARCHIVE,
    }

    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.entries: Dict[str, FileEntry] = {}
        self._load()

    def add(self, entry: FileEntry):
        self.entries[entry.rel_path] = entry

    def remove(self, rel_path: str):
        self.entries.pop(rel_path, None)

    def get(self, rel_path: str) -> Optional[FileEntry]:
        return self.entries.get(rel_path)

    def query_by_category(self, category: FileCategory) -> List[FileEntry]:
        return [e for e in self.entries.values() if e.category == category]

    def query_by_tag(self, tag: str) -> List[FileEntry]:
        return [e for e in self.entries.values() if tag in e.tags]

    def query_by_extension(self, ext: str) -> List[FileEntry]:
        return [e for e in self.entries.values() if e.extension.lower() == ext.lower()]

    def count(self) -> Dict[str, int]:
        counts = {}
        for e in self.entries.values():
            cat = e.category.value
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    def _load(self):
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry_data in data.get("entries", []):
                    entry = FileEntry(**entry_data)
                    self.entries[entry.rel_path] = entry

    def save(self):
        data = {
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "total": len(self.entries),
            "entries": [e.__dict__ for e in self.entries.values()],
        }
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

class Watchdog:
    """文件变化监控器"""

    def __init__(self, index: FileIndex, scan_dirs: List[Path]):
        self.index = index
        self.scan_dirs = scan_dirs
        self.running = False
        self._thread = None

    def start(self):
        """启动后台监控"""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        logger.info("Watchdog 已启动")

    def stop(self):
        """停止监控"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _watch_loop(self):
        """监控循环（每30秒扫描一次增量变化）"""
        previous_mtimes: Dict[str, float] = {}
        while self.running:
            time.sleep(30)
            current_mtimes = {}
            for scan_dir in self.scan_dirs:
                if not scan_dir.exists():
                    continue
                for fp in scan_dir.rglob("*"):
                    if fp.is_file() and ".git" not in str(fp):
                        current_mtimes[str(fp)] = fp.stat().st_mtime

            # 检测变化
            for path_str, mtime in current_mtimes.items():
                if path_str not in previous_mtimes:
                    logger.debug(f"新文件: {path_str}")
                elif mtime != previous_mtimes[path_str]:
                    logger.debug(f"文件修改: {path_str}")

            for path_str in previous_mtimes:
                if path_str not in current_mtimes:
                    logger.debug(f"文件删除: {path_str}")

            previous_mtimes = current_mtimes
            # TODO: R07 触发增量索引更新

class AutoFileScanner:
    """自动文件扫描引擎主类"""

    ROOT_DIR = Path(r"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent")
    INDEX_PATH = ROOT_DIR / "file_index.json"

    def __init__(self):
        self.index = FileIndex(self.INDEX_PATH)
        self.watchdog = None
        self.scan_count = 0

    def build_tree(self, scan_dirs: List[Path] = None) -> ScanResult:
        """全量扫描构建文件树"""
        self.scan_count += 1
        if scan_dirs is None:
            scan_dirs = [self.ROOT_DIR]

        prev_count = len(self.index.entries)
        current_files: Set[str] = set()

        new_count = 0
        modified_count = 0

        for scan_dir in scan_dirs:
            if not scan_dir.exists():
                continue
            for fp in scan_dir.rglob("*"):
                if fp.is_file() and ".git" not in str(fp):
                    rel = str(fp.relative_to(scan_dir))
                    current_files.add(rel)
                    entry = self._create_entry(fp, rel, scan_dir)

                    existing = self.index.get(rel)
                    if not existing:
                        self.index.add(entry)
                        new_count += 1
                    elif existing.md5 != entry.md5:
                        self.index.add(entry)
                        modified_count += 1

        # 检测删除
        deleted_count = sum(
            1 for rel in self.index.entries
            if rel not in current_files
        )
        for rel in list(self.index.entries.keys()):
            if rel not in current_files:
                self.index.remove(rel)

        self.index.save()

        result = ScanResult(
            scan_time=time.strftime("%Y-%m-%dT%H:%M:%S"),
            total_files=len(self.index.entries),
            new_files=new_count,
            modified_files=modified_count,
            deleted_files=deleted_count,
        )
        return result

    def start_watchdog(self):
        """启动文件变化监控"""
        self.watchdog = Watchdog(self.index, [self.ROOT_DIR])
        self.watchdog.start()

    def bridge_to_memory(self, memory_os) -> dict:
        """与MemoryOS的索引桥接：将文件索引注入记忆系统"""
        summary = {
            "total_files": len(self.index.entries),
            "categories": self.index.count(),
            "recent_scans": self.scan_count,
        }
        # TODO: R07 调用 MemoryOS.write()
        return summary

    def _create_entry(self, fp: Path, rel_path: str, base: Path) -> FileEntry:
        """创建文件索引条目"""
        ext = fp.suffix.lower()
        category = self.index.CATEGORY_MAP.get(ext, FileCategory.UNKNOWN)
        try:
            md5 = hashlib.md5(fp.read_bytes()).hexdigest()
        except Exception:
            md5 = "ERROR"

        return FileEntry(
            path=str(fp),
            rel_path=rel_path,
            category=category,
            size=fp.stat().st_size,
            md5=md5,
            mtime=fp.stat().st_mtime,
            extension=ext,
        )

# 模块入口
if __name__ == "__main__":
    scanner = AutoFileScanner()
    result = scanner.build_tree()
    print(json.dumps({
        "total": result.total_files,
        "new": result.new_files,
        "modified": result.modified_files,
        "deleted": result.deleted_files,
    }, ensure_ascii=False))

```
