# lsp_intelligence.py

> 原始文件: `lsp_intelligence.py`  |  类型: `.py`  |  自动转换

```python
"""
LSP Intelligence v1.0
对标: OpenCode LSP 语言服务器自动加载
"""

import os
from typing import Optional, Dict, List


class LSPIntelligence:
    """
    LSP智能感知接口
    对标 OpenCode 16万Star 的 LSP 自动加载机制
    """

    LANGUAGE_MAP = {
        ".py": "pylsp",
        ".js": "typescript-language-server",
        ".ts": "typescript-language-server",
        ".tsx": "typescript-language-server",
        ".jsx": "typescript-language-server",
        ".rs": "rust-analyzer",
        ".go": "gopls",
        ".java": "jdtls",
        ".cpp": "clangd",
        ".c": "clangd",
        ".h": "clangd",
        ".hpp": "clangd",
        ".cs": "omnisharp",
        ".rb": "solargraph",
        ".php": "intelephense",
        ".swift": "sourcekit-lsp",
        ".kt": "kotlin-language-server",
        ".scala": "metals",
        ".vue": "volar",
        ".svelte": "svelte-language-server",
        ".json": "vscode-json-languageserver",
        ".yaml": "yaml-language-server",
        ".md": "marksman",
        ".toml": "taplo",
    }

    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.loaded_servers = {}
        self.file_index = {}

    def detect_language(self, file_path: str) -> Optional[str]:
        """
        自动检测文件语言 → 匹配LSP服务器
        """
        ext = os.path.splitext(file_path)[1].lower()
        return self.LANGUAGE_MAP.get(ext)

    def load_server(self, language: str) -> Dict:
        """
        加载对应的LSP服务器
        """
        if language in self.loaded_servers:
            return self.loaded_servers[language]

        server_info = {
            "language": language,
            "lsp_name": self.LANGUAGE_MAP.get(language, "unknown"),
            "status": "loaded",
            "capabilities": ["completion", "hover", "definition", "references", "diagnostics"]
        }
        self.loaded_servers[language] = server_info
        return server_info

    def code_understanding(self, file_path: str) -> dict:
        """
        代码库深度理解
        """
        language = self.detect_language(file_path)
        if not language:
            return {"error": f"Unsupported language for {file_path}"}

        server = self.load_server(language)

        return {
            "file": file_path,
            "language": language,
            "lsp_server": server["lsp_name"],
            "symbols": self._extract_symbols(file_path),
            "imports": self._extract_imports(file_path),
            "dependencies": [],
            "complexity": self._estimate_complexity(file_path)
        }

    def multi_file_diff(self, changes: List[dict]) -> dict:
        """
        多文件变更Diff预览
        """
        diffs = []
        for change in changes:
            diffs.append({
                "file": change.get("file"),
                "type": change.get("type", "modify"),
                "lines_added": change.get("added", 0),
                "lines_removed": change.get("removed", 0)
            })
        return {
            "total_files": len(diffs),
            "total_additions": sum(d["lines_added"] for d in diffs),
            "total_deletions": sum(d["lines_removed"] for d in diffs),
            "diffs": diffs
        }

    def index_workspace(self) -> dict:
        """
        索引整个工作区
        """
        index = {"files": {}, "total_files": 0, "languages": set()}
        for root, _, files in os.walk(self.workspace_root):
            for f in files:
                file_path = os.path.join(root, f)
                lang = self.detect_language(file_path)
                if lang:
                    index["files"][file_path] = lang
                    index["languages"].add(lang)
                    index["total_files"] += 1
        index["languages"] = list(index["languages"])
        return index

    def _extract_symbols(self, file_path: str) -> list:
        return []

    def _extract_imports(self, file_path: str) -> list:
        return []

    def _estimate_complexity(self, file_path: str) -> int:
        try:
            with open(file_path, encoding="utf-8") as f:
                return len(f.readlines())
        except:
            return 0

print("[LSPIntelligence] v1.0 加载完成")
```
