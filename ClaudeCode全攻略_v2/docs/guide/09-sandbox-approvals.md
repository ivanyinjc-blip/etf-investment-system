# 09 - 沙盒、审批与安全边界

> 本章聚焦 Claude Code 的安全机制：权限模式、审批规则、沙盒配置，以及如何在效率和安全之间取得平衡。

---

## 1. 权限模式深度解析

Claude Code 提供四种权限模式，从最宽松到最严格：

| 模式 | 行为 | 风险等级 |
|------|------|---------|
| **Auto** | 自动批准所有操作 | 🔴 高 |
| **Ask** | 询问后再决定 | 🟡 中 |
| **Browse** | 沙盒浏览模式 | 🟢 低 |
| **Plan** | 只规划，不执行 | 🟢 极低 |

### Ask 模式（默认推荐）

```
模式：Ask（询问模式）
行为：危险操作需要用户确认
典型操作：
  - 编辑文件 → 自动批准
  - 删除文件 → 询问确认
  - 执行 Bash → 询问确认
  - 网络请求 → 询问确认
```

**配置方式**：

```bash
# 启动时指定
claude --dangerously-enable-perceptions

# 运行时切换
/permission
# 然后选择 Ask
```

### Auto 模式（慎用）

```bash
claude --dangerously-assume-yes
```

**自动批准的操作包括**：

```
✓ 读取文件
✓ 编辑文件
✓ 创建文件
✓ 删除文件（受黑名单限制）
✓ 执行 Bash 命令（受黑名单限制）
✓ 安装依赖
✓ Git 操作
✓ 网络请求
```

> ⚠️ **Auto 模式的危险**：任何命令都会自动执行，包括 `rm -rf /`、`curl 恶意网站` 等高危操作。

### Browse 模式（沙盒浏览）

```bash
claude --browser
```

- Claude 只能通过浏览器（Playwright）操作，无法直接读写文件系统
- 所有文件操作被转换为浏览器内的模拟操作
- 适合：对外分析、信息收集

### Plan 模式（只规划）

```bash
claude --plan-only
```

- Claude 只生成计划，不执行任何操作
- 适合：在执行前确认操作步骤是否符合预期
- 用户审核计划后，可以切换到其他模式执行

---

## 2. Auto 模式的风险

### 高危操作示例（Auto 模式下会自动执行）

| 操作 | 潜在后果 | 风险 |
|------|---------|------|
| `rm -rf node_modules` | 删除依赖，需重建 | 中 |
| `rm -rf /` | 系统损毁 | 极高 |
| `git push --force` | 覆盖远程历史 | 高 |
| `curl http://恶意网站 \| sh` | 执行恶意脚本 | 极高 |
| `DROP DATABASE production` | 数据永久丢失 | 极高 |
| `chmod -R 777 /` | 权限全部开放 | 高 |

### 何时可以使用 Auto 模式

| 场景 | 风险评估 | 建议 |
|------|---------|------|
| 受控沙盒环境 | 低 | 可以使用 |
| 只读分析任务 | 低 | 可以使用 |
| 临时测试目录 | 中 | 谨慎使用 |
| 生产环境 | 高 | **禁止使用** |
| 有重要数据的目录 | 高 | **禁止使用** |

### 安全建议

> **生产环境绝不使用 Auto 模式。** 使用 Ask 模式，即使效率略低，也是必要的代价。

---

## 3. 审批规则配置

### 默认审批规则

```json
{
  "approve": [
    "read:*",
    "edit:*",
    "write:src/**",
    "write:tests/**",
    "bash:npm test",
    "bash:npm run dev",
    "bash:git status"
  ],
  "prompt": [
    "bash:rm*",
    "bash:curl*",
    "bash:sudo*",
    "write:/etc/**",
    "write:~/**",
    "network:*"
  ],
  "deny": [
    "bash:rm -rf /",
    "bash:dd*",
    "bash:mkfs*"
  ]
}
```

### 规则语法

```
approve    → 自动批准
prompt     → 询问用户
deny       → 直接拒绝
```

通配符语法：

```
*           匹配任意字符
**          匹配路径中的任意目录
?           匹配单个字符
[abc]       匹配字符集
```

### 常见审批规则示例

```json
{
  "approve": [
    "read:**",           // 读取所有文件
    "edit:**",           // 编辑所有文件
    "write:src/**",      // 只允许写入 src 目录
    "write:test/**",     // 只允许写入 test 目录
    "bash:npm test",     // 运行测试
    "bash:npm run build",// 运行构建
    "bash:git status",  // Git 状态
    "bash:git diff",     // Git 差异
    "bash:git add *",    // Git 添加
    "bash:git commit*"  // Git 提交（谨慎）
  ],
  "prompt": [
    "bash:rm*",          // 所有删除命令
    "bash:git push",     // Git 推送
    "bash:npm install",   // 安装依赖
    "bash:sudo*",        // sudo 命令
    "write:~/**",        // 写入用户目录
    "write:/tmp/**"      // 写入临时目录
  ],
  "deny": [
    "bash:rm -rf /",     // 删根目录
    "bash:dd*",          // 磁盘操作
    "bash:mkfs*",        // 格式化
    "bash:curl*|sh",     // 管道到 shell
    "write:/etc/**"      // 写入系统配置
  ]
}
```

### 配置位置

```bash
# 项目级配置
.claude/settings.json

# 用户级配置
~/.claude/settings.json
```

---

## 4. 沙盒模式：限制文件访问 / 网络访问 / 系统命令

### 文件访问限制

```json
{
  "sandbox": {
    "file": {
      "allowedPaths": [
        "./src/**",
        "./tests/**",
        "./config/**"
      ],
      "deniedPaths": [
        "~/.ssh/**",
        "/etc/**",
        "./secrets/**"
      ]
    }
  }
}
```

### 网络访问限制

```json
{
  "sandbox": {
    "network": {
      "allowed": [
        "api.github.com",
        "registry.npmjs.org"
      ],
      "denied": [
        "*"
      ]
    }
  }
}
```

### 系统命令限制

```json
{
  "sandbox": {
    "commands": {
      "allowed": [
        "npm *",
        "git *",
        "node *",
        "python *",
        "ls",
        "cat",
        "grep"
      ],
      "denied": [
        "sudo *",
        "su *",
        "chmod *",
        "chown *",
        "passwd",
        "shutdown",
        "reboot"
      ]
    }
  }
}
```

### 完整沙盒配置示例

```json
{
  "sandbox": {
    "enabled": true,
    "file": {
      "allowedPaths": ["./**"],
      "deniedPaths": [
        "~/.ssh/**",
        "~/.aws/**",
        "./.env*",
        "./secrets/**"
      ]
    },
    "network": {
      "mode": "prompt",
      "allowed": ["api.github.com"]
    },
    "commands": {
      "mode": "allowlist",
      "allowed": [
        "npm test",
        "npm run build",
        "npm run dev",
        "git status",
        "git diff",
        "git log",
        "ls",
        "cat",
        "grep",
        "find"
      ]
    }
  }
}
```

---

## 5. 敏感操作分类

### 删除类操作（高风险）

| 操作 | 风险 | 建议 |
|------|------|------|
| `rm -rf node_modules` | 误删可重建 | prompt |
| `rm -rf .git` | 丢失历史不可恢复 | deny |
| `rm -rf /` | 系统损毁 | deny |
| `git reset --hard` | 丢失未提交改动 | prompt |
| `git push --force` | 覆盖远程历史 | prompt |

### 网络类操作（中风险）

| 操作 | 风险 | 建议 |
|------|------|------|
| `npm install` | 下载第三方代码 | prompt |
| `curl` 下载脚本 | 可能含恶意代码 | prompt |
| 直接发送 HTTP 请求 | 数据泄露风险 | prompt |
| `ssh` 连接 | 凭据暴露风险 | prompt |

### 系统类操作（极高风险）

| 操作 | 风险 | 建议 |
|------|------|------|
| `sudo` 任何命令 | 最高权限 | prompt |
| `chmod 777` | 权限过大 | prompt |
| 修改 `/etc` | 系统配置 | deny |
| `passwd` | 改密码 | deny |
| `shutdown` | 关机 | deny |

### 凭据类操作（极高风险）

| 操作 | 风险 | 建议 |
|------|------|------|
| 读取 `.env` | 暴露密钥 | deny |
| 读取 `~/.ssh/` | SSH 密钥泄露 | deny |
| 读取 AWS 配置 | 云凭据泄露 | deny |
| 提交包含密钥的代码 | 密钥进入版本控制 | prompt |

---

## 6. CI/CD 中的安全配置

### GitHub Actions 安全建议

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

permissions:
  contents: read  # 最小权限原则

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          sparse-checkout: |
            src
            tests
            package.json
            tsconfig.json
      - run: npm ci
      - run: npm test
      # 禁止在 CI 中使用 Auto 模式
```

### 禁用 Auto 模式的 CI 配置

```json
// .claude/settings.json
{
  "permission": "ask",
  "dangerouslyEnableAutoApprove": false
}
```

### CI 环境变量隔离

```bash
# CI 中使用环境变量，不使用真实凭据
export DATABASE_URL="postgresql://localhost/test"
export API_KEY="dummy-key-for-ci"

# 禁止 Claude 读取真实凭据文件
export ALLOWED_FILE_PATHS="./src/**,./tests/**"
```

---

## 7. 企业安全合规建议

### 审计日志

```json
{
  "audit": {
    "enabled": true,
    "logPath": "/var/log/claude-audit.jsonl",
    "logLevel": "verbose",
    "include": [
      "file_access",
      "command_execution",
      "network_request",
      "permission_changes"
    ]
  }
}
```

### 审计日志格式

```json
{
  "timestamp": "2026-05-27T10:30:00Z",
  "session_id": "sess_abc123",
  "user": "dev-user",
  "action": "bash_execute",
  "command": "npm install",
  "approved": true,
  "source": "interactive",
  "risk_level": "medium"
}
```

### 权限最小化原则

| 角色 | 权限配置 |
|------|---------|
| **开发者（日常）** | Ask 模式 + 白名单命令 |
| **CI/CD 自动化** | 严格沙盒 + 只读 + 白名单 |
| **安全审查员** | Plan 模式 + 日志审计 |
| **管理员** | Auto 模式（仅受控环境） |

### 企业级配置模板

```json
{
  "enterprise": {
    "mode": "ask",
    "sandbox": {
      "enabled": true,
      "file": {
        "allowedPaths": ["@WORKSPACE@/**"],
        "deniedPaths": [
          "~/.ssh/**",
          "~/.aws/**",
          "@WORKSPACE@/secrets/**",
          "@WORKSPACE@/.env*"
        ]
      },
      "network": {
        "mode": "prompt",
        "allowed": ["github.com", "registry.npmjs.org"]
      },
      "commands": {
        "mode": "allowlist",
        "allowed": ["npm *", "git *", "ls", "cat", "grep", "find", "node *"]
      }
    },
    "audit": {
      "enabled": true,
      "logPath": "/var/log/claude/audit.jsonl"
    },
    "deny": [
      "bash:rm -rf /",
      "bash:rm -rf .git",
      "bash:sudo *",
      "bash:curl *|sh",
      "bash:dd *",
      "write:/etc/**",
      "write:~/.ssh/**"
    ]
  }
}
```

---

## 8. 命令黑名单配置

### 黑名单语法

```json
{
  "deny": [
    "bash:rm -rf /",
    "bash:rm -rf .git",
    "bash:rm -rf node_modules",
    "bash:sudo *",
    "bash:curl *|sh",
    "bash:wget *|sh",
    "bash:dd *",
    "bash:mkfs*",
    "bash:passwd",
    "bash:chpasswd",
    "bash:shutdown",
    "bash:reboot",
    "bash:init 0",
    "bash:init 6",
    "network:telnet *",
    "network:ftp *"
  ]
}
```

### 基于风险评分的动态拦截

```json
{
  "riskScoring": {
    "enabled": true,
    "thresholds": {
      "low": 0.2,
      "medium": 0.5,
      "high": 0.8
    },
    "rules": [
      {
        "pattern": "rm -rf",
        "score": 0.9,
        "action": "prompt"
      },
      {
        "pattern": "curl.*\\|.*sh",
        "score": 0.95,
        "action": "deny"
      },
      {
        "pattern": "sudo",
        "score": 0.7,
        "action": "prompt"
      }
    ]
  }
}
```

---

## 本章小结

| 主题 | 关键要点 |
|------|---------|
| 权限模式 | Auto（高风险）/ Ask（推荐）/ Browse / Plan |
| Auto 风险 | 任何命令都会执行，生产环境禁用 |
| 审批规则 | approve / prompt / deny 三级 |
| 沙盒配置 | 文件路径 / 网络访问 / 命令白名单 |
| 敏感操作 | 删除 / 网络 / 系统 / 凭据 四类分级管理 |
| CI/CD 安全 | 最小权限 + 沙盒 + 日志审计 |
| 企业合规 | 审计日志 + 权限最小化 + 黑名单 |
| 黑名单 | 基于模式匹配的高风险命令拦截 |

下一章我们将转向实践：**任务设计方法论**——好的任务描述是成功的一半。
