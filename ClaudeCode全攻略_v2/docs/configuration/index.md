# 配置与扩展总览

> 资料来源：Anthropic 官方文档 | 更新日期：2026-05-27

---

## 四层配置体系表

Claude Code 采用分层配置设计，从项目规则到安全边界，层层递进。理解这四层，是用好 Claude Code 的前提。

| 层级 | 文件/入口 | 解决什么问题 | 初学者建议 |
|------|----------|-------------|-----------|
| **项目规则** | `AGENTS.md` / `CLAUDE.md` | 理解仓库约定 | 每个重要仓库都写 |
| **本地配置** | `config.toml` | 模型/沙盒/审批/profiles | 先保守再放开 |
| **扩展能力** | Skills / MCP / Subagents | 复用流程/连接外部工具 | 先沉淀高频流程 |
| **安全边界** | Sandbox / Approvals | 管控命令/网络/敏感文件 | 高危操作留人工 |

### 层级详解

#### 第一层：项目规则（AGENTS.md / CLAUDE.md）

放在项目根目录，告诉 Claude Code 这个仓库的「规矩」：

- 目录结构说明
- 代码风格约定
- 常用命令
- 特殊注意事项

```markdown
# 本项目的约定

## 目录结构
- `src/` 源代码
- `tests/` 测试文件

## 代码风格
- 使用 2 空格缩进
- 函数要有 JSDoc 注释

## 常用命令
- `npm test` 运行测试
- `npm run build` 构建
```

#### 第二层：本地配置（config.toml）

用户级别的配置文件，控制模型行为、审批规则、扩展能力。

```toml
# ~/.claude/config.toml 示例
[models]
default = "claude-opus-4-5"

[approval]
default = "ask"  # 默认询问审批

[sandbox]
enabled = true
allow-network = false
```

#### 第三层：扩展能力（Skills / MCP / Subagents）

- **Skills**：可复用的提示词工作流
- **MCP**：Model Context Protocol，连接外部工具（如数据库、API）
- **Subagents**：子任务分解与并行执行

#### 第四层：安全边界（Sandbox / Approvals）

- 沙盒隔离：限制文件访问和网络请求
- 审批规则：精确控制哪些命令需要人工批准

---

## 最小配置路线

### 第一天：立刻能用

```bash
# 1. 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 2. 登录（只需一次）
claude auth

# 3. 进入项目，直接开始
cd ~/my-project
claude
```

**第一天只需知道三件事：**
1. `claude` 启动对话
2. `/help` 查看所有命令
3. `Ctrl+C` 退出

### 第一周：开始用规则

```markdown
<!-- 在重要项目根目录创建 AGENTS.md -->
# 本项目规则

## 必须先写测试
所有新功能必须有对应测试才能提交。

## 提交规范
遵循 Conventional Commits 格式。
```

### 第一个月：按需解锁

| 需求 | 配置动作 |
|------|---------|
| 换更强模型 | `config.toml` 改 `default` 模型 |
| 频繁用某工具 | 写一个 Skill |
| 需要连数据库 | 配置 MCP Server |
| 团队协作 | 设置共享 config + 审批规则 |

---

## 常见误区表

| 误区 | 为什么是坑 | 正确做法 |
|------|----------|---------|
| 只调模型不写上下文 | 模型再强，不知道项目情况也白搭 | 写好 AGENTS.md + 项目描述 |
| 直接放开全部权限 | 等于裸奔，数据泄露风险极高 | 按需开放，高危操作默认审批 |
| 把所有规则塞进提示词 | 提示词越来越长，Claude 容易忽略重点 | 分层：规则文件 + 提示词 + 审批配置 |
| 不用 Sandbox | 任何误操作可能影响真实系统 | 测试环境默认开启沙盒 |
| 忽视 /mcp 命令 | 不知道有哪些可用工具 | 定期 `/mcp list` 查看已连接服务 |

---

## 官方资料延伸

| 资源 | 链接 | 推荐场景 |
|------|------|---------|
| Claude Code 官方文档 | https://code.claude.com/docs/ | 权威配置参考 |
| Claude Code GitHub | https://github.com/anthropics/claude-code | Bug 反馈、功能请求 |
| Anthropic 官网 | https://www.anthropic.com/ | 了解公司和大模型能力 |
| Anthropic API 文档 | https://docs.anthropic.com/ | API 调用和模型参数 |

> **阅读建议**：官方文档更新最频繁，遇到具体配置问题优先查官方。中文资料（包括本文档）会尽量同步，但可能有滞后。

---

## 下一步

- 想了解所有 CLI 命令？→ [CLI 选项与命令参考](./cli-options.md)
- 需要配置安全规则？→ [安全、审批与管理](./security-admin.md)
