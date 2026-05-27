# 安全、审批与管理

> 安全是底线，不是束缚 | 更新日期：2026-05-27

---

## 权限层级

Claude Code 的权限分为三个级别，从严到松：

| 级别 | 说明 | 何时用 |
|------|------|-------|
| **Ask（默认）** | 执行危险操作前必须人工批准 | 所有场景（**推荐默认**） |
| **Auto（分类批准）** | 提前配置好的安全操作自动放行，其余仍需审批 | 信任的操作可预批 |
| **Browse（限浏览器）** | 仅允许浏览器操作，不能执行本地命令 | 需要 Claude 浏览网页时 |

### 查看当前权限

```
/permissions
```

输出示例：
```
当前权限级别: Ask
- git 操作: 需要审批
- 网络请求: 需要审批
- 文件删除: 需要审批
- 只读操作: 自动放行
```

---

## 审批规则配置

在 `config.toml` 中配置 `approve` 和 `reject` 列表：

```toml
[approval]
# 默认行为：询问
default = "ask"

[approval.approve]
# 自动批准的安全操作（白名单）
commands = ["git status", "git diff", "npm test", "cargo build"]
file_patterns = ["*.rs", "*.ts", "*.py"]

[approval.reject]
# 明确拒绝的操作（黑名单）
commands = ["rm -rf /", "drop database", "curl | sh"]
```

### approve vs reject 策略

| 策略 | 适用场景 | 风险 |
|------|---------|------|
| **approve 白名单** | 明确的操作集合 | 更安全，但配置繁琐 |
| **reject 黑名单** | 禁止少数危险操作 | 更灵活，但可能遗漏 |
| **两者结合** | 白名单优先，黑名单兜底 | **推荐** |

---

## 危险操作分类

### 🔴 高危（必须审批）

这些操作默认拦截，必须人工确认：

| 操作 | 危险原因 | 建议处理 |
|------|---------|---------|
| `rm -rf /` 或 `rm -rf <dir>` | 数据永久丢失 | 先 `rm -ri` 模拟，确认后放行 |
| `curl \| sh` 或 `wget \| sh` | 可能执行恶意脚本 | 手动检查脚本来源 |
| 网络请求（直接调用外部 API） | 数据泄露、费用风险 | 使用环境变量，不硬编码 Key |
| 凭据访问（读取 `.env`、AWS keys） | 密钥泄露 | 通过 MCP 读取，不暴露内容 |
| 系统修改（sudo、chmod、修改 /etc） | 影响系统稳定性 | 仅在理解后果后放行 |
| 数据库写入（DELETE、DROP） | 数据不可逆 | 先备份，确认语句正确 |

### 🟡 中危（了解后放行）

了解操作后果后可预批：

| 操作 | 风险 | 放行条件 |
|------|------|---------|
| `git push` | 误推送不可删除的提交 | 确认分支正确、提交内容审查过 |
| `npm publish` | 发布到 npm | 确认版本号、changelog |
| Docker 操作 | 占用资源、镜像污染 | 确认镜像名称和标签 |
| 数据库写入（INSERT、UPDATE） | 数据错误 | 有回滚方案 |
| 部署命令 | 影响生产环境 | 有回滚方案、审批流 |

### 🟢 低危（可自动）

几乎无风险的操作：

| 操作 | 说明 |
|------|------|
| `git status` / `git diff` | 只读，不会修改任何内容 |
| `ls` / `find` / `grep` | 文件查找和搜索 |
| `npm test` / `cargo test` | 运行测试，不会修改代码 |
| 代码格式化（`prettier`、`rustfmt`） | 按规则修改格式 |
| 读取配置文件 | 不涉及写操作 |

---

## 企业合规

### 审计日志

Claude Code 会记录所有操作到日志文件：

```bash
# 查看审计日志
cat ~/.claude/logs/audit.log

# 过滤危险操作
grep -E "(rm|git push|curl)" ~/.claude/logs/audit.log
```

日志格式：
```
[2026-05-27 10:30:15] USER: alice | ACTION: git push | STATUS: APPROVED | DURATION: 2.3s
[2026-05-27 10:31:02] USER: bob | ACTION: rm -rf temp/ | STATUS: REJECTED | REASON: 未确认目录
```

### 操作留痕

| 记录内容 | 用途 |
|---------|------|
| 命令内容 | 审计谁执行了什么 |
| 执行时间 | 定位问题时间线 |
| 审批人 | 责任追溯 |
| 执行结果 | 判断是否成功 |

### 最小权限原则

```
原则：只授予完成任务所需的最小权限

例子：
- 读取 .env 文件 → 只允许通过 MCP，不暴露内容
- git push → 只允许特定分支，不允许 force push
- 网络请求 → 只允许特定域名白名单
```

---

## API Key 安全使用

### ❌ 错误做法

```bash
# 硬编码在命令里
claude "帮我调用 https://api.example.com/secret"

# 写在代码里
const apiKey = "sk-xxx"  # 绝对不要这样做
```

### ✅ 正确做法

**1. 使用环境变量**

```bash
# .env 文件（加入 .gitignore）
ANTHROPIC_API_KEY=sk-xxx
OPENAI_API_KEY=sk-xxx

# 在 Claude Code 中读取
/export API_KEY=`cat .env | grep API_KEY | cut -d= -f2`
```

**2. 通过 MCP 安全读取**

```toml
# config.toml
[mcp.servers.env-reader]
command = "mcp-server-env"
allowed_keys = ["ANTHROPIC_API_KEY", "DATABASE_URL"]
```

**3. 永远不提交到 Git**

```bash
# .gitignore 加入
.env
*.pem
*.key
credentials.json
```

---

## 多用户场景配置建议

### 团队配置文件结构

```
~/.claude/
├── config.toml          # 基础配置（共享）
├── config.team.toml     # 团队配置
└── config.personal.toml # 个人配置（覆盖团队）
```

### 团队配置示例

```toml
# config.team.toml
[approval]
default = "ask"

[approval.approve]
# 所有人都自动批准的安全操作
commands = [
    "git status",
    "git diff",
    "npm test",
    "cargo test",
    "ls",
    "find",
    "grep"
]

[approval.reject]
# 所有人都禁止的操作
commands = [
    "rm -rf /",
    "curl | sh",
    "wget | sh",
    "sudo rm"
]

[audit]
enabled = true
log_path = "/var/log/claude/audit.log"
```

### 个人覆盖

```toml
# config.personal.toml
[models]
default = "claude-opus-4-5"  # 个人偏好使用更强模型

[approval.approve]
# 个人额外的信任操作（需谨慎）
commands = ["cargo build --release"]
```

---

## 安全检查清单

### 每次 Claude Code 上岗前

- [ ] `config.toml` 中 `default = "ask"` 是否设置？
- [ ] 危险命令黑名单是否配置？
- [ ] API Key 是否通过环境变量而非硬编码？
- [ ] `.gitignore` 是否包含敏感文件？
- [ ] 审计日志路径是否正确配置？

### 每次开始危险操作前

- [ ] 确认目标文件/目录路径正确
- [ ] 确认命令没有 typo（特别是 `rm`）
- [ ] 有数据备份吗？
- [ ] 知道如何回滚吗？
- [ ] 是当前分支正确吗？（git 操作）

### 定期检查

- [ ] 审计日志是否有异常？
- [ ] API Key 是否轮换过？
- [ ] 团队新成员是否了解安全规则？
- [ ] `config.toml` 是否有未授权修改？

---

## 下一步

- 查看完整命令 → [CLI 选项与命令参考](./cli-options.md)
- 官方安全文档 → [Anthropic 安全最佳实践](https://docs.anthropic.com/)
