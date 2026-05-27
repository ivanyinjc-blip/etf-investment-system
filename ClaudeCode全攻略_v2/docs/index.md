---
home: true
heroImage: /hero-claudecode.png
heroText: Claude Code 全攻略
tagline: 面向全球初学者、创作者、开发者与团队的 Claude Code 实践指南
actions:
  - text: 🚀 快速开始
    link: /guide/00-overview
    type: primary
  - text: 📖 学习路径
    link: /guide/01-app-installation
    type: secondary
features:
  - title: 🖥️ Desktop App 入门路径
    details: 通过图形界面零门槛上手，适合初次接触 AI 编程工具的用户。安装即用，快速完成第一个任务闭环。
  - title: 💻 CLI 工程实践
    details: 掌握终端高级用法，集成到 CI/CD 流水线，实现自动化代码审查、批量重构和持续集成。
  - title: 🔌 Skills 与插件
    details: 利用 Claude Code 的 Skills 生态和 MCP 协议扩展，打造属于你自己的自动化工作流。
  - title: 🔒 安全与权限
    details: 企业级安全配置详解——沙盒隔离、审批流程、权限分级、审计日志，让 AI 安全落地。
  - title: 📱 移动协同
    details: 无论身在何处，通过 Desktop App 或 Web 界面随时查看任务进度，保持与团队同步。
  - title: 📋 真实案例库
    details: 来自真实项目的 13+ 实战案例，覆盖前端重构、后端迁移、测试编写、文档生成等常见场景。
  - title: 👥 团队沉淀
    details: 团队规则库、案例库、排障手册，让 AI 编程能力成为组织资产而非个人技巧。
  - title: ⚙️ 配置与排障
    details: IDE 深度集成、MCP 协议配置、常见问题排查清单，遇到问题不再慌。
---

---

## 🛤️ 选择你的学习路径

<div class="path-cards">

### 🌱 第一次使用 Claude Code？

从 Desktop App 开始，零门槛体验 AI 编程的魅力。适合**初学者、个人创作者、产品经理**。

[![开始入门](https://img.shields.io/badge/→%20开始入门-Desktop%20App-1A365D?style=for-the-badge)](./guide/01-app-installation)

---

### 🛠️ 开发者 / 工程化

从 CLI 切入，深度集成到你的开发工作流。适合**前端/后端工程师、DevOps、独立开发者**。

[![工程实践](https://img.shields.io/badge/→%20工程实践-CLI%20+%20IDE-2B6CB0?style=for-the-badge)](./guide/06-task-execution)

---

### 👔 团队负责人 / 技术 Lead

建立团队规则、沉淀案例库、配置安全权限。适合**技术负责人、CTO、工程经理**。

[![团队协作](https://img.shields.io/badge/→%20团队协作-团队手册-2C5282?style=for-the-badge)](./guide/team-playbook)

</div>

---

## 🔄 任务闭环工作流

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  说明   │ →  │  执行   │ →  │  控制   │ →  │  验证   │ →  │  沉淀   │
│ Describe│    │ Execute │    │ Control │    │ Verify  │    │ Archive │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

| 步骤 | 关键词 | 核心问题 |
|:---:|--------|---------|
| **说明** | 目标 · 范围 · 约束 | "我要Claude做什么，边界在哪？" |
| **执行** | 计划 · 改写 · 创建 | "Claude如何实现，需要哪些改动？" |
| **控制** | 审批 · 干预 · 中断 | "关键操作是否需要人工确认？" |
| **验证** | diff · 测试 · 报告 | "改动是否符合预期，有无副作用？" |
| **沉淀** | 规则 · 案例 · 文档 | "这次经验如何固化为团队资产？" |

---

## ⚖️ Claude Code vs Codex

| 维度 | Claude Code | Codex (OpenAI) |
|------|------------|----------------|
| **开发商** | Anthropic | OpenAI |
| **模型** | Claude 3.7 Sonnet (200K 上下文) | GPT-4.1 / o3 |
| **入口** | Desktop App + CLI + IDE | API + 第三方 IDE 集成 |
| **代码理解** | 深度代码库理解，跨文件推理 | 强大的代码生成与补全 |
| **安全合规** | 内置沙盒 + 审批流 + 审计日志 | 企业级安全支持 |
| **适用场景** | 复杂多步骤任务、团队协作、安全要求高的项目 | API 集成、代码补全、简单自动化 |

---

## 📊 项目全景

<div class="metrics-grid">

| 18节系统指南 | 13个实战案例 | 4类配置主题 | 3组实践方法 |
|:-----------:|:-----------:|:-----------:|:-----------:|
| **覆盖从入门到团队协作全链路** | **来自真实项目的经验沉淀** | **IDE/MCP/安全/权限** | **验证/排障/贡献** |

</div>

---

<style>
  /* VuePress 主题覆盖 - 深蓝色系 */
  .theme-container {
    --theme-color: #1A365D;
    --theme-color-lighten: #2B6CB0;
  }

  .path-cards {
    display: flex;
    gap: 1.5rem;
    margin: 2rem 0;
    flex-wrap: wrap;
  }

  .path-cards .feature-item {
    flex: 1;
    min-width: 260px;
    background: linear-gradient(135deg, #1A365D 0%, #2C5282 100%);
    border-radius: 12px;
    padding: 1.5rem;
    color: #fff;
    transition: transform 0.2s ease;
  }

  .path-cards .feature-item:hover {
    transform: translateY(-3px);
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 2rem 0;
  }

  @media (max-width: 768px) {
    .metrics-grid {
      grid-template-columns: repeat(2, 1fr);
    }
    .path-cards {
      flex-direction: column;
    }
  }

  .metrics-grid > div {
    background: #1A365D;
    color: #fff;
    border-radius: 8px;
    padding: 1.25rem;
    text-align: center;
  }

  .metrics-grid > div strong {
    display: block;
    font-size: 1.5rem;
    margin-bottom: 0.25rem;
  }

  .metrics-grid > div span {
    font-size: 0.875rem;
    opacity: 0.85;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
  }

  table th {
    background: #1A365D;
    color: #fff;
    padding: 0.75rem;
    text-align: center;
  }

  table td {
    padding: 0.6rem 0.75rem;
    border-bottom: 1px solid #e2e8f0;
    text-align: center;
  }

  table tr:last-child td {
    border-bottom: none;
  }
</style>
