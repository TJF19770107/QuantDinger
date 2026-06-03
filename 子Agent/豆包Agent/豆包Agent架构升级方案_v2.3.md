# 豆包Agent架构升级方案 v2.3

> **版本**：v2.3  
> **日期**：2026-05-31  
> **对标系统**：Codex CLI / Claude Agent SDK / Hermes / OpenClaw / Gemini 2.5 / Marvis Workbody / OpenCode / AI IDE趋势  
> **方法论**：龙虾五步法（情报采集→架构升级→能力迭代→缺口分析→可执行代码产出）  

---

## 目录

1. [架构全景](#一架构全景)
2. [思考架构层](#二思考架构层-think)
3. [编码能力层](#三编码能力层-exec)
4. [自主规划层](#四自主规划层-plan)
5. [工具调用层](#五工具调用层-tool)
6. [本地执行层](#六本地执行层-infra)
7. [自进化闭环层](#七自进化闭环层-evol)
8. [AI IDE完整功能](#八ai-ide完整功能)
9. [数据流与交互协议](#九数据流与交互协议)
10. [部署与运维](#十部署与运维)

---

## 一、架构全景

### 1.1 六层架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    自进化闭环层 (EVOL)                         │
│   Act → Observe → Reflect → Update                          │
│   对标: 自进化闭环理论 + 中文社区记忆增强实践                      │
└─────────────────────────────────────────────────────────────┘
                              ↕ 监控 & 更新
┌─────────────────────────────────────────────────────────────┐
│                    思考架构层 (THINK)                          │
│   Central Orchestrator | CoT Engine | Agent Graph            │
│   Memory Bank | Context Manager (512K+) | Model Voting      │
│   对标: Claude Agent SDK + Gemini 2.5 + Codex CLI            │
└─────────────────────────────────────────────────────────────┘
                              ↕ 任务分派 & 上下文
┌─────────────────────────────────────────────────────────────┐
│                    自主规划层 (PLAN)                           │
│   ReAct Loop | Reflexion | Plan-Execute                     │
│   Checkpoint & Rollback | Hierarchical Agent                │
│   对标: Codex CLI (ReAct/Reflexion/Checkpoint)              │
└─────────────────────────────────────────────────────────────┘
                              ↕ 执行指令
┌─────────────────────────────────────────────────────────────┐
│                    编码能力层 (EXEC)                           │
│   Code Engine | Multi-Agent Coding | Autonomous PR          │
│   Agentic IDE | Repo-aware | Git Agent | Shell Sandbox      │
│   文件操作 | 文档处理 | 多模态引擎                             │
│   对标: Codex CLI + OpenCode + AI IDE趋势 + Marvis Workbody  │
└─────────────────────────────────────────────────────────────┘
                              ↕ 工具调用
┌─────────────────────────────────────────────────────────────┐
│                    工具调用层 (TOOL)                           │
│   Tool Registry | Agent Gateway | Message Bus (MOM)         │
│   Dynamic Composer | Agent注册中心 | Plugin Manager         │
│   对标: Hermes + OpenClaw + 中文社区多Agent协同               │
└─────────────────────────────────────────────────────────────┘
                              ↕ 基础设施
┌─────────────────────────────────────────────────────────────┐
│                    本地执行层 (INFRA)                          │
│   Ollama/LM Studio | 向量数据库 | 移动端推理(MNN/ncnn/TFLite) │
│   安全沙箱 | Docker | 端云协同桥接 | 部署方案                  │
│   对标: Ollama + Local Vector DB + Marvis Workbody          │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 对标映射矩阵

| 架构层 | 对标系统 | 核心能力导入 | 差异化策略 |
|--------|----------|-------------|-----------|
| THINK | Claude Agent SDK + Gemini 2.5 | Orchestrator, Agent Graph, Memory Bank, CoT, 1M Context | 融合多模型中枢 + 移动端推理优化 |
| PLAN | Codex CLI | ReAct, Reflexion, Plan-Execute, Checkpoint | 增加中文场景特化反思 |
| EXEC | Codex + OpenCode + Marvis Workbody | 编码引擎, Shell沙箱, 文件操作 | 端云协同执行 + 手机端交互优化 |
| TOOL | Hermes + OpenClaw | Tool Registry, Agent Gateway, MOM | 轻量化移动端适配 |
| INFRA | Ollama + LM Studio + Local Vector DB | 本地模型, 向量检索, 移动推理 | 端云协同 + 国产硬件加速适配 |
| EVOL | 自进化闭环理论 + 中文社区 | Observe→Reflect→Update, 反馈学习 | 隐私优先的本地进化 |

---

## 二、思考架构层 (THINK)

### 2.1 Central Orchestrator（对标 Claude Agent SDK）

**核心设计**：

```
                    ┌─────────────────┐
                    │  Central         │
     请求 ─────────→│  Orchestrator    │─────────→ 响应
                    │                  │
                    │  ┌────────────┐  │
                    │  │Agent Graph │  │
                    │  │  引擎      │  │
                    │  └────────────┘  │
                    │  ┌────────────┐  │
                    │  │CoT 推理链  │  │
                    │  │  引擎      │  │
                    │  └────────────┘  │
                    │  ┌────────────┐  │
                    │  │Model Voting│  │
                    │  │  决策器    │  │
                    │  └────────────┘  │
                    │  ┌────────────┐  │
                    │  │Context     │  │
                    │  │ Manager    │  │
                    │  └────────────┘  │
                    │  ┌────────────┐  │
                    │  │Memory Bank │  │
                    │  └────────────┘  │
                    └─────────────────┘
```

**关键模块**：

| 模块 | 对标 | 技术方案 | 接口 |
|------|------|----------|------|
| Orchestrator | Claude Agent SDK | 事件驱动 + 优先级队列 + 超时熔断 | `orchestrate(task: Task) -> Plan` |
| Agent Graph | Claude Agent SDK | DAG执行引擎，支持并行/串行/条件分支 | `execute_graph(nodes: List[AgentNode]) -> Result` |
| CoT Engine | Gemini 2.5 | 显式推理链 + Long-Context Cache | `chain_of_thought(prompt, context) -> Reasoning` |
| Model Voting | Hermes | 多模型并行推理 + 置信度加权投票 | `vote(prompt, models[]) -> Decision` |
| Context Manager | Codex CLI + Gemini 2.5 | 512K+ token + 智能剪枝 + 热/温/冷三级缓存 | `manage_context(input) -> OptimizedContext` |
| Memory Bank | Claude Agent SDK | 语义检索 + 增量更新 + 分级存储 | `store(key, value) / retrieve(query) -> Memory` |

### 2.2 Agent Graph 执行引擎（代码模板）

```python
# src/think/agent_graph.py
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Callable
import asyncio

class NodeType(Enum):
    SEQUENTIAL = "sequential"      # 串行执行
    PARALLEL = "parallel"          # 并行执行
    CONDITIONAL = "conditional"    # 条件分支
    LOOP = "loop"                  # 循环节点

@dataclass
class AgentNode:
    node_id: str
    node_type: NodeType
    agent_fn: Callable
    dependencies: List[str]        # 前置节点ID列表
    condition: Optional[Callable] = None
    max_retries: int = 0
    timeout_seconds: int = 30

@dataclass
class GraphResult:
    node_id: str
    output: dict
    success: bool
    duration_ms: float

class AgentGraphEngine:
    """对标 Claude Agent SDK 的 Agent Graph 执行引擎"""
    
    def __init__(self):
        self.nodes: Dict[str, AgentNode] = {}
    
    def add_node(self, node: AgentNode):
        self.nodes[node.node_id] = node
    
    async def execute(self, context: dict) -> Dict[str, GraphResult]:
        """DAG拓扑排序 + 并行执行"""
        results = {}
        executed = set()
        
        while len(executed) < len(self.nodes):
            # 找到所有依赖已满足的节点
            ready = [
                node for node in self.nodes.values()
                if node.node_id not in executed
                and all(dep in executed for dep in node.dependencies)
            ]
            
            if not ready:
                raise RuntimeError("Graph deadlock detected")
            
            # 并行节点并发执行
            parallel_nodes = [n for n in ready if n.node_type == NodeType.PARALLEL]
            sequential_nodes = [n for n in ready if n.node_type != NodeType.PARALLEL]
            
            if parallel_nodes:
                tasks = [self._execute_node(n, context, results) for n in parallel_nodes]
                parallel_results = await asyncio.gather(*tasks, return_exceptions=True)
                for node, result in zip(parallel_nodes, parallel_results):
                    if isinstance(result, Exception):
                        results[node.node_id] = GraphResult(
                            node_id=node.node_id,
                            output={"error": str(result)},
                            success=False,
                            duration_ms=0
                        )
                    else:
                        results[node.node_id] = result
                    executed.add(node.node_id)
            
            for node in sequential_nodes:
                result = await self._execute_node(node, context, results)
                results[node.node_id] = result
                executed.add(node.node_id)
        
        return results
    
    async def _execute_node(
        self, node: AgentNode, context: dict, prev_results: dict
    ) -> GraphResult:
        import time
        start = time.time()
        try:
            output = await asyncio.wait_for(
                node.agent_fn(context, prev_results),
                timeout=node.timeout_seconds
            )
            return GraphResult(
                node_id=node.node_id,
                output=output,
                success=True,
                duration_ms=(time.time() - start) * 1000
            )
        except asyncio.TimeoutError:
            return GraphResult(node.node_id, {"error": "timeout"}, False, node.timeout_seconds * 1000)
```

### 2.3 CoT推理引擎（代码模板）

```python
# src/think/cot_engine.py
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class ReasoningStep:
    step_id: int
    thought: str              # 当前思考
    action: Optional[str]     # 计划执行的动作
    observation: Optional[str] # 执行后的观察
    confidence: float          # 置信度 0-1

@dataclass
class CoTResult:
    steps: List[ReasoningStep]
    final_answer: str
    total_confidence: float

class CoTEngine:
    """对标 Gemini 2.5 内置 Chain-of-Thought"""
    
    def __init__(self, model_adapter, cache_manager):
        self.model = model_adapter
        self.cache = cache_manager
    
    async def reason(
        self, 
        prompt: str, 
        context: dict,
        max_steps: int = 10,
        min_confidence: float = 0.7
    ) -> CoTResult:
        """
        显式推理链：Think → Act → Observe → Think → ... → Answer
        """
        steps = []
        current_context = context.copy()
        
        for i in range(max_steps):
            # 查找缓存
            cache_key = f"cot:{hash(prompt)}:{i}"
            cached = self.cache.get(cache_key)
            if cached:
                steps.append(cached)
                continue
            
            # Think
            thought_prompt = self._build_thought_prompt(prompt, steps, current_context)
            thought = await self.model.generate(thought_prompt)
            
            # Decide: 是否得出最终答案
            if self._is_final_answer(thought):
                return CoTResult(
                    steps=steps,
                    final_answer=thought.get("answer", thought.get("thought", "")),
                    total_confidence=self._calc_confidence(steps)
                )
            
            # Act: 确定下一步动作
            action = thought.get("action")
            if action:
                observation = await self._execute_action(action, current_context)
            else:
                observation = None
            
            step = ReasoningStep(
                step_id=i + 1,
                thought=thought.get("thought", ""),
                action=action,
                observation=observation,
                confidence=thought.get("confidence", 0.5)
            )
            steps.append(step)
            self.cache.set(cache_key, step)
            
            if observation:
                current_context["last_observation"] = observation
        
        return CoTResult(steps=steps, final_answer="", total_confidence=0.0)
    
    def _build_thought_prompt(self, prompt, steps, context):
        history = "\n".join([
            f"Step {s.step_id}: Thought: {s.thought}\n"
            f"Action: {s.action}\nObservation: {s.observation}"
            for s in steps
        ])
        return f"""Problem: {prompt}

Previous reasoning:
{history}

Current context: {context}

Think step by step. Output JSON: {{"thought": "...", "action": "...", "confidence": 0.0-1.0}}
If you have the final answer, output: {{"thought": "...", "answer": "...", "confidence": 1.0}}"""
    
    def _is_final_answer(self, thought: dict) -> bool:
        return "answer" in thought and thought.get("confidence", 0) >= 0.8
```

### 2.4 Context Manager（代码模板）

```python
# src/think/context_manager.py
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from collections import OrderedDict
import hashlib
import time

@dataclass
class ContextChunk:
    chunk_id: str
    content: str
    tokens: int
    priority: float       # 0-1, 越高越重要
    last_access: float    # Unix timestamp
    source: str           # 来源标识

class ContextManager:
    """
    对标 Codex CLI 512K context + Gemini 1M+ token
    三级缓存：Hot (内存) / Warm (本地DB) / Cold (磁盘)
    """
    
    MAX_HOT_TOKENS = 128000    # 热缓存：128K
    MAX_WARM_TOKENS = 512000   # 温缓存：512K
    MAX_COLD_TOKENS = 1048576  # 冷缓存：1M（Gemini级别）
    
    def __init__(self, warm_db_path: str, cold_disk_path: str):
        self.hot_cache: OrderedDict[str, ContextChunk] = OrderedDict()
        self.warm_db = WarmCacheDB(warm_db_path)
        self.cold_disk_path = cold_disk_path
        self._hot_tokens = 0
    
    def add(self, content: str, priority: float = 0.5, source: str = "unknown") -> str:
        """添加上下文，自动分级存储"""
        chunk_id = hashlib.sha256(f"{content}{time.time()}".encode()).hexdigest()[:16]
        tokens = self._estimate_tokens(content)
        chunk = ContextChunk(
            chunk_id=chunk_id,
            content=content,
            tokens=tokens,
            priority=priority,
            last_access=time.time(),
            source=source
        )
        
        if self._hot_tokens + tokens <= self.MAX_HOT_TOKENS:
            self.hot_cache[chunk_id] = chunk
            self._hot_tokens += tokens
        elif tokens <= self.MAX_WARM_TOKENS:
            self.warm_db.put(chunk)
        else:
            self._store_cold(chunk)
        
        self._evict_if_needed()
        return chunk_id
    
    def retrieve(self, query: str, top_k: int = 5) -> List[ContextChunk]:
        """语义检索 + 缓存层级穿透"""
        results = []
        
        # 1. 热缓存优先
        hot_results = self._search_hot(query, top_k)
        results.extend(hot_results)
        
        # 2. 温热缓存穿透
        if len(results) < top_k:
            warm_results = self.warm_db.search(query, top_k - len(results))
            results.extend(warm_results)
            # 提升到热缓存
            for chunk in warm_results:
                self._promote_to_hot(chunk)
        
        # 3. 冷缓存兜底
        if len(results) < top_k:
            cold_results = self._search_cold(query, top_k - len(results))
            results.extend(cold_results)
        
        return results
    
    def _evict_if_needed(self):
        """智能淘汰：优先级 + LRU 双重策略"""
        while self._hot_tokens > self.MAX_HOT_TOKENS:
            # 按 (priority * 0.7 + recency * 0.3) 排序，淘汰最低分
            chunks = list(self.hot_cache.values())
            chunks.sort(key=lambda c: c.priority * 0.7 + (time.time() - c.last_access) * 0.3)
            evicted = chunks[0]
            self.warm_db.put(evicted)
            del self.hot_cache[evicted.chunk_id]
            self._hot_tokens -= evicted.tokens
    
    def _estimate_tokens(self, text: str) -> int:
        """保守估计：中文 1.5字/token，英文 4字符/token"""
        import re
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        other_chars = len(text) - chinese_chars
        return int(chinese_chars / 1.5 + other_chars / 4)
```

---

## 三、编码能力层 (EXEC)

### 3.1 全栈编码引擎（对标 Codex CLI + OpenCode）

**核心架构**：

```
┌─────────────────────────────────────────────────────────┐
│                    全栈编码引擎                           │
│                                                         │
│  ┌───────────┐  ┌───────────┐  ┌───────────────────┐  │
│  │ Code      │  │ Debug     │  │ Test              │  │
│  │ Generator │  │ Engine    │  │ Generator         │  │
│  └─────┬─────┘  └─────┬─────┘  └────────┬──────────┘  │
│        │              │                 │              │
│        └──────────────┼─────────────────┘              │
│                       ▼                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Code Sandbox Manager                 │  │
│  │  Python | JS/TS | Shell | Go | Rust | SQL        │  │
│  └────────────────────┬─────────────────────────────┘  │
│                       ▼                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Multi-Agent Coding Coordinator         │  │
│  │  编码Agent | 审查Agent | 测试Agent | 文档Agent   │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**代码模板：编码引擎核心**

```python
# src/execute/code_engine.py
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import subprocess
import tempfile
import os

class Language(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    SHELL = "shell"
    GO = "go"
    RUST = "rust"
    SQL = "sql"

@dataclass
class CodeExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    language: Language

class CodeEngine:
    """
    对标 Codex CLI 编码引擎 + OpenCode 工具链
    支持多语言沙箱执行 + 代码审查 + 测试生成
    """
    
    LANG_CONFIG = {
        Language.PYTHON:  {"ext": ".py",  "cmd": ["python"],         "timeout": 30},
        Language.JAVASCRIPT: {"ext": ".js",  "cmd": ["node"],             "timeout": 30},
        Language.TYPESCRIPT: {"ext": ".ts",  "cmd": ["npx", "ts-node"],   "timeout": 30},
        Language.SHELL:     {"ext": ".sh",  "cmd": ["bash"],             "timeout": 10},
        Language.GO:        {"ext": ".go",  "cmd": ["go", "run"],        "timeout": 60},
        Language.RUST:      {"ext": ".rs",  "cmd": ["rustc", "-o"],      "timeout": 120},
        Language.SQL:       {"ext": ".sql", "cmd": ["sqlite3"],          "timeout": 15},
    }
    
    def __init__(self, sandbox_manager):
        self.sandbox = sandbox_manager
    
    async def generate_code(
        self, 
        spec: str, 
        language: Language,
        context: Optional[dict] = None
    ) -> str:
        """基于规格说明生成代码"""
        prompt = self._build_code_gen_prompt(spec, language, context)
        return await self._llm_generate(prompt)
    
    async def execute(
        self, 
        code: str, 
        language: Language,
        stdin: Optional[str] = None
    ) -> CodeExecutionResult:
        """沙箱执行代码"""
        config = self.LANG_CONFIG.get(language)
        if not config:
            raise ValueError(f"Unsupported language: {language}")
        
        with tempfile.NamedTemporaryFile(
            suffix=config["ext"], 
            mode="w", 
            delete=False
        ) as f:
            f.write(code)
            tmp_path = f.name
        
        try:
            start = __import__("time").time()
            result = subprocess.run(
                config["cmd"] + [tmp_path] if language != Language.RUST else config["cmd"] + [tmp_path],
                capture_output=True,
                text=True,
                timeout=config["timeout"],
                input=stdin
            )
            return CodeExecutionResult(
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                duration_ms=(__import__("time").time() - start) * 1000,
                language=language
            )
        except subprocess.TimeoutExpired:
            return CodeExecutionResult("", "Execution timed out", -1, config["timeout"] * 1000, language)
        finally:
            os.unlink(tmp_path)
    
    async def debug(
        self, 
        code: str, 
        error: str, 
        language: Language
    ) -> str:
        """基于错误信息调试代码"""
        prompt = f"""Code with error:
```{language.value}
{code}
```

Error:
{error}

Analyze the error and provide the corrected code."""
        return await self._llm_generate(prompt)
    
    async def refactor(
        self, 
        code: str, 
        language: Language, 
        instruction: str
    ) -> str:
        """按指令重构代码"""
        prompt = f"""Refactor this code: {instruction}

```{language.value}
{code}
```"""
        return await self._llm_generate(prompt)
```

### 3.2 Multi-Agent Coding（对标 AI IDE 趋势）

```python
# src/execute/multi_agent_coding.py
from dataclasses import dataclass
from typing import List, Dict
import asyncio

@dataclass
class CodingTask:
    task_id: str
    description: str
    language: str
    files_to_modify: List[str]
    priority: int  # 1-5

@dataclass
class CodeReview:
    file_path: str
    issues: List[Dict]  # [{line, severity, message, suggestion}]
    score: float  # 0-100

class MultiAgentCodingCoordinator:
    """
    对标 AI IDE Multi-Agent Coding：
    - 编码Agent：生成/修改代码
    - 审查Agent：Code Review + 安全扫描
    - 测试Agent：自动生成测试
    - 文档Agent：同步更新文档
    """
    
    def __init__(self, code_engine, tool_registry):
        self.code_engine = code_engine      # EXEC-CODE-001
        self.code_reviewer = CodeReviewer()  # EXEC-CODE-005
        self.test_generator = TestGenerator() # EXEC-CODE-006
        self.tool_registry = tool_registry
    
    async def execute_task(self, task: CodingTask) -> Dict:
        """四Agent协同执行编码任务"""
        results = {}
        
        # Phase 1: 编码Agent生成代码
        code_result = await self.code_engine.generate_code(
            spec=task.description,
            language=task.language
        )
        results["code"] = code_result
        
        # Phase 2: 审查Agent + 测试Agent并行
        review_task = self.code_reviewer.review(code_result, task.files_to_modify)
        test_task = self.test_generator.generate(code_result, task.language)
        
        review, tests = await asyncio.gather(review_task, test_task)
        results["review"] = review
        results["tests"] = tests
        
        # Phase 3: 如果审查不通过，自动修复
        if review.score < 70:
            fix_prompt = f"Fix the following issues:\n" + "\n".join(
                f"- Line {i['line']}: {i['message']}" 
                for issue in review.issues for i in [issue]
            )
            fixed_code = await self.code_engine.refactor(
                code_result, task.language, fix_prompt
            )
            results["fixed_code"] = fixed_code
        
        return results

class CodeReviewer:
    """代码审查Agent（EXEC-CODE-005）"""
    
    async def review(self, code: str, context_files: List[str]) -> CodeReview:
        issues = []
        
        # 安全检查
        security_issues = self._scan_security(code)
        issues.extend(security_issues)
        
        # 最佳实践检查
        best_practice_issues = self._check_best_practices(code)
        issues.extend(best_practice_issues)
        
        # 性能检查
        performance_issues = self._check_performance(code)
        issues.extend(performance_issues)
        
        score = max(0, 100 - len(issues) * 3)
        return CodeReview(
            file_path=context_files[0] if context_files else "generated_code",
            issues=issues,
            score=score
        )
    
    def _scan_security(self, code: str) -> List[dict]:
        """安全漏洞扫描"""
        patterns = {
            "exec(": ("CRITICAL", "Dynamic code execution detected, use subprocess instead"),
            "eval(": ("CRITICAL", "eval() is dangerous, avoid dynamic evaluation"),
            "os.system(": ("HIGH", "Use subprocess.run() instead of os.system()"),
            "shell=True": ("MEDIUM", "Avoid shell=True in subprocess"),
            r"password\s*=\s*[\"'][^\"']+[\"']": ("HIGH", "Hardcoded password detected"),
        }
        return [
            {"line": self._find_line(code, pattern), "severity": sev, "message": msg}
            for pattern, (sev, msg) in patterns.items()
            if pattern in code
        ]

class TestGenerator:
    """测试生成Agent（EXEC-CODE-006）"""
    
    async def generate(self, code: str, language: str) -> str:
        """自动生成单元测试"""
        prompt = f"""Generate comprehensive unit tests for the following code.
Include edge cases, error handling, and boundary testing.

```{language}
{code}
```

Generate tests using the standard testing framework for {language}."""
        return await self._llm_generate(prompt)
```

### 3.3 Shell执行沙箱（对标 Marvis Workbody）

```python
# src/execute/shell_sandbox.py
import subprocess
import os
import resource
from dataclasses import dataclass
from typing import Optional

@dataclass
class ShellResult:
    command: str
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    truncated: bool = False

class ShellSandbox:
    """
    对标 Marvis Workbody：Shell + Sandbox 隔离
    三层安全：进程隔离 + 文件系统限制 + 资源限制
    """
    
    # 允许的安全命令白名单
    ALLOWED_COMMANDS = {
        "ls", "dir", "cat", "echo", "head", "tail", "wc",
        "grep", "find", "sort", "uniq", "sed", "awk",
        "python", "node", "git", "docker", "curl", "wget",
        "mkdir", "touch", "cp", "mv", "rm",
    }
    
    # 禁止的敏感路径
    FORBIDDEN_PATHS = [
        "/etc/passwd", "/etc/shadow", "~/.ssh", "~/.aws",
        "C:\\Windows", "C:\\Windows\\System32"
    ]
    
    def __init__(self, workspace_dir: str, max_memory_mb: int = 512, timeout_seconds: int = 30):
        self.workspace = workspace_dir
        self.max_memory = max_memory_mb * 1024 * 1024
        self.timeout = timeout_seconds
    
    def execute(self, command: str, stdin: Optional[str] = None) -> ShellResult:
        """安全执行 Shell 命令"""
        import time
        
        # 安全检查
        cmd_name = command.split()[0] if command.split() else ""
        if cmd_name not in self.ALLOWED_COMMANDS:
            return ShellResult(command, "", f"Command '{cmd_name}' not in allowlist", -1, 0)
        
        if self._has_forbidden_path(command):
            return ShellResult(command, "", "Forbidden path detected", -1, 0)
        
        start = time.time()
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.workspace,
                preexec_fn=self._set_resource_limits if os.name != 'nt' else None
            )
            
            stdout = result.stdout[:10000]  # 截断超长输出
            truncated = len(result.stdout) > 10000
            
            return ShellResult(
                command=command,
                stdout=stdout,
                stderr=result.stderr[:5000],
                exit_code=result.returncode,
                duration_ms=(time.time() - start) * 1000,
                truncated=truncated
            )
        except subprocess.TimeoutExpired:
            return ShellResult(command, "", "Execution timed out", -1, self.timeout * 1000)
    
    def _has_forbidden_path(self, command: str) -> bool:
        return any(forbidden in command for forbidden in self.FORBIDDEN_PATHS)
    
    def _set_resource_limits(self):
        """Unix: 设置进程资源限制"""
        resource.setrlimit(resource.RLIMIT_AS, (self.max_memory, self.max_memory))
```

---

## 四、自主规划层 (PLAN)

### 4.1 ReAct 循环（对标 Codex CLI）

```
Think ──→ Act ──→ Observe ──→ Think ──→ Act ──→ ...
   ↑                            │
   └────────── Reflect ─────────┘
              (失败时)
```

```python
# src/plan/react_loop.py
from enum import Enum
from typing import List, Dict, Any, Optional

class ActionType(Enum):
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    EXECUTE_CODE = "execute_code"
    SEARCH = "search"
    ASK_USER = "ask_user"
    CALL_TOOL = "call_tool"

class ReActLoop:
    """
    对标 Codex CLI ReAct/Reflexion 循环
    Think → Act → Observe → Reflect → Retry or Complete
    """
    
    MAX_ITERATIONS = 20
    
    def __init__(self, orchestrator, tool_registry, memory_bank):
        self.orchestrator = orchestrator
        self.tools = tool_registry
        self.memory = memory_bank
    
    async def run(self, task: str, context: dict) -> dict:
        """执行 ReAct 循环"""
        history = []
        
        for i in range(self.MAX_ITERATIONS):
            # THINK: 分析当前状态，决定下一步
            thought = await self._think(task, history, context)
            
            if thought.get("is_final"):
                return {"status": "completed", "answer": thought["answer"], "history": history}
            
            # ACT: 执行具体动作
            action = thought["action"]
            observation = await self._act(action)
            
            # OBSERVE: 记录结果
            history.append({
                "step": i + 1,
                "thought": thought["reasoning"],
                "action": action,
                "observation": observation
            })
            
            # REFLECT（仅在失败时）
            if observation.get("error"):
                reflection = await self._reflect(history)
                if reflection.get("should_retry"):
                    thought["action"]["params"] = reflection["adjusted_params"]
                else:
                    return {"status": "failed", "error": observation["error"], "history": history}
        
        return {"status": "max_iterations", "history": history}
    
    async def _think(self, task, history, context):
        """推理下一步动作"""
        prompt = f"""Task: {task}
History: {history}
Context: {context}

Decide the next action. Output JSON:
{{"reasoning": "why this action", "action": {{"type": "ACTION_TYPE", "params": {{}}}}, "is_final": false}}
If task is complete: {{"reasoning": "...", "answer": "...", "is_final": true}}"""
        return await self.orchestrator.llm_generate(prompt)
```

### 4.2 Checkpoint & Rollback（对标 Codex CLI）

```python
# src/plan/checkpoint.py
import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class Checkpoint:
    checkpoint_id: str
    step: int
    timestamp: str
    state_snapshot: Dict           # 关键状态快照
    file_snapshots: Dict[str, str] # 文件路径 → 备份路径
    description: str

class CheckpointManager:
    """
    对标 Codex CLI Checkpoint & Rollback
    关键步骤自动存档，失败时可回滚至任意节点
    """
    
    def __init__(self, checkpoint_dir: str):
        self.checkpoint_dir = checkpoint_dir
        self.checkpoints: List[Checkpoint] = []
        os.makedirs(checkpoint_dir, exist_ok=True)
    
    def save(self, step: int, state: Dict, files_to_backup: List[str], desc: str) -> Checkpoint:
        """创建检查点"""
        import hashlib, shutil
        
        cid = hashlib.md5(f"{step}{datetime.now()}".encode()).hexdigest()[:12]
        
        # 备份文件
        file_snapshots = {}
        for fp in files_to_backup:
            if os.path.exists(fp):
                backup_path = os.path.join(self.checkpoint_dir, f"{cid}_{os.path.basename(fp)}")
                shutil.copy2(fp, backup_path)
                file_snapshots[fp] = backup_path
        
        cp = Checkpoint(
            checkpoint_id=cid,
            step=step,
            timestamp=datetime.now().isoformat(),
            state_snapshot=state,
            file_snapshots=file_snapshots,
            description=desc
        )
        
        self.checkpoints.append(cp)
        
        # 持久化
        with open(os.path.join(self.checkpoint_dir, f"{cid}.json"), "w") as f:
            json.dump(asdict(cp), f, indent=2, default=str)
        
        return cp
    
    def rollback(self, checkpoint_id: str) -> Dict:
        """回滚到指定检查点"""
        import shutil
        
        cp = next((c for c in self.checkpoints if c.checkpoint_id == checkpoint_id), None)
        if not cp:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")
        
        # 恢复文件
        for original_path, backup_path in cp.file_snapshots.items():
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, original_path)
        
        # 移除该检查点之后的所有检查点
        idx = next(i for i, c in enumerate(self.checkpoints) if c.checkpoint_id == checkpoint_id)
        self.checkpoints = self.checkpoints[:idx + 1]
        
        return cp.state_snapshot
    
    def list_checkpoints(self) -> List[Dict]:
        return [{"id": c.checkpoint_id, "step": c.step, "time": c.timestamp, "desc": c.description} for c in self.checkpoints]
```

---

## 五、工具调用层 (TOOL)

### 5.1 Tool Registry（对标 Hermes）

```python
# src/tool/tool_registry.py
from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass, field
import jsonschema
import json

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters_schema: Dict       # JSON Schema
    handler: Callable
    version: str = "1.0.0"
    tags: List[str] = field(default_factory=list)
    timeout_seconds: int = 30
    requires_auth: bool = False

class ToolRegistry:
    """
    对标 Hermes Tool Registry：
    工具注册、发现、参数校验、版本管理
    """
    
    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}
        self._aliases: Dict[str, str] = {}
    
    def register(self, tool: ToolDefinition) -> None:
        """注册工具 + JSON Schema 校验"""
        # 校验 Schema 合法性
        jsonschema.Draft7Validator.check_schema(tool.parameters_schema)
        
        if tool.name in self._tools:
            existing = self._tools[tool.name]
            if self._version_compare(tool.version, existing.version) <= 0:
                raise ValueError(f"Tool {tool.name} version {tool.version} <= existing {existing.version}")
        
        self._tools[tool.name] = tool
    
    def register_alias(self, alias: str, target: str) -> None:
        """注册工具别名"""
        if target not in self._tools:
            raise ValueError(f"Target tool {target} not found")
        self._aliases[alias] = target
    
    def resolve(self, name: str) -> ToolDefinition:
        """解析工具名（含别名）"""
        actual_name = self._aliases.get(name, name)
        if actual_name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._tools[actual_name]
    
    async def execute(self, name: str, params: dict) -> Any:
        """校验参数 + 执行工具"""
        tool = self.resolve(name)
        
        # JSON Schema 参数校验
        try:
            jsonschema.validate(params, tool.parameters_schema)
        except jsonschema.ValidationError as e:
            raise ValueError(f"Parameter validation failed for {name}: {e.message}")
        
        # 超时执行
        import asyncio
        return await asyncio.wait_for(
            tool.handler(**params) if callable(tool.handler) else tool.handler(params),
            timeout=tool.timeout_seconds
        )
    
    def list_tools(self, tag: Optional[str] = None) -> List[Dict]:
        """列出所有工具（可按 tag 过滤）"""
        tools = self._tools.values()
        if tag:
            tools = [t for t in tools if tag in t.tags]
        return [{
            "name": t.name,
            "description": t.description,
            "version": t.version,
            "tags": t.tags
        } for t in tools]
    
    def get_tool_schema(self, name: str) -> Dict:
        """获取工具的完整 JSON Schema（供 LLM function calling）"""
        tool = self.resolve(name)
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema
            }
        }
```

### 5.2 Agent Gateway（对标 OpenClaw）

```python
# src/tool/agent_gateway.py
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time

class AgentStatus(Enum):
    ONLINE = "online"
    BUSY = "busy"
    OFFLINE = "offline"

@dataclass
class AgentInfo:
    agent_id: str
    name: str
    capabilities: List[str]
    endpoint: str
    status: AgentStatus = AgentStatus.OFFLINE
    last_heartbeat: float = 0.0
    quota_used: int = 0
    quota_limit: int = 1000

@dataclass
class RoutedMessage:
    message_id: str
    source_agent: str
    target_agent: str
    payload: dict
    timestamp: float = field(default_factory=time.time)
    ttl_seconds: int = 300

class AgentGateway:
    """
    对标 OpenClaw 网关：
    Agent Discovery + Message Routing + Auth/Quota
    """
    
    def __init__(self):
        self._agents: Dict[str, AgentInfo] = {}
        self._routes: Dict[str, List[str]] = {}  # capability → agent_ids
        self._message_queue: List[RoutedMessage] = []
        self._auth_tokens: Dict[str, str] = {}  # agent_id → token
    
    def register(self, agent: AgentInfo, auth_token: str) -> None:
        """Agent 注册 + 能力索引构建"""
        self._agents[agent.agent_id] = agent
        self._auth_tokens[agent.agent_id] = auth_token
        
        for cap in agent.capabilities:
            if cap not in self._routes:
                self._routes[cap] = []
            if agent.agent_id not in self._routes[cap]:
                self._routes[cap].append(agent.agent_id)
    
    def discover(self, capability: str) -> List[AgentInfo]:
        """能力发现：找到能处理特定能力的 Agent"""
        agent_ids = self._routes.get(capability, [])
        return [
            self._agents[aid] for aid in agent_ids
            if self._agents[aid].status != AgentStatus.OFFLINE
        ]
    
    def route(self, message: RoutedMessage, auth_token: str) -> bool:
        """消息路由 + 鉴权 + 配额检查"""
        # 鉴权
        if self._auth_tokens.get(message.source_agent) != auth_token:
            raise PermissionError("Authentication failed")
        
        # 配额检查
        source = self._agents.get(message.source_agent)
        if source and source.quota_used >= source.quota_limit:
            raise QuotaExceededError(f"Agent {message.source_agent} quota exceeded")
        
        target = self._agents.get(message.target_agent)
        if not target:
            raise ValueError(f"Target agent {message.target_agent} not found")
        
        self._message_queue.append(message)
        if source:
            source.quota_used += 1
        
        return True
    
    def heartbeat(self, agent_id: str) -> None:
        """心跳检测"""
        if agent_id in self._agents:
            self._agents[agent_id].last_heartbeat = time.time()
            self._agents[agent_id].status = AgentStatus.ONLINE
    
    def cleanup_stale(self, timeout_seconds: int = 60):
        """清理超时Agent"""
        now = time.time()
        for agent in self._agents.values():
            if now - agent.last_heartbeat > timeout_seconds:
                agent.status = AgentStatus.OFFLINE
```

---

## 六、本地执行层 (INFRA)

### 6.1 本地模型部署（对标 Ollama + LM Studio）

```python
# src/infra/ollama_deploy.py
import subprocess
import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class LocalModelConfig:
    model_name: str
    model_path: str
    quantization: str  # q4_0, q4_1, q5_0, q8_0, f16
    context_length: int = 4096
    gpu_layers: int = 0  # GPU 加速层数

class OllamaDeployManager:
    """
    对标 Ollama + LM Studio：
    本地模型部署、管理、推理
    """
    
    SUPPORTED_MODELS = {
        "qwen2.5": {"sizes": ["0.5b", "1.5b", "7b", "14b", "72b"], "context": 32768},
        "deepseek-coder": {"sizes": ["1.3b", "6.7b", "33b"], "context": 16384},
        "codellama": {"sizes": ["7b", "13b", "34b"], "context": 16384},
        "phi3": {"sizes": ["mini", "small", "medium"], "context": 4096},
        "llama3": {"sizes": ["8b", "70b"], "context": 8192},
    }
    
    def __init__(self):
        self._check_ollama_installed()
    
    def _check_ollama_installed(self):
        try:
            subprocess.run(["ollama", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("Ollama is not installed. Install from https://ollama.com")
    
    def list_models(self) -> List[Dict]:
        """列出已安装模型"""
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        models = []
        for line in result.stdout.strip().split("\n")[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    models.append({"name": parts[0], "size": parts[1]})
        return models
    
    def pull_model(self, model: str) -> bool:
        """拉取模型"""
        result = subprocess.run(["ollama", "pull", model], capture_output=True, text=True)
        return result.returncode == 0
    
    def generate(self, model: str, prompt: str, system_prompt: Optional[str] = None) -> str:
        """本地模型推理"""
        cmd = ["ollama", "run", model, prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return result.stdout.strip()
    
    def create_custom_model(self, config: LocalModelConfig, modelfile_content: str) -> bool:
        """创建自定义模型（基于 Modelfile）"""
        import tempfile, os
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".Modelfile", delete=False) as f:
            f.write(f"""FROM {config.model_path}
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx {config.context_length}
{modelfile_content}
""")
            modelfile_path = f.name
        
        try:
            result = subprocess.run(
                ["ollama", "create", config.model_name, "-f", modelfile_path],
                capture_output=True, text=True
            )
            return result.returncode == 0
        finally:
            os.unlink(modelfile_path)
```

### 6.2 安全沙箱（对标 Marvis Workbody）

```python
# src/infra/sandbox.py
import os
import tempfile
from typing import Dict, List, Optional, Set

class SandboxLevel:
    """三层隔离级别"""
    NONE = 0       # 无隔离（信任环境）
    PROCESS = 1    # 进程级隔离（默认）
    CONTAINER = 2  # 容器级隔离（最高安全）

class Sandbox:
    """
    对标 Marvis Workbody Sandbox：
    进程隔离 + 文件系统隔离 + 网络隔离
    """
    
    def __init__(self, level: SandboxLevel = SandboxLevel.PROCESS):
        self.level = level
        self._workspace = tempfile.mkdtemp(prefix="doubao_sandbox_")
        self._allowed_paths: Set[str] = set()
        self._network_enabled = False
    
    @property
    def workspace(self) -> str:
        return self._workspace
    
    def allow_path(self, path: str):
        """添加允许访问的路径"""
        self._allowed_paths.add(os.path.abspath(path))
    
    def allow_network(self, enabled: bool = True):
        """控制网络访问"""
        self._network_enabled = enabled
    
    def validate_access(self, target_path: str) -> bool:
        """校验文件访问权限"""
        abs_path = os.path.abspath(target_path)
        
        # 禁止系统路径
        forbidden_prefixes = ["/etc/", "/sys/", "/proc/", "C:\\Windows\\"]
        for prefix in forbidden_prefixes:
            if abs_path.startswith(prefix):
                return False
        
        # 检查是否在允许路径内
        return any(abs_path.startswith(allowed) for allowed in self._allowed_paths)
    
    def cleanup(self):
        """清理沙箱环境"""
        import shutil
        if os.path.exists(self._workspace):
            shutil.rmtree(self._workspace, ignore_errors=True)
```

---

## 七、自进化闭环层 (EVOL)

### 7.1 自进化循环（Act → Observe → Reflect → Update）

```python
# src/evol/observer.py
from typing import Dict, List, Any
from dataclasses import dataclass, field
import time
import json

@dataclass
class ExecutionTrace:
    trace_id: str
    task_type: str
    start_time: float
    end_time: float
    success: bool
    steps: List[Dict]
    tools_used: List[str]
    error_message: Optional[str] = None

class Observer:
    """
    自进化闭环 Step 1: Observe
    全量行为日志采集 + 性能指标监控
    """
    
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.current_trace: Optional[ExecutionTrace] = None
    
    def start_trace(self, task_type: str) -> str:
        """开始追踪"""
        import uuid
        trace_id = uuid.uuid4().hex[:16]
        self.current_trace = ExecutionTrace(
            trace_id=trace_id,
            task_type=task_type,
            start_time=time.time(),
            end_time=0,
            success=False,
            steps=[]
        )
        return trace_id
    
    def record_step(self, step: Dict):
        """记录执行步骤"""
        if self.current_trace:
            self.current_trace.steps.append({
                "timestamp": time.time(),
                **step
            })
    
    def record_tool_usage(self, tool_name: str):
        """记录工具使用"""
        if self.current_trace and tool_name not in self.current_trace.tools_used:
            self.current_trace.tools_used.append(tool_name)
    
    def end_trace(self, success: bool, error: Optional[str] = None):
        """结束追踪并持久化"""
        if self.current_trace:
            self.current_trace.end_time = time.time()
            self.current_trace.success = success
            self.current_trace.error_message = error
            
            # 持久化
            import os
            os.makedirs(self.storage_path, exist_ok=True)
            filepath = os.path.join(self.storage_path, f"trace_{self.current_trace.trace_id}.json")
            with open(filepath, "w") as f:
                json.dump(self.current_trace.__dict__, f, indent=2)
```

```python
# src/evol/reflect_engine.py
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

class ReflectEngine:
    """
    自进化闭环 Step 2: Reflect
    失败模式分析 + 成功策略提炼 + 决策树优化
    """
    
    def __init__(self, memory_bank):
        self.memory = memory_bank
    
    def analyze_failures(self, traces: List[Dict], window_days: int = 7) -> Dict:
        """分析近期失败模式"""
        from datetime import datetime, timedelta
        
        cutoff = (datetime.now() - timedelta(days=window_days)).timestamp()
        recent_traces = [t for t in traces if t["start_time"] >= cutoff]
        failures = [t for t in recent_traces if not t["success"]]
        
        # 失败模式分类
        patterns = defaultdict(lambda: {"count": 0, "examples": []})
        for f in failures:
            error_type = self._classify_error(f.get("error_message", ""))
            patterns[error_type]["count"] += 1
            if len(patterns[error_type]["examples"]) < 3:
                patterns[error_type]["examples"].append({
                    "task_type": f["task_type"],
                    "error": f.get("error_message"),
                })
        
        return {
            "total_failures": len(failures),
            "failure_rate": len(failures) / max(len(recent_traces), 1),
            "patterns": dict(patterns)
        }
    
    def extract_success_patterns(self, traces: List[Dict]) -> List[Dict]:
        """提炼成功策略模式"""
        successes = [t for t in traces if t["success"]]
        
        # 按 task_type 分组分析
        by_type = defaultdict(list)
        for s in successes:
            by_type[s["task_type"]].append(s)
        
        patterns = []
        for task_type, group in by_type.items():
            # 找出该类型成功的共同特征
            tool_freq = defaultdict(int)
            avg_steps = 0
            for g in group:
                avg_steps += len(g["steps"])
                for tool in g["tools_used"]:
                    tool_freq[tool] += 1
            
            patterns.append({
                "task_type": task_type,
                "sample_count": len(group),
                "avg_steps": avg_steps / len(group),
                "most_used_tools": sorted(tool_freq.items(), key=lambda x: -x[1])[:5],
                "avg_duration": sum(g["end_time"] - g["start_time"] for g in group) / len(group)
            })
        
        return patterns
    
    def generate_improvement_suggestions(self, analysis: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        for error_type, data in analysis.get("patterns", {}).items():
            if data["count"] >= 3:  # 高频失败
                suggestions.append(
                    f"[{error_type}] Failed {data['count']} times. "
                    f"Consider adding pre-check validation or alternative approach."
                )
        
        return suggestions
    
    def _classify_error(self, error_msg: str) -> str:
        if "timeout" in error_msg.lower():
            return "TIMEOUT"
        elif "permission" in error_msg.lower():
            return "PERMISSION"
        elif "not found" in error_msg.lower():
            return "NOT_FOUND"
        elif "validation" in error_msg.lower():
            return "VALIDATION"
        else:
            return "UNKNOWN"
```

---

## 八、AI IDE 完整功能

### 8.1 Agentic IDE 核心

```python
# src/execute/agentic_ide.py
from dataclasses import dataclass
from typing import Dict, List, Optional
import os

@dataclass
class IDEFileNode:
    name: str
    path: str
    is_dir: bool
    children: Optional[List['IDEFileNode']] = None

@dataclass
class IDESession:
    session_id: str
    project_root: str
    open_files: List[str]
    active_file: Optional[str]
    terminal_cwd: str

class AgenticIDE:
    """
    对标 AI IDE 趋势：
    内嵌代码编辑器 + 文件树 + 终端 + 调试器 + Git面板
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.session = IDESession(
            session_id="",
            project_root=project_root,
            open_files=[],
            active_file=None,
            terminal_cwd=project_root
        )
    
    def get_file_tree(self, max_depth: int = 3) -> IDEFileNode:
        """获取项目文件树"""
        def build_tree(path: str, depth: int) -> IDEFileNode:
            name = os.path.basename(path) or path
            is_dir = os.path.isdir(path)
            children = None
            
            if is_dir and depth < max_depth:
                try:
                    entries = sorted(os.listdir(path))
                    children = [
                        build_tree(os.path.join(path, e), depth + 1)
                        for e in entries
                        if not e.startswith('.') and e not in ['node_modules', '__pycache__']
                    ]
                except PermissionError:
                    children = []
            
            return IDEFileNode(name=name, path=path, is_dir=is_dir, children=children)
        
        return build_tree(self.project_root, 0)
    
    def open_file(self, file_path: str) -> str:
        """打开文件（读取内容）"""
        abs_path = os.path.join(self.project_root, file_path) if not os.path.isabs(file_path) else file_path
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.session.open_files.append(file_path)
        self.session.active_file = file_path
        return content
    
    def edit_file(self, file_path: str, edits: List[Dict]) -> bool:
        """编辑文件：支持行插入/替换/删除"""
        abs_path = os.path.join(self.project_root, file_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for edit in sorted(edits, key=lambda e: e.get("line", 0), reverse=True):
            op = edit["op"]
            line = edit.get("line", 0)
            content = edit.get("content", "")
            
            if op == "insert":
                lines.insert(line, content + "\n")
            elif op == "replace":
                lines[line] = content + "\n"
            elif op == "delete":
                del lines[line]
        
        with open(abs_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        return True
    
    def get_git_status(self) -> Dict:
        """获取 Git 状态（Git面板）"""
        import subprocess
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True,
                cwd=self.project_root
            )
            files = [line[3:] for line in result.stdout.strip().split("\n") if line]
            return {"clean": len(files) == 0, "changed_files": files}
        except subprocess.CalledProcessError:
            return {"clean": True, "changed_files": [], "error": "Not a git repository"}
```

---

## 九、数据流与交互协议

### 9.1 请求处理全链路

```
用户请求 → Agent Gateway [Auth/Rate Limit] → Central Orchestrator [路由]
  → CoT Engine [推理] → Plan-Execute [规划]
  → Multi-Agent Coding [并行编码]
    → Code Engine [生成代码] → Shell Sandbox [执行验证]
    → Code Reviewer [审查] → Test Generator [测试]
  → Tool Registry [记录工具调用]
  → Observer [行为日志] → Reflect Engine [策略优化]
  → Agent Gateway → 用户响应
```

### 9.2 跨层通信协议

| 层级间 | 协议 | 格式 | 说明 |
|--------|------|------|------|
| Gateway → Orchestrator | HTTP/gRPC | JSON/Protobuf | 同步请求-响应 |
| Orchestrator → Plan | 内部事件 | Python dict | 异步消息 |
| Plan → EXEC | 指令队列 | Task object | 有优先级调度 |
| EXEC → Tool Registry | 本地调用 | function call | 同步 |
| EVOL → All Layers | 旁路监听 | Event log | 异步、非阻塞 |
| All → Memory Bank | 写入API | MemoryChunk | 异步持久化 |

---

## 十、部署与运维

### 10.1 Docker Compose 部署

```yaml
# deploy/docker-compose.yml
version: '3.8'
services:
  orchestrator:
    build: ./src/think
    ports: ["8000:8000"]
    environment:
      - DOUBAO_ENV=production
      - OLLAMA_HOST=http://ollama:11434
    depends_on: [ollama, chromadb, redis]
    volumes:
      - ./workspace:/workspace
      - ./checkpoints:/checkpoints

  ollama:
    image: ollama/ollama:latest
    ports: ["11434:11434"]
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  chromadb:
    image: chromadb/chroma:latest
    ports: ["8001:8000"]
    volumes:
      - chroma_data:/chroma/chroma

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  sandbox:
    build: ./src/infra
    privileged: false
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp:size=512M

volumes:
  ollama_data:
  chroma_data:
```

### 10.2 健康检查

```python
# src/infra/health_check.py
async def health_check() -> dict:
    results = {}
    
    # Ollama
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:11434/api/tags")
            results["ollama"] = "ok" if resp.status_code == 200 else "error"
    except:
        results["ollama"] = "unreachable"
    
    # ChromaDB
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:8001/api/v1/heartbeat")
            results["chromadb"] = "ok" if resp.status_code == 200 else "error"
    except:
        results["chromadb"] = "unreachable"
    
    return results
```

---

> **方案维护**：本方案在每次龙虾五步法全维度迭代中更新  
> **下一版预告**：v2.4 将补齐全部52项能力的代码模板实现，并完成本地部署 MVP
