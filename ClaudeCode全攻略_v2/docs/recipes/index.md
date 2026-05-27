# 实战案例库（13 个场景）

> 真实场景 × 可复制配置 × 开箱即用

---

## 案例概览表

| 类型 | 案例 | 核心场景 | 推荐入口 |
|------|------|----------|----------|
| 内容生产 | PPT Skill / Draw.io MCP / 架构图 | 一句话生成演示/图表 | App/Skills |
| 知识库 | Obsidian / LLM Wiki / Notion | 本地笔记AI化 | CLI/Obsidian |
| 浏览器 | Playwright MCP / Chrome插件 | AI操控网页 | App/MCP |
| 设计协作 | Figma MCP / 飞书CLI | 读设计稿/处理数据 | MCP/CLI |
| 发布运维 | GitHub Actions CI / 远程Bug修复 | 自动修复/远程诊断 | CLI/GitHub |

---

## 13 个案例清单

### 🚀 快速启动类
1. [Claude Code × GitHub Actions：CI 失败自动修复](./01-ci-auto-fix.md) — AI 自动定位根因并修复
2. [Claude Code × Obsidian：本地 AI 知识库](./02-obsidian-codex.md) — 让 AI 读懂你的笔记库
3. [Claude Code × Draw.io MCP：AI 自动绘制架构图](./03-drawio-architecture.md) — 10 分钟生成专业架构图

### 🎨 内容生产类
4. PPT Skill：直接生成可编辑 PPT 文件
5. Draw.io MCP：架构图 / 流程图 / 时序图自动生成
6. 飞书文档：CLI 直接读写飞书文档内容

### 🧠 知识管理类
7. Obsidian Vault：本地笔记 AI 索引与问答
8. LLM Wiki：私有知识库搭建（向量检索）
9. Notion 集成：Notion 数据库与页面的 AI 读写

### 🌐 浏览器与自动化类
10. Playwright MCP：AI 操控浏览器完成复杂操作
11. Chrome 插件：无需命令行，浏览器内直接对话

### 🎨 设计协作类
12. Figma MCP：读取设计稿，自动生成代码片段
13. 飞书 CLI：处理飞书表格数据、批量生成文档

---

## 如何选择先看哪个

按你的目标对号入座：

### 🎯 想先提效日常工作
→ 从 **Obsidian 知识库** 或 **Draw.io 架构图** 开始，5 分钟出成果，建立信心

### 🔧 想提升开发流程质量
→ 先看 **GitHub Actions CI 自动修复**，解决团队高频痛点

### 📊 想做技术汇报或文档
→ **Draw.io 架构图** + **PPT Skill** 组合，产出专业

### 👥 想在团队推广
→ 先通读所有案例，选 1 个试点项目，再参考 **团队 Playbook** 推进

### 🏢 想集成到现有工具链
→ 按类型筛选：
- 知识管理 → Obsidian / Notion / LLM Wiki
- CI/CD → GitHub Actions 自动修复
- 设计 → Figma MCP
- 文档 → 飞书 CLI

---

## 案例贡献指南

### 贡献标准
- ✅ 必须是真实已验证的场景（不是设想）
- ✅ 包含可复制的配置文件或命令
- ✅ 说明适用场景与效果
- ✅ 标注工具版本或环境前提

### 贡献流程
1. 在对应分类目录下新建 `XX-case-name.md`
2. 按下方模板编写内容
3. 更新本文件 index.md 的案例清单
4. 提交 PR 或告知维护者

### 案例模板
```markdown
# Claude Code × [工具名]：[一句话场景描述]

## 背景
> 为什么需要这个场景，解决什么痛点

## 工具栈
- 工具A（版本）
- 工具B（版本）

## 核心步骤
Step 1: ...
Step 2: ...

## 完整配置
\`\`\`yaml
# 配置文件内容
\`\`\`

## 效果与收益
- 节省时间：xxx
- 适用场景：xxx

## 常见问题
Q: ...
A: ...
```

---

> 💡 **提示**：案例持续更新中，欢迎提交你的实战场景！
