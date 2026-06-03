# Obsidian 联动桥接方案 v1.0

> **目的**：建立豆包Agent与Obsidian知识库的双向联动机制  
> **核心理念**：三层知识架构（L1实时缓存 / L2工作记忆 / L3永久知识库）  
> **关联系统**：龙虾全域Agent体系 + 26维对标矩阵  

---

## 一、三层知识架构 → Obsidian目录映射

### 1.1 架构总览

```
三层知识架构                           Obsidian Vault 映射
─────────────────────────────────────  ─────────────────────────────────
L1 实时缓存（Session Context）    →   00_Inbox/          对话临时切片
L2 工作记忆（Structured Memory）  →   10_WorkingMemory/   Skill执行记录、调度日志
L3 永久知识库（Long-term KB）     →   20_KnowledgeBase/   标准化Skill、对标文档
                                    →   30_Meta/           索引、图谱配置
```

### 1.2 目录结构设计

```
龙虾AI知识库/                          # Obsidian Vault 根目录
├── 00_Inbox/                          # L1: 实时缓存
│   ├── Session_YYYYMMDD_HHmmss.md     #    每轮对话切片（自动归档）
│   └── .archive/                      #    已处理的Session移至此处
│
├── 10_WorkingMemory/                  # L2: 工作记忆
│   ├── Dispatch_Logs/                 #    调度执行日志
│   │   └── Dispatch_YYYYMMDD.md       #    每日调度记录
│   ├── Task_Results/                  #    阶段产出摘要
│   │   ├── 阶段一_文件清单.md
│   │   ├── 阶段二-A_核心模板摘要.md
│   │   ├── 阶段二-B_技术对标摘要.md
│   │   └── 阶段三_技能模块索引.md
│   └── Skill_Execution/               #    Skill调用记录
│       └── ...                        
│
├── 20_KnowledgeBase/                  # L3: 永久知识库
│   ├── Skills/                        #    标准化Skill模块
│   │   ├── Skill_01_多Agent并行调度.md
│   │   ├── Skill_02_桌面安全自动化控制.md
│   │   ├── Skill_03_长期记忆系统.md
│   │   ├── Skill_04_AI_on_UI全自动执行.md
│   │   ├── Skill_05_本地推理部署.md
│   │   ├── Skill_06_自主技能生成.md
│   │   ├── Skill_07_五步法执行引擎.md
│   │   └── Skill_08_全域对标矩阵维护.md
│   ├── Templates/                     #    模板库
│   │   ├── 龙虾全域官方模板-最终版.md
│   │   └── 龙虾五步法技能.md
│   ├── Benchmarks/                    #    对标文档
│   │   ├── Claude_Opus_4.8协议.md
│   │   ├── Hermes_SWARM协议.md
│   │   └── 26维对标矩阵.md
│   └── Infrastructure/               #    基础设施
│       ├── 本地推理部署方案.md
│       └── AI_on_UI架构.md
│
└── 30_Meta/                           # 元数据 & 索引
    ├── INDEX.md                       #    全局索引（MOC）
    ├── Graph_Config.json              #    图谱可视化配置
    ├── Tag_System.md                  #    标签体系定义
    └── Sync_Log.md                    #    同步日志
```

---

## 二、Markdown 双向链接策略

### 2.1 链接类型与语法

| 链接类型 | Obsidian 语法 | 示例 | 用途 |
|---------|-------------|------|------|
| **WikiLink（标准）** | `[[文件名]]` | `[[Skill_01_多Agent并行调度]]` | 跨文档引用 |
| **WikiLink + 别名** | `[[文件名\|显示文本]]` | `[[Skill_01_多Agent并行调度\|并行调度]]` | 简化引用 |
| **标题锚点** | `[[文件名#标题]]` | `[[26维对标矩阵#Claude对标]]` | 精准定位 |
| **块引用** | `[[文件名#^block-id]]` | `[[INDEX#^skill-summary]]` | 粒度引用 |
| **Markdown 链接** | `[文本](路径)` | `[调度日志](10_WorkingMemory/Dispatch_Logs/)` | 外部路径 |

### 2.2 自动链接生成规则

当Agent生成新文档时，自动注入以下双向链接：

```
新文档 A 生成时：
  1. 扫描文档内容，提取引用到的 Skill / 模板 / 对标文档名
  2. 在 A 头部插入 [[被引用文档]] 的入链声明
  3. 在被引用文档 B 的末尾新增 [[新文档A]] 出链声明（如果存在）
```

### 2.3 MOC（Map of Content）节点设计

```
INDEX.md 作为全局 MOC：
  - [[00_Inbox/]]          当前活跃会话
  - [[10_WorkingMemory/]]  调度记录与阶段产出
  - [[20_KnowledgeBase/]]  永久知识库
    - [[Skill_01]] [[Skill_02]] ... [[Skill_08]]
    - [[龙虾全域官方模板-最终版]]
    - [[26维对标矩阵]]
  - [[30_Meta/]]           元数据
```

---

## 三、定期同步脚本设计

### 3.1 同步架构

```
豆包Agent 产出目录              Obsidian Vault
(E:\...\豆包Agent\)    ──→    (龙虾AI知识库/)
                              │
                     sync_bridge.py
                     ├── 增量检测（MD5 + modify_time）
                     ├── 双向链接注入
                     ├── MOC 自动更新
                     └── 同步日志记录
```

### 3.2 同步触发策略

| 触发方式 | 间隔 | 适用场景 |
|---------|:---:|------|
| **阶段完成触发** | 每次阶段产出后 | 调度循环内自动同步 |
| **定时同步** | 每 4 小时 | 对应全域迭代循环周期 |
| **手动触发** | 按需 | 用户主动指令 `sync_to_obsidian` |

### 3.3 sync_bridge.py 伪代码

```python
# 核心同步逻辑（伪代码）
class ObsidianBridge:
    def __init__(self, source_dir, vault_dir):
        self.source = Path(source_dir)    # 豆包Agent产出目录
        self.vault = Path(vault_dir)      # Obsidian Vault根目录

    def detect_changes(self):
        """MD5 + modify_time 增量检测"""
        for file in self.source.rglob("*.md"):
            target = self.map_to_vault(file)
            if not target.exists() or md5(file) != md5(target):
                yield file, target

    def inject_bidirectional_links(self, content, file_name):
        """提取引用 → 注入双向 [[WikiLink]]"""
        refs = extract_references(content)
        header = "\n".join(f"- [[{r}]]" for r in refs)
        return f"{header}\n\n---\n\n{content}"

    def update_moc(self):
        """自动更新 INDEX.md MOC 节点"""
        # 扫描所有目录 → 生成/刷新 INDEX.md
        pass

    def sync(self):
        for src, dst in self.detect_changes():
            content = src.read_text(encoding="utf-8")
            content = self.inject_bidirectional_links(content, src.stem)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(content, encoding="utf-8")
        self.update_moc()
        self.write_sync_log()
```

### 3.4 目录映射规则

```
豆包Agent产出                    →  Obsidian Vault 目标
─────────────────────────────────────────────────────
多Agent调度测试报告_v1.0.md      →  10_WorkingMemory/Task_Results/
Obsidian联动桥接方案.md          →  30_Meta/
阶段二-A_核心模板摘要.md          →  10_WorkingMemory/Task_Results/
阶段二-B_技术对标摘要.md          →  10_WorkingMemory/Task_Results/
阶段三_技能模块/*.md              →  20_KnowledgeBase/Skills/
阶段三_技能模块/INDEX.md          →  30_Meta/INDEX_Skills.md
```

---

## 四、向量检索接口规划

### 4.1 接口层级

```
检索请求
    │
    ├── L1 快速语义检索（Session内）
    │   └── 基于 Embedding 的实时向量匹配
    │       范围：00_Inbox/ + 10_WorkingMemory/
    │       延迟：< 100ms
    │
    ├── L2 结构化检索（工作记忆）
    │   └── 标签 + 时间范围 + Skill类型 多维过滤
    │       范围：10_WorkingMemory/
    │       延迟：< 500ms
    │
    └── L3 深度语义检索（永久知识库）
        └── 全文向量索引 + RRF 融合排序
            范围：20_KnowledgeBase/ 全量
            延迟：< 2s
```

### 4.2 API 设计

```
POST /api/v1/search/semantic
{
  "query": "多Agent并行调度的安全边界是什么",
  "layers": ["L1", "L2", "L3"],      // 搜索范围
  "top_k": 10,
  "min_score": 0.7
}

Response:
{
  "results": [
    {
      "layer": "L3",
      "source": "20_KnowledgeBase/Skills/Skill_01_多Agent并行调度.md",
      "chunk": "## 六、安全边界\n...",
      "score": 0.94,
      "links": ["[[Hermes_SWARM协议]]", "[[龙虾调度体系]]"]
    }
  ],
  "fusion_strategy": "RRF",
  "latency_ms": 850
}
```

### 4.3 向量化策略

| 层级 | 切片粒度 | 向量模型 | 索引方式 |
|------|---------|---------|---------|
| L1 实时缓存 | 按段落 | text-embedding-3-small | 内存 FAISS |
| L2 工作记忆 | 按章节 | text-embedding-3-large | ChromaDB 持久化 |
| L3 永久知识库 | 按章节 + 语义块 | text-embedding-3-large | ChromaDB + 定期全量重建 |

### 4.4 检索增强生成（RAG）流程

```
用户查询
  │
  ├──→ 向量检索（L1 → L2 → L3 逐层fallback）
  │     │
  │     └──→ 检索结果排序（RRF融合）
  │           │
  │           └──→ 取 Top-K 切片 + [[WikiLink]] 上下文展开
  │                 │
  │                 └──→ 拼接为增强Context
  │
  └──→ 增强后的Context + 用户查询 → LLM推理 → 带来源引用的回答
```

---

## 五、实施路线图

| 阶段 | 内容 | 优先级 | 预估周期 |
|:---:|------|:---:|:---:|
| P1 | Obsidian Vault目录结构搭建 + 首批文件迁移 | 🔴 高 | 1天 |
| P2 | sync_bridge.py 开发 + 测试 | 🔴 高 | 2天 |
| P3 | Markdown双向链接自动注入 + MOC生成 | 🟡 中 | 1天 |
| P4 | ChromaDB向量索引搭建 + L2/L3语义检索 | 🟡 中 | 3天 |
| P5 | RAG检索增强生成管道 | 🟢 低 | 2天 |
| P6 | 定时同步cron + 监控面板 | 🟢 低 | 1天 |

---

> **版本**：v1.0  
> **生成时间**：2026-06-02  
> **对标来源**：Obsidian三层架构（L1/L2/L3）、Claude Agent OS、龙虾全域对标矩阵
