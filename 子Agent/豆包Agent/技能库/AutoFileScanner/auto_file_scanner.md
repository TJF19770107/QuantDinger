# auto_file_scanner.py

> 原始文件: `auto_file_scanner.py`  |  类型: `.py`  |  自动转换

```python
# auto_file_scanner.py - 豆包Agent自主文件扫描器
# 版本：v1.0 | 自动生成：R06 | 来源：R05设计
"""自主扫描豆包Agent目录，构建索引，智能分类，自动注册能力清单。"""
import os, json, time, hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class AutoFileScanner:
    """自主文件扫描引擎 —— 启动时自动构建文件树索引并注册能力"""

    def __init__(self, root_dir: str):
        self.root = Path(root_dir)
        self.index_path = self.root / "file_index.json"
        self.caps_path = self.root / "capabilities.json"
        self.file_tree: Dict = {}
        self.categories = {
            "architecture": ["架构", "architecture"],
            "iteration": ["迭代", "iteration"],
            "capability": ["能力", "对标", "capability"],
            "memory": ["memory", "记忆"],
            "skill": ["技能", "skill"],
        }

    def build_tree(self) -> Dict:
        """构建完整目录树索引"""
        self.file_tree = {"scan_time": datetime.now().isoformat(), "files": {}, "categories_count": {}}
        for path in self.root.rglob("*"):
            if path.is_file() and not any(x in path.parts for x in [".git", "__pycache__", "checkpoints"]):
                rel = str(path.relative_to(self.root))
                self.file_tree["files"][rel] = {
                    "size": path.stat().st_size,
                    "mtime": path.stat().st_mtime,
                    "type": path.suffix,
                    "category": self._classify(rel),
                    "md5": self._hash_file(path)
                }
        self._count_categories()
        self._save_index()
        return self.file_tree

    def _classify(self, rel_path: str) -> str:
        for cat, keywords in self.categories.items():
            for kw in keywords:
                if kw in rel_path.lower():
                    return cat
        return "other"

    def _count_categories(self):
        counts = {}
        for f in self.file_tree["files"].values():
            counts[f["category"]] = counts.get(f["category"], 0) + 1
        self.file_tree["categories_count"] = counts

    def _hash_file(self, path: Path) -> str:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def _save_index(self):
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.file_tree, f, ensure_ascii=False, indent=2)

    def extract_capabilities(self) -> List[str]:
        """从md文件中提取能力标签"""
        caps = set()
        for md_path in self.root.rglob("*.md"):
            try:
                content = md_path.read_text(encoding="utf-8")
                for line in content.split("\n"):
                    if "✅" in line and ("激活" in line or "完成" in line or "已设计" in line):
                        caps.add(line.strip())
            except Exception:
                pass
        return sorted(caps)[:50]

    def auto_register(self):
        """自动注册能力到capabilities.json"""
        caps = self.extract_capabilities()
        with open(self.caps_path, "w", encoding="utf-8") as f:
            json.dump({"registered": len(caps), "capabilities": caps, "updated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
        return caps

    def incremental_update(self, changed_files: List[str]):
        """增量更新——仅刷新变化的文件"""
        for f in changed_files:
            rel = str(Path(f).relative_to(self.root)) if self.root in Path(f).parents else f
            path = self.root / rel
            if path.exists():
                self.file_tree["files"][rel] = {
                    "size": path.stat().st_size,
                    "mtime": path.stat().st_mtime,
                    "type": path.suffix,
                    "category": self._classify(rel),
                    "md5": self._hash_file(path)
                }
            else:
                self.file_tree["files"].pop(rel, None)
        self._count_categories()
        self._save_index()

if __name__ == "__main__":
    scanner = AutoFileScanner(str(ROOT))
    scanner.build_tree()
    caps = scanner.auto_register()
    print(f"扫描完成：{len(scanner.file_tree['files'])} 文件, {len(caps)} 能力已注册")

```
