---
title: 学习路线总览
description: Claude Code 全攻略学习路线图 — 从零基础到团队协作的完整路径规划
---

# 🛤️ Claude Code 学习路线

---

## 📌 Global Understanding

**Claude Code** 是 Anthropic 推出的 **AI Agent 编程工具**，它将 Claude 的智能体能力直接带入软件工程工作流。

与传统的 AI 编程助手不同，Claude Code 采用**目标导向**的交互范式：

> **你描述目标，Claude Code 自动完成：分析 → 计划 → 执行 → 验证 → 交付**

它的核心优势在于：
- 🔁 **完整闭环**：从任务说明到交付物，不只是建议，而是执行
- 🧠 **深度理解**：200K 上下文窗口，能理解整个代码库
- 🔒 **安全可控**：沙盒隔离 + 审批流程 + 审计日志
- 🤝 **团队友好**：规则沉淀、案例共享、MCP 扩展

---

## 📊 四阶段学习路线

| 阶段 | 🎯 目标 | 📚 推荐页面 | ✅ 验收标准 |
|:----:|---------|------------|------------|
| **入门** | 跑通低风险任务，理解基本工作流 | [01-app-installation](./01-app-installation) · [02-subscribe](./02-subscribe) · [03-overview](./03-overview) · [05-first-task](./05-first-task) | ✅ 完成一次完整闭环（说明→执行→验证→交付） |
| **进阶** | 形成稳定的任务描述与验证方法 | [04-platform](./04-platform) · [06-task-execution](./06-task-execution) · [07-verification](./07-verification) | ✅ 每次任务都能写清：目标 / 范围 / 验证标准 / 交付物 |
| **工程化** | 进入真实项目，掌握风险控制 | [08-agents-md](./08-agents-md) · [09-sandbox-approvals](./09-sandbox-approvals) · [10-troubleshooting](./10-troubleshooting) | ✅ 每次改动有：diff / 测试 / 风险说明 |
| **团队化** | 沉淀团队规则和案例库 | [11-ide](./11-ide) · [team-playbook](../team/team-playbook.md) | ✅ 项目有：规则 / 案例 / 排障手册 / 贡献路径 |

---

## 👤 三类用户路径

### 🌱 新手 — 从 App 开始

> **推荐从 Desktop App 入手**，图形界面降低学习曲线，先建立对 Claude Code 的直观认知。

| 步骤 | 内容 | 页面 |
|:----:|------|------|
| 1 | 安装 Desktop App | [01-app-installation](./01-app-installation) |
| 2 | 注册与订阅方案选择 | [02-subscribe](./02-subscribe) |
| 3 | 界面与核心概念一览 | [03-overview](./03-overview) |
| 4 | 完成第一个低风险任务 | [05-first-task](./05-first-task) |
| 5 | 学习结果验证与检查 | [07-verification](./07-verification) |

---

### 🛠️ 开发者 — 从 CLI 开始

> **直接切入命令行**，深度集成到你的开发工作流，适合已有编程基础的用户。

| 步骤 | 内容 | 页面 |
|:----:|------|------|
| 1 | CLI 安装与环境配置 | [01-app-installation](./01-app-installation) |
| 2 | 订阅方案与 API 密钥 | [02-subscribe](./02-subscribe) |
| 3 | 平台架构与核心概念 | [04-platform](./04-platform) |
| 4 | 任务执行核心方法 | [06-task-execution](./06-task-execution) |
| 5 | agents.md 多智能体协作 | [08-agents-md](./08-agents-md) |
| 6 | 沙盒与审批流 | [09-sandbox-approvals](./09-sandbox-approvals) |
| 7 | 排障与错误处理 | [10-troubleshooting](./10-troubleshooting) |
| 8 | IDE 深度集成 | [11-ide](./11-ide) |

---

### 👔 非开发者 / 团队负责人

> **聚焦配置与协作**，理解如何为团队建立规范，而非亲自操作代码。

| 步骤 | 内容 | 页面 |
|:----:|------|------|
| 1 | Claude Code 能做什么 | [03-overview](./03-overview) |
| 2 | 平台架构与权限模型 | [04-platform](./04-platform) |
| 3 | 安全与权限配置 | [09-sandbox-approvals](./09-sandbox-approvals) |
| 4 | 团队手册与规则沉淀 | [team-playbook](../team/team-playbook.md) |
| 5 | 案例库与最佳实践 | [../practice/](../practice/) |

---

## 📈 学习路径图

```
新手路径                          开发者路径                        团队路径
─────────                         ─────────                        ────────
App 安装                           CLI 安装                          平台架构
  ↓                                 ↓                                ↓
订阅配置                           订阅配置                          权限模型
  ↓                                 ↓                                ↓
界面概览              →            任务执行             →            安全配置
  ↓                         ↗            ↓                         ↓
第一个任务             进阶       agents.md              团队化      规则沉淀
  ↓                   ↗   ↘           ↓                         ↓
验证检查                      沙盒+审批           排障                案例库
```

---

## ⚠️ 重要提示

> 🔔 **核对日期**：本文档最后更新于 **2026-05-27**，请确认你阅读的是最新版本。

---

## 📍 下一步

<div class="next-steps">

| 你是谁？ | 推荐下一步 |
|---------|-----------|
| 🌱 第一次使用 | [01 - Desktop App 安装指南](./01-app-installation) |
| 🛠️ 开发者，想用 CLI | [01 - CLI 安装与环境配置](./01-app-installation) |
| 👔 团队负责人 | [04 - 平台架构与权限模型](./04-platform) |

</div>

---

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
    font-size: 0.95rem;
  }

  table th {
    background: #1A365D;
    color: #fff;
    padding: 0.85rem;
    text-align: left;
  }

  table td {
    padding: 0.75rem;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
  }

  table tr:last-child td {
    border-bottom: none;
  }

  table tr:hover td {
    background: #f7fafc;
  }

  .next-steps {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
  }

  .next-steps > div {
    flex: 1;
    min-width: 200px;
    background: #edf2f7;
    border-left: 4px solid #1A365D;
    padding: 1rem;
    border-radius: 0 6px 6px 0;
  }

  .next-steps > div strong {
    color: #1A365D;
  }
</style>
