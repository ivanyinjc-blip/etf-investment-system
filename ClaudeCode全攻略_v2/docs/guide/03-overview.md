---
title: "了解 Claude Code 基本组成"
description: "Claude Code界面详解：交互模式、工具集、权限模式、快捷键及Session管理"
---

# 了解 Claude Code 基本组成

在开始第一个任务之前，先花几分钟熟悉 Claude Code 的界面结构和核心概念。这能让你后续使用事半功倍。

---

## 核心界面介绍

Claude Code 的界面根据使用入口不同有所差异，以下以 CLI 界面为例：

### 主要组件

```
┌─────────────────────────────────────────┐
│  [状态栏] Model: Claude 4 Opus  Context: 45K/200K  │
├─────────────────────────────────────────┤
│                                         │
│  [对话区]                                │
│  - User: 你输入的内容                     │
│  - Claude: Claude 的回复和操作            │
│                                         │
├─────────────────────────────────────────┤
│  [工具执行日志]                           │
│  ✓ Read: file.txt (读取成功)             │
│  ✓ Edit: src/app.py (已修改)             │
│  ✓ Bash: git status (输出...)            │
│                                         │
└─────────────────────────────────────────┘
```

### 状态栏信息解读

| 字段 | 含义 |
|------|------|
| `Model` | 当前使用的模型（如 Claude 4 Sonnet / Opus） |
| `Context` | 当前上下文使用量（已用 / 上限） |
| `Tokens` | 本次请求消耗的 Token 数量 |
| `Session` | 当前会话 ID |

---

## 四种交互模式

Claude Code 提供了四种不同的交互模式，适应不同的工作流程：

### 1. Ask 模式（默认）

- **触发**：`claude` 或 `claude ask "你的问题"`
- **特点**：Claude 回答你的问题，可以调用工具执行操作
- **适用**：问答、代码解释、单一任务执行

### 2. Auto 模式

- **触发**：`claude auto` 或在对话中输入 `/auto`
- **特点**：Claude 自动执行多步操作，无需每步确认
- **适用**：批量修改、重构项目、自动化脚本编写
- **注意**：Auto 模式权限较高，请确保操作范围明确

### 3. Browse 模式

- **触发**：`claude browse`
- **特点**：Claude 可以主动浏览网页、点击链接、提取信息
- **适用**：调研市场行情、技术选型对比、查找文档
- **权限**：需要显式授权才能访问网页

### 4. Plan 模式

- **触发**：`claude plan`
- **特点**：Claude 只读探索代码库，生成分析报告或修改计划
- **适用**：理解大型项目结构、安全审查、制定修改方案
- **限制**：不会执行任何修改操作

---

## 工具集详解

Claude Code 的核心能力来自它内置的工具集。以下是所有可用工具：

### Read（读取）

```bash
# 读取单个文件
Read: "src/app.py"

# 读取多个文件
Read: ["src/app.py", "src/utils.py"]

# 读取文件指定范围（行号）
Read: "src/app.py"  # 完整内容
Read: "src/app.py" offset=50 limit=100  # 第50-149行
```

**用途**：读取代码、配置、文档等文件内容。

### Edit（编辑）

```bash
# 精确替换（oldText → newText）
Edit:
  path: "src/app.py"
  oldText: "def hello():\n    print('old')"
  newText: "def hello():\n    print('new')"

# 在指定位置后插入
Edit:
  path: "src/app.py"
  after: "def hello():"
  newText: "    return 'world'"
```

**用途**：修改代码、配置文件、文档。

### Bash（终端命令）

```bash
# 执行命令
Bash: "git status"
Bash: "npm run build"
Bash: "python test.py"

# 执行并获取输出
Bash: "ls -la /path/to/dir"
```

**用途**：运行脚本、执行 git 操作、启动服务、查看文件列表。

### Glob（文件查找）

```bash
# 查找所有 .py 文件
Glob: "**/*.py"

# 查找特定目录
Glob: "src/**/*.ts"

# 查找多个扩展名
Glob: ["**/*.json", "**/*.yaml"]
```

**用途**：快速定位项目中的文件，无需手动浏览目录。

### Grep（内容搜索）

```bash
# 在项目中搜索关键词
Grep: "TODO"
Grep: "function_name"
Grep: "api_key"

# 指定目录
Grep:
  pattern: "TODO"
  path: "src/"

# 正则搜索
Grep:
  pattern: "log.*error"
  path: "src/"
  regex: true
```

**用途**：在代码库中搜索特定字符串、函数名、注释。

### WebFetch（网页抓取）

```bash
# 获取网页内容
WebFetch: "https://docs.anthropic.com/claude-code"
```

**用途**：获取网页文档、技术博客、API 说明等内容。

### MCP（Model Context Protocol）

MCP 是扩展工具集的标准协议，允许 Claude Code 连接外部数据源和工具：

```bash
# 列出已配置的 MCP 服务器
MCP: "list"

# 调用 MCP 工具（示例）
MCP:
  server: "filesystem"
  tool: "read_directory"
  args:
    path: "/workspace"
```

**常见 MCP 场景**：连接数据库、操作 Kubernetes、调用飞书/Notion API 等。

---

## 权限模式详解

Claude Code 有四种权限级别，决定了 Claude 可以执行哪些操作：

| 权限模式 | 说明 | 触发条件 |
|---------|------|---------|
| **Ask** | 默认模式，每次工具调用需用户确认 | `claude` |
| **Auto** | 自动批准安全操作，无需确认 | `claude auto` |
| **Browse** | 允许网页交互（浏览、点击、填表） | `claude browse` |
| **Plan** | 只读模式，禁止任何修改 | `claude plan` |

### Ask 模式权限详情

Ask 模式下，以下操作会**逐个请求确认**：

```
[确认] Read: src/app.py
[确认] Bash: git status
[确认] Edit: src/app.py (将替换 3 行)
[确认] Bash: npm install
```

每次确认前会显示：
- **将要执行的操作**
- **影响的文件/范围**
- **预估结果**

你可以选择：**批准 / 拒绝 / 修改请求 / 全部批准（Auto）**

### Auto 模式权限详情

Auto 模式下，以下安全操作会被**自动批准**：

| 自动批准的操作 | 需要额外确认的操作 |
|-------------|-----------------|
| Read 文件 | 删除文件 |
| Edit（修改） | `rm -rf` 类危险命令 |
| Bash（查看类，如 git status） | 系统级修改 |
| Glob / Grep | 网络请求（curl 等） |
| 创建新文件 | 暴露敏感信息的操作 |

> **Tip**：在 Auto 模式下，如果 Claude 遇到需要额外确认的操作，会主动暂停并询问你。

---

## 快捷键汇总

### CLI 快捷键

| 快捷键 | 功能 |
|-------|------|
| `Ctrl+C` | 取消当前操作 |
| `Ctrl+D` | 退出 Claude Code |
| `Ctrl+L` | 清屏 |
| `↑ / ↓` | 切换历史命令 |
| `Tab` | 自动补全（路径、命令） |
| `Ctrl+Enter` | 发送消息 |

### Claude Code 内部命令

| 命令 | 功能 |
|------|------|
| `/help` | 显示帮助信息 |
| `/tools` | 列出所有可用工具 |
| `/model <name>` | 切换模型（如 opus、sonnet） |
| `/auto` | 切换到 Auto 模式 |
| `/plan` | 切换到 Plan 模式 |
| `/browse` | 切换到 Browse 模式 |
| `/exit` | 退出 Claude Code |
| `/compact` | 压缩当前上下文 |

---

## Session 管理

Claude Code 的 Session（会话）是独立的工作上下文，每次对话都是一个独立的 Session。

### 新建 Session

```bash
# 开始新的空 Session
claude

# 指定 Session 名称
claude --session "feature-login"
```

### 恢复 Session

```bash
# 列出最近 Session
claude sessions list

# 恢复指定 Session
claude --resume <session-id>

# 查看 Session 内容
claude sessions show <session-id>
```

### 压缩上下文（Compact）

当对话变长，上下文快满时：

```bash
# 手动触发压缩
/compact
```

压缩后：
- 较早的对话内容会被总结
- 上下文窗口腾出空间
- 关键信息保留，细节精简

### 清除 Session

```bash
# 清除当前 Session（开始新对话）
/clear

# 删除特定 Session
claude sessions delete <session-id>
```

> **Tip**：建议在开始一个新任务前使用 `/clear`，保持上下文干净，避免历史内容干扰当前任务。

---

## 下一步

现在你已经熟悉了 Claude Code 的基本组成。接下来：

- 🚀 前往 [用 Claude Code 完成第一个任务](./04-first-task.md)，实战演练
- 📖 或者先看 [入口地图：选对适合你的入口](./05-platform.md)，找到最适合自己的使用方式
