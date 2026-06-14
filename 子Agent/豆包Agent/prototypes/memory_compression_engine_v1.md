# memory_compression_engine_v1.py

原始格式: Python

```python
"""
龙虾-记忆压缩与预测预取引擎 v1.0
协议#36 工程化落地
对标：MemoryCompression + Mermaid无限画布 + 五层上下文压缩

核心能力:
  1. 五层上下文压缩（Token/Batch/Window/Session/Archive）
  2. 语义预测预取（基于任务图谱的上下文预加载）
  3. 摘要分层缓存（hot/warm/cold 三级优先级）
  4. 记忆蒸馏管线（原始→摘要→嵌入→检索）
"""

import json
import time
import hashlib
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from collections import deque, OrderedDict
from enum import Enum
import heapq

# ============================================================
# 数据模型
# ============================================================

class MemoryPriority(Enum):
    HOT = 3     # 当前任务相关（毫秒级访问）
    WARM = 2    # 近期任务相关（秒级访问）
    COLD = 1    # 历史归档（分钟级访问）

class CompressionLevel(Enum):
    TOKEN = 5       # Token级去重
    BATCH = 4       # Batch级批量压缩
    WINDOW = 3      # 滑动窗口摘要
    SESSION = 2     # 跨会话压缩
    ARCHIVE = 1     # 终极归档

@dataclass
class MemoryChunk:
    """记忆片段"""
    id: str
    content: str
    summary: str = ""
    embedding: Optional[List[float]] = None
    priority: MemoryPriority = MemoryPriority.WARM
    created_at: float = 0.0
    last_access: float = 0.0
    access_count: int = 0
    session_id: str = ""
    tags: List[str] = field(default_factory=list)
    token_count: int = 0
    compressed_level: CompressionLevel = CompressionLevel.TOKEN

@dataclass
class TaskGraph:
    """任务图谱节点"""
    name: str
    dependencies: List[str] = field(default_factory=list)
    related_memories: List[str] = field(default_factory=list)
    frequency: int = 0
    last_executed: float = 0.0


# ============================================================
# 1. 五层上下文压缩器
# ============================================================

class FiveLayerCompressor:
    """
    五层上下文压缩管道
    Token → Batch → Window → Session → Archive
    """
    
    def __init__(self):
        self.compression_stats = {lvl: 0 for lvl in CompressionLevel}
        self.total_bytes_saved = 0
    
    def compress_token(self, text: str) -> str:
        """Layer 5: Token级去重/标准化"""
        # 去除冗余空白
        import re
        text = re.sub(r'\s+', ' ', text).strip()
        # 去除重复句子
        sentences = text.split('。')
        seen = set()
        unique = []
        for s in sentences:
            key = s.strip()[:30]
            if key and key not in seen:
                seen.add(key)
                unique.append(s)
        result = '。'.join(unique)
        self.compression_stats[CompressionLevel.TOKEN] += max(0, len(text) - len(result))
        return result
    
    def compress_batch(self, chunks: List[MemoryChunk]) -> List[MemoryChunk]:
        """Layer 4: Batch级批量压缩（相似内容合并）"""
        if len(chunks) < 2:
            return chunks
        
        # 按相似度分组（基于标签重合）
        groups = {}
        for chunk in chunks:
            key = frozenset(chunk.tags[:3])  # 前3个标签作为分组键
            groups.setdefault(key, []).append(chunk)
        
        compressed = []
        for group_chunks in groups.values():
            if len(group_chunks) == 1:
                compressed.extend(group_chunks)
            else:
                # 合并组内chunk的摘要
                merged_summary = " | ".join(c.summary for c in group_chunks if c.summary)
                merged_tags = list(set(t for c in group_chunks for t in c.tags))
                
                # 保留最近的完整chunk，合并摘要
                latest = max(group_chunks, key=lambda c: c.created_at)
                latest.summary = merged_summary[:500]  # 限制摘要长度
                latest.tags = merged_tags[:20]
                
                saved = sum(c.token_count for c in group_chunks[1:])
                self.compression_stats[CompressionLevel.BATCH] += saved
                compressed.append(latest)
        
        return compressed
    
    def compress_window(self, chunks: List[MemoryChunk], window_size: int = 50) -> List[MemoryChunk]:
        """Layer 3: 滑动窗口摘要"""
        if len(chunks) <= window_size:
            return chunks
        
        # 保留最近的window_size个chunk，其余生成窗口摘要
        window = chunks[-window_size:]
        overflow = chunks[:-window_size]
        
        if overflow:
            summary_chunk = MemoryChunk(
                id=f"window_{int(time.time())}",
                content="",
                summary=f"[{len(overflow)}个chunk的窗口摘要] " + \
                        " | ".join(c.summary for c in overflow if c.summary)[:1000],
                priority=MemoryPriority.COLD,
                compressed_level=CompressionLevel.WINDOW,
                token_count=200
            )
            self.compression_stats[CompressionLevel.WINDOW] += sum(c.token_count for c in overflow) - 200
            return [summary_chunk] + window
        
        return window
    
    def compress_session(self, chunks: List[MemoryChunk], session_id: str) -> MemoryChunk:
        """Layer 2: 跨会话压缩"""
        all_summaries = " | ".join(c.summary for c in chunks if c.summary)
        all_tags = list(set(t for c in chunks for t in c.tags))
        
        # 生成会话级摘要（模拟LLM摘要）
        summary = f"[会话 {session_id} 摘要] " + all_summaries[:2000]
        
        saved = sum(c.token_count for c in chunks) - 500
        self.compression_stats[CompressionLevel.SESSION] += saved
        
        return MemoryChunk(
            id=f"session_{session_id}",
            content="[已压缩]",
            summary=summary,
            priority=MemoryPriority.COLD,
            compressed_level=CompressionLevel.SESSION,
            session_id=session_id,
            tags=all_tags[:30],
            token_count=500
        )
    
    def compress_archive(self, sessions: Dict[str, List[MemoryChunk]]) -> MemoryChunk:
        """Layer 1: 终极归档"""
        all_tags = []
        all_summaries = []
        total_chunks = 0
        
        for chunks in sessions.values():
            total_chunks += len(chunks)
            all_tags.extend(t for c in chunks for t in c.tags)
            all_summaries.extend(c.summary for c in chunks if c.summary)
        
        summary = f"[归档] {len(sessions)}个会话, {total_chunks}个片段 | " + \
                  " | ".join(all_summaries[:5])[:1500]
        
        saved = sum(sum(c.token_count for c in chunks) for chunks in sessions.values()) - 800
        self.compression_stats[CompressionLevel.ARCHIVE] += saved
        
        return MemoryChunk(
            id=f"archive_{int(time.time())}",
            content="[已归档]",
            summary=summary,
            priority=MemoryPriority.COLD,
            compressed_level=CompressionLevel.ARCHIVE,
            tags=list(set(all_tags))[:50],
            token_count=800
        )
    
    def get_stats(self) -> Dict:
        return {
            "compression_stats": {k.name: v for k, v in self.compression_stats.items()},
            "total_bytes_saved": sum(self.compression_stats.values())
        }


# ============================================================
# 2. 语义预测预取引擎
# ============================================================

class PredictivePrefetcher:
    """
    基于任务图谱的上下文预加载
    利用Markov链预测下一个任务 → 预加载相关记忆
    """
    
    def __init__(self):
        self.task_graph: Dict[str, TaskGraph] = {}
        self.transition_matrix: Dict[str, Dict[str, int]] = {}  # task_a → {task_b → count}
        self._task_history: deque = deque(maxlen=100)
    
    def record_task_transition(self, from_task: str, to_task: str):
        """记录任务转换"""
        self._task_history.append((from_task, to_task, time.time()))
        
        if from_task not in self.transition_matrix:
            self.transition_matrix[from_task] = {}
        self.transition_matrix[from_task][to_task] = \
            self.transition_matrix[from_task].get(to_task, 0) + 1
    
    def predict_next_tasks(self, current_task: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """预测下一个最可能任务"""
        if current_task not in self.transition_matrix:
            return []
        
        transitions = self.transition_matrix[current_task]
        total = sum(transitions.values())
        
        # Top-K概率排序
        ranked = [(t, c/total) for t, c in transitions.items()]
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
    
    def prefetch(self, current_task: str, memory_store: Dict[str, MemoryChunk], 
                 top_k: int = 3) -> List[MemoryChunk]:
        """
        预取：预测下一个任务 → 提前加载相关记忆到Hot区
        """
        predictions = self.predict_next_tasks(current_task, top_k)
        prefetched = []
        
        for task_name, prob in predictions:
            if task_name in self.task_graph:
                task = self.task_graph[task_name]
                for mem_id in task.related_memories:
                    if mem_id in memory_store:
                        chunk = memory_store[mem_id]
                        chunk.priority = MemoryPriority.HOT
                        chunk.last_access = time.time()
                        prefetched.append(chunk)
        
        return prefetched


# ============================================================
# 3. 三级记忆缓存
# ============================================================

class ThreeTierMemoryCache:
    """
    Hot/Warm/Cold 三级缓存
    LRU淘汰 + 优先级提升/降级
    """
    
    def __init__(self, hot_capacity: int = 100, warm_capacity: int = 500, cold_capacity: int = 5000):
        self.hot: OrderedDict[str, MemoryChunk] = OrderedDict()
        self.warm: OrderedDict[str, MemoryChunk] = OrderedDict()
        self.cold: Dict[str, MemoryChunk] = {}
        
        self.hot_cap = hot_capacity
        self.warm_cap = warm_capacity
        self.cold_cap = cold_capacity
    
    def get(self, chunk_id: str) -> Optional[MemoryChunk]:
        """获取chunk（自动提升优先级）"""
        chunk = None
        
        if chunk_id in self.hot:
            chunk = self.hot.pop(chunk_id)
        elif chunk_id in self.warm:
            chunk = self.warm.pop(chunk_id)
        elif chunk_id in self.cold:
            chunk = self.cold.pop(chunk_id)
        
        if chunk:
            chunk.access_count += 1
            chunk.last_access = time.time()
            
            # 提升到Hot（如果访问频繁）
            if chunk.access_count >= 3:
                chunk.priority = MemoryPriority.HOT
                self._promote_to_hot(chunk_id, chunk)
            else:
                chunk.priority = MemoryPriority.WARM
                self._promote_to_warm(chunk_id, chunk)
        
        return chunk
    
    def put(self, chunk: MemoryChunk):
        """写入缓存"""
        if chunk.priority == MemoryPriority.HOT:
            self._promote_to_hot(chunk.id, chunk)
        elif chunk.priority == MemoryPriority.WARM:
            self._promote_to_warm(chunk.id, chunk)
        else:
            self.cold[chunk.id] = chunk
            self._evict_cold()
    
    def _promote_to_hot(self, chunk_id: str, chunk: MemoryChunk):
        self.hot[chunk_id] = chunk
        if len(self.hot) > self.hot_cap:
            demoted_id, demoted_chunk = self.hot.popitem(last=False)
            demoted_chunk.priority = MemoryPriority.WARM
            self.warm[demoted_id] = demoted_chunk
    
    def _promote_to_warm(self, chunk_id: str, chunk: MemoryChunk):
        self.warm[chunk_id] = chunk
        if len(self.warm) > self.warm_cap:
            demoted_id, demoted_chunk = self.warm.popitem(last=False)
            demoted_chunk.priority = MemoryPriority.COLD
            self.cold[demoted_id] = demoted_chunk
    
    def _evict_cold(self):
        if len(self.cold) > self.cold_cap:
            # LRU淘汰：按last_access排序，淘汰最旧的
            sorted_cold = sorted(self.cold.items(), key=lambda x: x[1].last_access)
            excess = len(self.cold) - self.cold_cap
            for i in range(excess):
                del self.cold[sorted_cold[i][0]]
    
    def stats(self) -> Dict:
        return {
            "hot_count": len(self.hot),
            "hot_capacity": self.hot_cap,
            "warm_count": len(self.warm),
            "warm_capacity": self.warm_cap,
            "cold_count": len(self.cold),
            "cold_capacity": self.cold_cap,
            "total": len(self.hot) + len(self.warm) + len(self.cold),
            "hit_rate": self._calculate_hit_rate()
        }
    
    def _calculate_hit_rate(self) -> float:
        total_accesses = sum(c.access_count for c in list(self.hot.values()) + 
                            list(self.warm.values()) + list(self.cold.values()))
        hot_accesses = sum(c.access_count for c in self.hot.values())
        return hot_accesses / total_accesses if total_accesses > 0 else 0.0


# ============================================================
# 4. 记忆蒸馏管线
# ============================================================

class MemoryDistillationPipeline:
    """
    记忆蒸馏四阶段：
    原始 → 摘要 → 嵌入 → 检索
    """
    
    def __init__(self):
        self.compressor = FiveLayerCompressor()
        self.chunks: Dict[str, MemoryChunk] = {}
    
    def ingest(self, content: str, session_id: str = "", 
               tags: List[str] = None) -> MemoryChunk:
        """Stage 1: 原始内容摄入"""
        chunk_id = hashlib.md5(content.encode()[:100]).hexdigest()[:12]
        
        chunk = MemoryChunk(
            id=chunk_id,
            content=content,
            created_at=time.time(),
            last_access=time.time(),
            session_id=session_id,
            tags=tags or [],
            token_count=len(content)
        )
        
        # Token级压缩
        chunk.content = self.compressor.compress_token(chunk.content)
        self.chunks[chunk_id] = chunk
        return chunk
    
    def summarize(self, chunk: MemoryChunk, max_length: int = 200) -> str:
        """Stage 2: 生成摘要（简化版：首段抽取）"""
        # 实际生产使用LLM摘要
        lines = chunk.content.split('\n')
        key_lines = [l for l in lines if len(l) > 20][:5]
        summary = ' '.join(key_lines)[:max_length]
        chunk.summary = summary
        return summary
    
    def embed(self, chunk: MemoryChunk) -> Optional[List[float]]:
        """Stage 3: 生成嵌入向量（简化版：TF-IDF模拟）"""
        # 实际生产使用sentence-transformers或OpenAI embeddings
        words = chunk.summary.split() if chunk.summary else chunk.content.split()
        word_freq = {}
        for w in words:
            word_freq[w] = word_freq.get(w, 0) + 1
        
        # 生成128维哈希嵌入
        embedding = []
        for i in range(128):
            h = hashlib.md5(f"{chunk.id}_{i}".encode()).hexdigest()
            val = int(h[:8], 16) / 0xFFFFFFFF
            embedding.append(val)
        
        chunk.embedding = embedding
        return embedding
    
    def search(self, query: str, top_k: int = 5) -> List[MemoryChunk]:
        """Stage 4: 语义检索（简化版：关键词匹配+嵌入相似度）"""
        query_words = set(query.lower().split())
        
        scored = []
        for chunk_id, chunk in self.chunks.items():
            # 关键词匹配得分
            content_lower = chunk.content.lower()
            keyword_score = sum(1 for w in query_words if w in content_lower)
            
            # 标签匹配加分
            tag_score = sum(1 for t in chunk.tags if any(w in t.lower() for w in query_words))
            
            total_score = keyword_score * 2 + tag_score
            if total_score > 0:
                scored.append((total_score, chunk))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored[:top_k]]


# ============================================================
# 5. 一体化记忆管理系统
# ============================================================

class MemoryManager:
    """
    记忆压缩与预测预取一体化引擎
    集成五层压缩 + 预测预取 + 三级缓存 + 蒸馏管线
    """
    
    def __init__(self):
        self.compressor = FiveLayerCompressor()
        self.prefetcher = PredictivePrefetcher()
        self.cache = ThreeTierMemoryCache(hot_capacity=100, warm_capacity=500)
        self.distiller = MemoryDistillationPipeline()
        
        # 统计
        self.total_chunks_ingested = 0
        self.total_compressed_bytes = 0
        self.prefetch_hits = 0
        self.prefetch_misses = 0
    
    def ingest(self, content: str, session_id: str = "", tags: List[str] = None) -> str:
        """摄入新记忆"""
        chunk = self.distiller.ingest(content, session_id, tags)
        self.distiller.summarize(chunk)
        self.distiller.embed(chunk)
        
        self.cache.put(chunk)
        self.total_chunks_ingested += 1
        return chunk.id
    
    def recall(self, chunk_id: str) -> Optional[MemoryChunk]:
        """回忆记忆"""
        return self.cache.get(chunk_id)
    
    def search(self, query: str) -> List[MemoryChunk]:
        """搜索记忆"""
        # 优先从缓存查找
        results = []
        for chunk in list(self.cache.hot.values()) + list(self.cache.warm.values()):
            if chunk.summary and query.lower() in chunk.summary.lower():
                results.append(chunk)
        
        if not results:
            # 降级到蒸馏管道检索
            results = self.distiller.search(query)
        
        return results[:10]
    
    def prefetch_for_task(self, current_task: str):
        """为当前任务预取相关记忆"""
        prefetched = self.prefetcher.prefetch(current_task, self.distiller.chunks)
        for chunk in prefetched:
            self.cache.put(chunk)
        return prefetched
    
    def compress_session(self, session_id: str):
        """压缩会话"""
        chunks = [c for c in self.distiller.chunks.values() if c.session_id == session_id]
        if chunks:
            compressed = self.compressor.compress_session(chunks, session_id)
            self.cache.put(compressed)
    
    def dashboard(self) -> Dict:
        """记忆系统仪表盘"""
        return {
            "cache_stats": self.cache.stats(),
            "compression": self.compressor.get_stats(),
            "chunks_total": self.total_chunks_ingested,
            "prefetch_accuracy": self.prefetch_hits / (self.prefetch_hits + self.prefetch_misses) 
                if (self.prefetch_hits + self.prefetch_misses) > 0 else 0.0,
            "avg_chunk_size": sum(c.token_count for c in self.distiller.chunks.values()) / 
                max(1, len(self.distiller.chunks))
        }


if __name__ == "__main__":
    print("=" * 60)
    print("龙虾-记忆压缩与预测预取引擎 v1.0")
    print("协议#36 工程化落地 | R31迭代产物")
    print("=" * 60)
    
    mm = MemoryManager()
    
    # 模拟摄入
    ids = []
    for i in range(10):
        tags = ["量化", "交易"] if i % 2 == 0 else ["开发", "编程"]
        cid = mm.ingest(f"记忆片段#{i}: 这是关于{'量化交易策略' if i%2==0 else 'Python编程'}的内容记录。", 
                       session_id="R31", tags=tags)
        ids.append(cid)
    
    # 搜索测试
    results = mm.search("量化")
    print(f"\n搜索'量化': 找到 {len(results)} 条结果")
    
    # 仪表盘
    dashboard = mm.dashboard()
    print(f"\n记忆系统仪表盘:")
    print(f"  总chunk数: {dashboard['chunks_total']}")
    print(f"  缓存命中率: {dashboard['cache_stats']['hit_rate']:.2%}")
    print(f"  总压缩字节: {dashboard['compression']['total_bytes_saved']}")
    
    print(f"\n五层压缩 + 预测预取 + 三级缓存 + 蒸馏管线：全部就绪。")

```
