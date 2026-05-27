# Claude Code 全攻略

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/语言-简体中文-green.svg" alt="简体中文">
  <img src="https://img.shields.io/badge/Claude%20Code-v3.5%20Sonnet-orange.svg" alt="Claude Code v3.5">
  <img src="https://img.shields.io/github/stars/superma-ai/ClaudeCodeGuide?style=social" alt="Stars">
</p>

---

> **面向全球初学者、创作者、开发者与团队的 Claude Code 实践指南**

---

## 🎯 What is Claude Code?

Claude Code 是 Anthropic 官方推出的 **AI 原生编程工具**，它将 Claude 的强大能力直接融入你的终端和 IDE，让 AI 辅助编程从"补全建议"升级为**自主执行复杂任务的智能体工作流**。

与传统的 AI 编程助手不同，Claude Code 采用**目标导向**的交互模式：你只需描述要完成的任务，它会自动分析代码库、制定计划、执行修改、运行测试，直到任务完成。

### Why Claude Code instead of Codex?

| 维度 | Claude Code | Codex (OpenAI) |
|------|------------|----------------|
| **开发商** | Anthropic | OpenAI |
| **底层模型** | Claude 3.7 Sonnet | GPT-4.1 / o3 |
| **代码能力** | 超长上下文窗口（200K），深度代码推理 | 强大的代码补全和生成 |
| **生态集成** | IDE / CLI / Desktop / MCP | 主要 API 集成 |
| **安全合规** | 企业级安全与权限控制 | 安全与合规支持 |
| **适用场景** | 复杂多步骤任务、代码库理解、团队协作 | 代码补全、API 驱动开发 |

---

## 🛤️ 四大学习路径

<div align="center">

| 入门路径 | 开发者路径 | 团队路径 | 配置扩展 |
|:--------:|:----------:|:--------:|:--------:|
| 第一次使用 Claude Code？ | 想深度集成到工作流？ | 团队规模化使用？ | 扩展和安全配置？ |
| [→ 开始学习](./docs/guide/00-overview.md) | [→ 工程实践](./docs/guide/06-task-execution.md) | [→ 团队手册](./docs/guide/team-playbook.md) | [→ 配置参考](./docs/guide/11-ide.md) |

</div>

---

## ✨ Key Features

<div align="center">

| <img src="https://img.shields.io/badge/-Desktop%20App-6B7280?style=flat-square" width="110"> | <img src="https://img.shields.io/badge/-CLI%20工具-6B7280?style=flat-square" width="100"> | <img src="https://img.shields.io/badge/-IDE%20集成-6B7280?style=flat-square" width="100"> | <img src="https://img.shields.io/badge/-MCP%20协议-6B7280?style=flat-square" width=100"> | <img src="https://img.shields.io/badge/-安全权限-6B7280?style=flat-square" width=100"> | <img src="https://img.shields.io/badge/-团队协作-6B7280?style=flat-square" width=100"> |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 图形化界面，随时可用 | 终端自由，高效自动化 | VS Code / JetBrains 原生 | 模型上下文协议扩展 | 企业级权限与审计 | 规则沉淀与案例共享 |

</div>

---

## 🚀 Quick Start

### 安装（npm）

```bash
npm install -g @anthropic-ai/claude-code
```

### 首次运行任务

```bash
# 进入你的项目目录
cd your-project

# 用自然语言描述任务
claude "帮我把用户认证模块从 JWT 迁移到 OAuth2.0"

# 或指定更详细的要求
claude --task "修复登录页面的移动端适配问题，要求响应式布局，兼容 iOS Safari" --verbose
```

> 💡 **提示**：首次使用建议从低风险任务开始（如 README 优化、注释补全），熟悉后再处理核心业务逻辑。

---

## 📚 模块总览

| 模块 | 路径 | 说明 |
|------|------|------|
| 🏠 **指南首页** | [docs/](./docs/) | 项目概览与快速入口 |
| 📖 **platform** | [docs/guide/](./docs/guide/) | 核心功能与平台指南 |
| ⚙️ **configuration** | [docs/config/](./docs/config/) | 配置文件、IDE、MCP 扩展 |
| 🧪 **practice** | [docs/practice/](./docs/practice/) | 工程实践方法与案例 |
| 🍳 **recipes** | [docs/recipes/](./docs/recipes/) | 常见场景实战食谱 |
| 📖 **reference** | [docs/reference/](./docs/reference/) | 命令行参数、API 参考 |
| 🤝 **community** | [docs/community/](./docs/community/) | 贡献指南、社区案例 |

---

## 📊 项目指标

<div align="center">

| 18节系统指南 | 13个实战案例 | 4类配置主题 | 3组实践方法 |
|:-----------:|:-----------:|:-----------:|:-----------:|
| 覆盖从入门到团队协作全链路 | 来自真实项目的经验沉淀 | IDE / MCP / 安全 / 权限 | 验证 / 排障 / 贡献 |

</div>

---

## 🤝 Contributing

欢迎贡献！无论是纠正错别字、完善案例还是新增章节，所有提交都会经过审核。

### 如何参与

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add: your feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 **Pull Request**

### 贡献类型

- 🐛 **Bug 修复**：发现文档错误或示例失效
- 📝 **案例补充**：分享你的真实使用案例
- 🌏 **翻译贡献**：帮助翻译为其他语言
- 📖 **内容完善**：补充遗漏的细节或步骤

> 更多细节请阅读 [CONTRIBUTING.md](./docs/community/CONTRIBUTING.md)

---

<div align="center">

**如果你觉得这个项目有帮助，请点一个 ⭐ Star！**

*Built with ❤️ by the superma-ai team · Last updated: 2026-05-27*

</div>
