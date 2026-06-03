【Trae提炼】2026-04-30 | 原文件完整路径：E:\龙虾AI主控中心\supabase_connection_test.py

# Supabase 共享知识库写入测试报告（脱敏）

## 1) 目标

- 学习 Supabase + PostgreSQL 三方日志同步方法
- 检查 Supabase 环境变量是否就绪
- 在“合规门禁允许”的前提下执行测试写入（写入→读取→删除回滚）

## 2) 当前脚本与依赖

- 测试脚本：E:\龙虾AI主控中心\supabase_connection_test.py  
- 依赖：psycopg、python-dotenv、supabase（python SDK）
- 连接模型：同时使用 Postgres 直连（建表）+ PostgREST（写读删）

## 3) 环境变量检查结果（仅 SET/EMPTY，不回显任何值）

本机当前状态：全部为空，无法执行写入测试。

- SUPABASE_URL=EMPTY
- SUPABASE_SERVICE_ROLE_KEY=EMPTY
- SUPABASE_DB_PASSWORD=EMPTY
- SUPABASE_ANON_KEY=EMPTY

## 4) 合规门禁说明（必须先对齐）

- 该脚本默认把 DB Host 推导为 `db.<project_ref>.supabase.co` 并使用 `sslmode=require`，属于“外部云端服务直连”形态。  
- 若你的体系规则要求“严格本地/离线、禁止云端付费 API”，则需要先改为：
  - 自建/内网 Supabase（或仅自建 Postgres），并把 URL 指向内网地址
  - 或者由你显式开门禁允许本次测试联通外部（建议仅临时、仅测试窗口）

## 5) 可执行的最小验收方案（你手动执行）

### A) 仅做就绪校验（安全）

- 在系统环境变量中设置好 3 个必需项（URL、Service Role Key、DB Password），再运行脚本。  
- 脚本自身不会打印密钥明文，但会打印写入的测试行内容（不含敏感值）。

### B) 写入测试（写→读→删）

```powershell
python E:\龙虾AI主控中心\supabase_connection_test.py
```

验收通过口径（脱敏）：
- 控制台出现 `supabase_connection_test result (redacted)`  
- inserted_row / selected_data 能读取到测试行  
- verify_after_delete 为空（表示删除回滚成功）

