---
description: "Claude Code × Notion MCP：打通 Notion 知识空间，实现双向同步与 AI 内容生成。"
---

# Claude Code × Notion MCP：打通知识空间

## 场景

想把 Claude Code 变成你的 Notion 助理——用自然语言管理笔记、生成内容、自动整理知识库。

## 工具栈

- Claude Code CLI
- Notion MCP Server
- Notion API（需要 Integration Token）

## 核心步骤

### Step 1：创建 Notion Integration

1. 打开 [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. 点击 "New integration"
3. 填写名称，选择对应 Workspace
4. 复制生成的 Internal Integration Token

### Step 2：安装 Notion MCP

```bash
# 使用 npm 安装
npm install -g @modelcontextprotocol/server-notion

# 配置 MCP（~/.claude/config.toml）
[[mcp]]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-notion"]

# 设置 API Key
export NOTION_API_KEY="secret_xxxxxxx"
```

### Step 3：在 Notion 中启用集成

1. 打开你想让 Claude 访问的 Page
2. 点击右上角 `...` → `Add connections`
3. 搜索并添加你的 Integration

### Step 4：开始使用

```bash
# 启动 Claude Code
claude

# 示例任务
"搜索我 Notion 中所有包含'项目计划'的页面"
"帮我总结这个页面的核心内容"
"在这个页面下创建一个新的笔记"
"更新页面状态为已完成"
```

## MCP 配置示例

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "secret_xxxx"
      }
    }
  }
}
```

## 效果

- 自然语言管理 Notion 内容
- AI 批量整理知识库
- 自动生成摘要和标签
- 与 Obsidian 等本地笔记工具配合使用

## 适用场景

个人知识管理 / 团队 Wiki / 内容创作 / 项目跟踪
