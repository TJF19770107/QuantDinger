# 三卡口Brainworm流量防御协议 v1.0

> **协议编号**：82
> **对标来源**：Hermes v0.15.0 Brainworm Defense
> **创建日期**：2026-06-01
> **状态**：Active
> **适用场景**：所有需要防御恶意输入、数据泄露、越权访问的AI Agent系统

---

## 一、协议概述

三卡口Brainworm流量防御协议借鉴了Hermes v0.15.0的Brainworm防御机制，在Agent系统的三个关键流量入口（工具输出、记忆召回、外部技能加载）设置安全检查点，实现主动威胁防御。

## 二、核心设计原则

1. **深度防御**：在多个层次设置安全检查，而非单一入口
2. **主动检测**：主动扫描潜在威胁，而非被动响应
3. **最小权限**：默认拒绝，按需授权
4. **可追溯性**：所有检查记录完整日志，便于审计

## 三、三卡口定义

### 3.1 卡口一：工具输出过滤

**位置**：工具执行完成后，结果返回给Agent前
**检查内容**：
- 敏感信息泄露（API密钥、密码、个人身份信息）
- 恶意代码/脚本注入
- 越权文件访问
- 异常系统调用

**防御机制**：
- 正则表达式匹配敏感模式
- 静态代码分析
- 沙箱执行验证
- 内容长度/类型检查

### 3.2 卡口二：记忆召回边界标记

**位置**：从长期记忆系统召回信息时
**检查内容**：
- 记忆访问权限验证
- 上下文相关性检查
- 隐私数据保护
- 记忆篡改检测

**防御机制**：
- 访问控制列表（ACL）
- 上下文相似度阈值
- 数据脱敏处理
- 数字签名验证

### 3.3 卡口三：外部技能加载检测

**位置**：加载外部技能/插件时
**检查内容**：
- 技能来源可信度
- 代码完整性验证
- 权限声明审查
- 依赖安全检查

**防御机制**：
- 代码签名验证
- 静态安全扫描
- 权限最小化原则
- 沙箱隔离运行

## 四、威胁模型与防御策略

| 威胁类型 | 可能入口 | 防御卡口 | 具体措施 |
|----------|----------|----------|----------|
| **数据泄露** | 工具输出 | 卡口一 | 敏感信息检测、数据脱敏、访问日志 |
| **代码注入** | 用户输入/工具输出 | 卡口一 | 输入净化、沙箱执行、静态分析 |
| **越权访问** | 记忆系统 | 卡口二 | ACL验证、上下文检查、权限审计 |
| **恶意技能** | 技能加载 | 卡口三 | 代码签名、安全扫描、权限审查 |
| **记忆污染** | 记忆写入 | 卡口二（扩展） | 写入验证、来源追踪、完整性检查 |
| **供应链攻击** | 依赖/插件 | 卡口三 | 依赖扫描、版本验证、漏洞检测 |

## 五、实现架构

### 5.1 系统架构

```
用户输入 → [Agent核心] → 工具调用 → [卡口一：工具输出过滤] → 结果返回
                    ↓
             记忆访问请求 → [卡口二：记忆召回边界标记] → 记忆返回
                    ↓
             技能加载请求 → [卡口三：外部技能加载检测] → 技能加载
```

### 5.2 卡口一实现细节

```python
class ToolOutputFilter:
    """工具输出过滤器"""
    
    def __init__(self):
        self.sensitive_patterns = [
            r'(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[\'"][^\'"]+[\'"]',
            r'(?i)(aws[_-]?access[_-]?key|aws[_-]?secret[_-]?key)',
            r'(?i)(private[_-]?key|ssh[_-]?key|rsa[_-]?key)',
            # 更多敏感模式...
        ]
        self.max_output_size = 10 * 1024 * 1024  # 10MB
        self.sandbox = SandboxExecutor()
    
    def filter(self, tool_name: str, output: str, context: dict) -> FilterResult:
        """过滤工具输出"""
        
        # 1. 大小检查
        if len(output) > self.max_output_size:
            return FilterResult(
                allowed=False,
                reason=f"输出过大: {len(output)} > {self.max_output_size}",
                sanitized_output="[输出被截断：大小超过限制]"
            )
        
        # 2. 敏感信息检测
        sensitive_matches = []
        for pattern in self.sensitive_patterns:
            matches = re.findall(pattern, output)
            if matches:
                sensitive_matches.extend(matches)
        
        if sensitive_matches:
            # 脱敏处理
            sanitized = self.sanitize_sensitive(output, sensitive_matches)
            return FilterResult(
                allowed=True,
                reason="包含敏感信息，已脱敏",
                sanitized_output=sanitized,
                original_size=len(output),
                sensitive_count=len(sensitive_matches)
            )
        
        # 3. 代码/脚本检查
        if self.looks_like_code(output):
            # 沙箱验证
            safe = self.sandbox.validate_safety(tool_name, output)
            if not safe:
                return FilterResult(
                    allowed=False,
                    reason="检测到潜在恶意代码",
                    sanitized_output="[代码执行被阻止]"
                )
        
        return FilterResult(allowed=True, sanitized_output=output)
```

### 5.3 卡口二实现细节

```python
class MemoryRecallGuard:
    """记忆召回守卫"""
    
    def __init__(self):
        self.access_control = AccessControlList()
        self.context_validator = ContextValidator()
        self.privacy_filter = PrivacyFilter()
    
    def guard_recall(self, memory_id: str, query: str, agent_context: dict) -> GuardResult:
        """守卫记忆召回"""
        
        # 1. 访问权限检查
        if not self.access_control.can_access(memory_id, agent_context['agent_id']):
            return GuardResult(
                allowed=False,
                reason="无权访问该记忆",
                sanitized_content=None
            )
        
        # 2. 上下文相关性检查
        memory_metadata = self.get_memory_metadata(memory_id)
        relevance = self.context_validator.calculate_relevance(
            query, memory_metadata, agent_context
        )
        
        if relevance < self.config.min_relevance_threshold:
            return GuardResult(
                allowed=False,
                reason=f"上下文相关性过低: {relevance:.2f} < {self.config.min_relevance_threshold}",
                sanitized_content=None
            )
        
        # 3. 隐私数据过滤
        memory_content = self.load_memory(memory_id)
        sanitized_content = self.privacy_filter.filter_privacy_data(
            memory_content, agent_context['permissions']
        )
        
        return GuardResult(
            allowed=True,
            reason="访问通过",
            sanitized_content=sanitized_content,
            relevance_score=relevance,
            original_size=len(memory_content),
            filtered_count=self.privacy_filter.last_filter_count
        )
```

### 5.4 卡口三实现细节

```python
class SkillLoadDetector:
    """技能加载检测器"""
    
    def __init__(self):
        self.code_scanner = StaticCodeScanner()
        self.signature_verifier = SignatureVerifier()
        self.permission_analyzer = PermissionAnalyzer()
    
    def detect(self, skill_manifest: dict, skill_code: str, source: str) -> DetectionResult:
        """检测技能安全性"""
        
        # 1. 来源可信度检查
        source_trust = self.evaluate_source_trust(source)
        if source_trust < self.config.min_source_trust:
            return DetectionResult(
                allowed=False,
                reason=f"来源可信度过低: {source_trust:.2f} < {self.config.min_source_trust}",
                issues=["不可信来源"]
            )
        
        # 2. 代码签名验证
        if not self.signature_verifier.verify(skill_manifest, skill_code):
            return DetectionResult(
                allowed=False,
                reason="代码签名验证失败",
                issues=["签名无效或缺失"]
            )
        
        # 3. 静态安全扫描
        security_issues = self.code_scanner.scan(skill_code)
        if security_issues:
            return DetectionResult(
                allowed=False,
                reason=f"发现{len(security_issues)}个安全问题",
                issues=security_issues
            )
        
        # 4. 权限声明审查
        declared_perms = skill_manifest.get('permissions', [])
        required_perms = self.permission_analyzer.analyze(skill_code)
        
        # 检查权限最小化
        excess_perms = set(declared_perms) - set(required_perms)
        if excess_perms:
            return DetectionResult(
                allowed=False,
                reason=f"声明了多余权限: {excess_perms}",
                issues=[f"权限过度声明: {excess_perms}"]
            )
        
        # 5. 依赖安全检查
        dependencies = skill_manifest.get('dependencies', {})
        vuln_deps = self.check_dependency_vulnerabilities(dependencies)
        if vuln_deps:
            return DetectionResult(
                allowed=False,
                reason=f"发现依赖漏洞: {vuln_deps}",
                issues=[f"漏洞依赖: {vuln_deps}"]
            )
        
        return DetectionResult(
            allowed=True,
            reason="安全检查通过",
            issues=[],
            source_trust=source_trust,
            required_permissions=list(required_perms)
        )
```

## 六、日志与审计

### 6.1 审计日志格式

```json
{
  "timestamp": "2026-06-01T16:00:00Z",
  "checkpoint": "tool_output_filter",
  "agent_id": "agent_123",
  "tool_name": "shell_executor",
  "decision": "allowed_with_sanitization",
  "reason": "包含敏感信息，已脱敏",
  "original_size": 2048,
  "sanitized_size": 1500,
  "sensitive_patterns_found": ["api_key", "secret_token"],
  "context": {
    "task_id": "task_456",
    "user_id": "user_789"
  }
}
```

### 6.2 监控指标

- **拦截率**：各卡口拦截请求的比例
- **误报率**：正常请求被错误拦截的比例
- **平均处理时间**：每个卡口的平均检查时间
- **威胁类型分布**：检测到的威胁类型统计

## 七、豆包Agent升级项（U128）

### 7.1 升级内容

1. **新增三卡口防御模块**
2. **集成敏感信息检测算法**
3. **实现记忆访问控制**
4. **添加技能安全扫描**
5. **建立完整审计日志系统**

### 7.2 预期效果

- **安全风险降低**：减少数据泄露、代码注入等安全事件
- **合规性提升**：满足数据保护法规要求
- **用户信任增强**：用户更放心使用Agent处理敏感任务
- **运维效率提升**：集中化的安全监控和审计

## 八、性能考虑

1. **异步处理**：安全检查异步执行，不阻塞主流程
2. **缓存优化**：对已验证内容进行缓存，减少重复检查
3. **分级检查**：根据风险等级实施不同深度的检查
4. **资源限制**：设置检查时间和资源上限

## 九、协议版本

- **v1.0** (2026-06-01)：初始版本，基于Hermes v0.15.0 Brainworm Defense设计
- **未来规划**：v2.0将引入机器学习威胁检测

---

> **集成状态**：待集成
> **优先级**：高（安全相关）
> **预计工作量**：3-4人周
> **依赖**：静态代码分析工具、签名验证系统、访问控制框架
