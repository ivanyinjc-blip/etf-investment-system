---
description: "Claude Code 常见问题与解决方案，涵盖安装、登录、网络、Context、权限、MCP等问题。"
---

# 排障手册：常见问题与恢复路径

::: tip 最后核对
官方资料最后核对日期：2026-05-27
:::

## 排障原则

遇到问题按以下顺序排查：

```
1. 错误信息是什么？（复制完整报错）
2. 最近改了什么配置？（AGENTS.md / config / 环境变量）
3. 这是首次发生还是偶发？（首次 = 配置问题，偶发 = 环境问题）
4. 重启能解决吗？（session 状态问题）
5. 清理后能解决吗？（Context 污染问题）
```

---

## 十大常见问题

### Q1：安装报错 "command not found"

**原因**：PATH 未正确配置

**解决**：
```bash
# 检查是否安装成功
npm list -g @anthropic-ai/claude-code

# 重新安装
npm install -g @anthropic-ai/claude-code

# Linux/macOS 添加 PATH
export PATH="$(npm root -g):$PATH"
```

---

### Q2：登录失败 "API Key 无效"

**原因**：Key 过期 / 格式错误 / 权限不足

**解决**：
```bash
# 检查 Key 格式
echo $ANTHROPIC_API_KEY
# 应该以 sk-ant- 开头

# 重新设置
export ANTHROPIC_API_KEY="your-key-here"

# 验证
claude -p "hello"
```

---

### Q3：网络超时 / 请求失败

**原因**：国内网络限制、代理配置错误

**解决**：
```bash
# 配置代理
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

# 使用 Anthropic 官方代理（部分地区）
export ANTHROPIC_BASE_URL="https://api.anthropic.com"

# 验证网络
curl -s https://api.anthropic.com/v1/models
```

---

### Q4：Context 耗尽 / 响应变慢

**原因**：Context window 填满后性能下降

**解决**：
```bash
# 使用会话内命令
/clear          # 清除 context，重置会话
/compact        # 压缩历史，保留关键上下文

# 预防措施
- 任务间主动 /clear
- 使用 subagent 分离调查任务
- 保持 AGENTS.md < 200 行
- 监控状态栏 tokens 使用量
```

---

### Q5：AGENTS.md 不生效

**原因**：文件位置错误 / 格式错误 / 被覆盖

**解决**：
```
位置优先级（从高到低）：
1. ~/.claude/CLAUDE.md          ← 用户级
2. ./CLAUDE.md                  ← 项目级（根目录）
3. ./CLAUDE.local.md            ← 本地覆盖

检查清单：
□ 文件名完全一致（大小写敏感）
□ 在正确的工作目录启动 claude
□ YAML frontmatter 格式正确
□ 无语法错误（试着用 /memory 确认读取）
```

---

### Q6：权限被拒绝 "Permission denied"

**原因**：危险操作被安全规则拦截

**解决**：
```bash
# 查看当前权限模式
/permissions

# 切换到 Ask 模式（每次询问）
/permissions ask

# 或临时批准单次操作
/approve

# 配置 approve 规则（config.toml）
[security]
allowed_commands = ["git", "npm", "node"]
blocked_commands = ["rm -rf /", "curl /dev"]
```

---

### Q7：MCP 连接失败

**原因**：MCP 服务器未启动 / 配置格式错误

**解决**：
```bash
# 检查 MCP 配置
~/.claude/config.toml

# 正确格式示例
[[mcp]]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem"]

# 测试 MCP 服务器
claude -p "list files in /tmp"

# 常见错误
# 1. command not found → 安装 MCP 服务器
# 2. connection timeout → 检查服务器是否运行
# 3. invalid format → YAML/TOML 格式错误
```

---

### Q8：文件修改后内容不对

**原因**：Codex 基于历史 context 做了额外修改

**解决**：
```bash
# 立即撤销
/undo

# 检查改动
/diff

# 恢复文件
git checkout -- <file>

# 预防：明确禁止事项
# 在任务描述中加入："禁止修改 xxx 文件"
```

---

### Q9：Session 无法恢复

**原因**：Session 过期 / 文件损坏

**解决**：
```bash
# 查看可用 session
ls ~/.claude/sessions/

# 恢复指定 session
claude -r <session-id>

# 清理损坏 session
rm -rf ~/.claude/sessions/<broken-session>

# 新建 session
claude
```

---

### Q10：从 Codex / Cursor 迁移过来不适应

**原因**：操作习惯差异、模型能力差异

**对比与适应**：

| 维度 | Codex | Cursor | Claude Code |
|------|-------|--------|-------------|
| 模型 | GPT-4.1 | GPT-4 | Claude 3.5/3.7 |
| 代码能力 | 强 | 强 | **最强** |
| 安全策略 | 宽松 | 中等 | **最严** |
| MCP 生态 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Context 窗口 | 128K | 200K | **200K** |

**适应建议**：
1. 先把 Codex 的成功任务迁移到 Claude Code 试一遍
2. 注意安全审批流程（Claude Code 更严格）
3. AGENTS.md 语法略有差异，需要迁移调整

---

## 急救锦囊

| 症状 | 急救操作 |
|------|---------|
| 任何异常 | `Esc` 立即停止 → `/clear` → 重试 |
| 死循环 | `Ctrl+C` 强制终止 → `/rewind` |
| Context 污染 | `/compact` 压缩，或 `/clear` 新建 |
| 修改出错 | `/undo` 撤销 → 检查 `/diff` |
| 无法恢复 | `claude` 新建 session |

---

## 获取帮助

1. 查看官方文档：https://code.claude.com/docs/
2. GitHub Issues：https://github.com/anthropics/claude-code/issues
3. Anthropic Discord：官方社区求助
4. 本项目 Issues：提 Bug 或建议
