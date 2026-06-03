# obsidian_mcp_bridge.py

> 原始文件: `obsidian_mcp_bridge.py`  |  类型: `.py`  |  自动转换

```python
"""
Obsidian MCP Bridge v1.0
对标: Obsidian ←→ MCP ←→ AI Agent 知识库联动
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, List


class ObsidianMCPBridge:
    """
    Obsidian知识库 MCP 桥接
    技术栈: 网页 → Markdown → Obsidian → MCP → AI Agent
    """

    def __init__(self, vault_path: str = None, memory_os=None):
        self.vault_path = vault_path
        self.memory_os = memory_os
        self.sync_status = {}
        self.markdown_index = {}

    def connect_vault(self, vault_path: str) -> dict:
        """
        连接Obsidian知识库
        """
        self.vault_path = vault_path
        stats = self._scan_vault()
        return {
            "vault_path": vault_path,
            "status": "connected",
            "total_notes": stats["total_notes"],
            "total_folders": stats["total_folders"],
            "file_types": stats["file_types"]
        }

    def _scan_vault(self) -> dict:
        """
        扫描知识库统计
        """
        if not self.vault_path or not os.path.exists(self.vault_path):
            return {"total_notes": 0, "total_folders": 0, "file_types": {}}

        total_notes = 0
        total_folders = 0
        file_types = {}

        for root, dirs, files in os.walk(self.vault_path):
            total_folders += len(dirs)
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext == ".md":
                    total_notes += 1
                file_types[ext] = file_types.get(ext, 0) + 1

        return {
            "total_notes": total_notes,
            "total_folders": total_folders,
            "file_types": file_types
        }

    def sync_vault(self) -> dict:
        """
        双向同步 Obsidian ↔ MemoryOS
        """
        if not self.vault_path:
            return {"error": "Vault not connected"}

        synced = []
        for root, _, files in os.walk(self.vault_path):
            for f in files:
                if f.endswith(".md"):
                    file_path = os.path.join(root, f)
                    note_id = f.replace(".md", "")
                    content = self._read_note(file_path)

                    if self.memory_os:
                        self.memory_os.upsert(
                            note_id=note_id,
                            content=content,
                            source="obsidian",
                            path=file_path
                        )

                    synced.append({
                        "id": note_id,
                        "path": file_path,
                        "size": len(content)
                    })

        self.sync_status["last_sync"] = datetime.now().isoformat()
        self.sync_status["synced_count"] = len(synced)
        return self.sync_status

    def markdown_index_build(self) -> dict:
        """
        构建Markdown语义索引
        """
        if not self.vault_path:
            return {"error": "Vault not connected"}

        index = {}
        for root, _, files in os.walk(self.vault_path):
            for f in files:
                if f.endswith(".md"):
                    file_path = os.path.join(root, f)
                    content = self._read_note(file_path)
                    title = self._extract_title(content)
                    tags = self._extract_tags(content)
                    links = self._extract_links(content)

                    index[file_path] = {
                        "title": title,
                        "tags": tags,
                        "links": links,
                        "word_count": len(content.split())
                    }

        self.markdown_index = index
        return {
            "indexed_files": len(index),
            "total_tags": sum(len(v["tags"]) for v in index.values()),
            "total_links": sum(len(v["links"]) for v in index.values())
        }

    def cross_reference(self, query: str, top_k: int = 10) -> List[dict]:
        """
        跨笔记交叉引用检索
        """
        if not self.markdown_index:
            self.markdown_index_build()

        results = []
        for file_path, meta in self.markdown_index.items():
            if query.lower() in meta.get("title", "").lower():
                results.append({"file": file_path, "match_type": "title", "meta": meta})
            elif query.lower() in ",".join(meta.get("tags", [])).lower():
                results.append({"file": file_path, "match_type": "tag", "meta": meta})

        return results[:top_k]

    def export_to_obsidian(self, note_id: str, content: str, tags: list = None) -> str:
        """
        MemoryOS → Obsidian 导出笔记
        """
        if not self.vault_path:
            return ""

        file_name = f"{note_id}.md"
        file_path = os.path.join(self.vault_path, file_name)

        tag_str = "\n".join([f"#{t}" for t in (tags or [])])
        full_content = f"""---
title: {note_id}
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [{", ".join(tags or [])}]
---

{tag_str}

{content}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        return file_path

    def _read_note(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return ""

    def _extract_title(self, content: str) -> str:
        for line in content.split("\n"):
            if line.startswith("# "):
                return line.replace("# ", "").strip()
        return "Untitled"

    def _extract_tags(self, content: str) -> list:
        tags = []
        for line in content.split("\n"):
            if line.startswith("tags:"):
                tags.extend([t.strip() for t in line.replace("tags:", "").strip("[]").split(",")])
        for word in content.split():
            if word.startswith("#") and len(word) > 1:
                tags.append(word[1:])
        return list(set(tags))

    def _extract_links(self, content: str) -> list:
        import re
        return re.findall(r'\[\[(.*?)\]\]', content)


print("[ObsidianMCPBridge] v1.0 加载完成")
```
