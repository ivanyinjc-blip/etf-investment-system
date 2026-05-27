# CLI 选项与命令参考

> 完整命令速查 | 更新日期：2026-05-27

---

## 启动命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `claude` | 启动交互式对话 | `claude` |
| `claude "task"` | 直接执行单次任务 | `claude "帮我修复登录 bug"` |
| `claude -p "query"` | 打印模式，输出结果到 stdout | `claude -p "解释这段代码"` |
| `claude -c` | 启动 Code Companion 模式 | `claude -c` |
| `claude -r` | 恢复上一次中断的会话 | `claude -r` |

### 管道与重定向

```bash
# 读取文件内容传给 Claude
cat error.log | claude -p "分析这个错误"

# 输出到文件
claude -p "写一个 README" > README.md

# 在脚本中使用
#!/bin/bash
claude -p "优化这段 SQL" < input.sql > output.sql
```

---

## 会话命令（斜杠命令）

在对话中直接输入 `/` 开头的命令：

### 基础会话

| 命令 | 功能 | 示例 |
|------|------|------|
| `/help` | 显示所有命令帮助 | `/help` |
| `/clear` | 清除当前会话上下文 | `/clear` |
| `/compact` | 压缩上下文，节省 token | `/compact` |
| `/rewind` | 回退到之前的某个时间点 | `/rewind 3` |
| `/memory` | 查看/编辑记忆内容 | `/memory` |
| `/exit` | 退出 Claude Code | `/exit` |

### 权限与安全

| 命令 | 功能 | 示例 |
|------|------|------|
| `/permissions` | 查看当前权限状态 | `/permissions` |
| `/approve <id>` | 批准待处理的审批 | `/approve abc123` |
| `/reject <id>` | 拒绝待处理的审批 | `/reject abc123` |

### 扩展能力

| 命令 | 功能 | 示例 |
|------|------|------|
| `/skill` | 查看/加载 Skills | `/skill list` |
| `/mcp` | 查看/管理 MCP 服务 | `/mcp list` |
| `/hooks` | 查看/配置钩子 | `/hooks list` |

### Agent 命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `/approve` | 批准当前 Agent 操作 | `/approve` |
| `/reject` | 拒绝当前 Agent 操作 | `/reject` |
| `/undo` | 撤销上一步操作 | `/undo` |

---

## 状态信息命令

| 命令 | 功能 | 返回内容 |
|------|------|---------|
| `/status` | 当前会话状态 | 模型、Token 数量、会话 ID |
| `/model` | 查看/切换模型 | 当前模型名称 |
| `/tokens` | 查看 Token 使用统计 | 本次会话消耗的 tokens |

---

## CLI 选项

启动时通过 `-` 或 `--` 传递的选项：

| 选项 | 说明 | 示例 |
|------|------|------|
| `--model <name>` | 指定使用的模型 | `claude --model claude-opus-4` |
| `--output-format <format>` | 输出格式（json/text/markdown） | `claude -p "..." --output-format json` |
| `--verbose` | 详细输出模式 | `claude --verbose` |
| `--no-stream` | 禁用流式输出 | `claude --no-stream` |
| `--system <prompt>` | 添加系统提示 | `claude --system "你是一个 Rust 专家"` |

### 模型选择建议

| 模型 | 适用场景 |
|------|---------|
| `claude-opus-4-5` | 复杂架构设计、大规模重构 |
| `claude-sonnet-4-7` | 日常开发、平衡速度与能力（**默认推荐**） |
| `claude-haiku-4` | 简单任务、快速查询 |

---

## 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `ANTHROPIC_API_KEY` | API 密钥 | `export ANTHROPIC_API_KEY=sk-...` |
| `ANTHROPIC_BASE_URL` | API 基础地址（自建代理用） | `export ANTHROPIC_BASE_URL=https://api.my-proxy.com` |
| `HTTP_PROXY` | HTTP 代理 | `export HTTP_PROXY=http://127.0.0.1:7890` |
| `HTTPS_PROXY` | HTTPS 代理 | `export HTTPS_PROXY=http://127.0.0.1:7890` |

### 配置位置

```bash
# Shell 配置文件（~/.bashrc / ~/.zshrc）
export ANTHROPIC_API_KEY="sk-xxx"
export ANTHROPIC_BASE_URL="https://api.my-proxy.com"

# 项目本地 .env 文件（不会被提交到 Git）
ANTHROPIC_API_KEY=sk-xxx
```

---

## 完整命令速查表

| 分类 | 命令 | 功能 | 示例 |
|------|------|------|------|
| **启动** | `claude` | 交互式对话 | `claude` |
| **启动** | `claude "task"` | 单次任务 | `claude "修复 bug"` |
| **启动** | `claude -p` | 打印模式 | `claude -p "分析"` |
| **启动** | `claude -c` | Code Companion | `claude -c` |
| **启动** | `claude -r` | 恢复会话 | `claude -r` |
| **会话** | `/help` | 帮助 | `/help` |
| **会话** | `/clear` | 清空上下文 | `/clear` |
| **会话** | `/compact` | 压缩上下文 | `/compact` |
| **会话** | `/rewind` | 回退会话 | `/rewind 5` |
| **会话** | `/exit` | 退出 | `/exit` |
| **状态** | `/status` | 会话状态 | `/status` |
| **状态** | `/model` | 模型信息 | `/model` |
| **状态** | `/tokens` | Token 统计 | `/tokens` |
| **权限** | `/permissions` | 权限状态 | `/permissions` |
| **权限** | `/approve` | 批准操作 | `/approve abc` |
| **权限** | `/reject` | 拒绝操作 | `/reject abc` |
| **扩展** | `/skill` | Skills 管理 | `/skill list` |
| **扩展** | `/mcp` | MCP 管理 | `/mcp list` |
| **扩展** | `/hooks` | 钩子管理 | `/hooks list` |
| **Agent** | `/undo` | 撤销 | `/undo` |

---

## 常见组合用法

### 管道组合

```bash
# 分析代码
cat src/main.rs | claude -p "审查这段 Rust 代码的性能"

# 批量处理
find . -name "*.js" | xargs claude -p "为每个文件添加 JSDoc 注释"

# 错误分析
npm test 2>&1 | claude -p "分析测试失败原因"
```

### 脚本化

```bash
#!/bin/bash
# 自动代码审查脚本
for file in $(git diff --name-only HEAD~1); do
  claude -p "审查 $file 的质量" >> reviews.txt
done
```

```bash
#!/bin/bash
# 批量翻译注释
find src -name "*.py" | while read file; do
  claude -p "把 $file 中的中文注释翻译成英文" > "$file.en"
done
```

### Git 集成

```bash
# 提交信息生成
git diff --cached | claude -p "生成符合 Conventional Commits 的提交信息"

# 自动提交
git add . && claude -p "生成提交信息" | git commit -F -
```

---

## 下一步

- 配置安全规则 → [安全、审批与管理](./security-admin.md)
- 查看官方文档 → [官方资料索引](../reference/index.md)
