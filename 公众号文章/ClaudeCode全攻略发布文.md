# Claude Code 全攻略正式发布：可能是最系统的中文实战指南

> 耗时两周，我把 Claude Code 从入门到团队落地，拆成了 16 节系统课 + 13 个案例库。

---

## 先说个真实经历

上周有个朋友问我："超哥，AI 编程工具现在到底用哪个好？Codex 还是 Claude Code？"

我说 Claude Code 代码能力强，Anthropic 的安全合规也更适合企业场景。

他说："我知道这东西好，但网上全是英文文档，装完不知道从哪开始，好不容易跑起来一个任务也不知道对不对。"

这句话让我决定做一件事——

**把 Claude Code 的中文实战指南，当成一个完整产品来打磨。**

两周后，《Claude Code 全攻略》正式发布。

---

## 这份全攻略解决什么问题？

Codex 火了，Claude Code 其实更强，但中文资料几乎为零。

这份全攻略解决三个核心问题：

**1. 怎么开始？**

安装、订阅、登录，第一个任务怎么跑通——手把手带，没有任何门槛。

**2. 怎么用好？**

任务描述、验证方式、Context 管理、MCP 集成——不是命令速查，是真实工作流。

**3. 怎么沉淀成团队资产？**

AGENTS.md 规范、团队 playbook、案例库——一个人用得好是技巧，团队都用好才是能力。

---

## 16 节系统指南，覆盖四个阶段

全攻略按"认识入口 → 跑通任务 → 建立方法 → 团队沉淀"四层组织。

### 阶段一：入门（跑通第一个闭环）

从安装到第一个任务，四步跑完整条链路：

- **01 桌面 App 下载安装** — 零门槛，图形界面，装完即用
- **02 订阅 Plus / Pro / Team 怎么选** — 方案对比，国内订阅避坑
- **03 基本组成** — 工具集 / 四种交互模式 / 权限体系 / Session 管理
- **04 完成第一个任务** — 目标 → 执行 → 验证 → 交付，四步闭环

### 阶段二：进阶（形成稳定方法）

能不能用好，关键在这一阶段：

- **05 入口地图** — VSCode / JetBrains / CLI / Cloud 怎么选
- **06 任务执行机制** — Agent 循环 / 小步修改 / Session 恢复
- **07 验证方式与结果检查** — 测试 / 构建 / 截图 / 日志四种验证
- **08 AGENTS.md 配置** — 项目级持久化指令，与 OpenClaw CLAUDE.md 的区别
- **09 沙盒、审批与安全边界** — 企业合规必备，危险操作分级管控

### 阶段三：工程化（进入真实项目）

- **10 排障手册** — 十大常见问题 + 急救锦囊，遇到问题不慌

### 阶段四：团队化（沉淀为组织能力）

- **任务设计方法论** — 五要素模板，好任务描述决定成败
- **团队落地 playbook** — 三阶段推广路径（个人试点 → 项目推广 → 团队复制）

---

## 13 个实战案例，有手就能复现

案例清单已规划 13 个，首批完整实现 4 个：

| 案例 | 场景 | 可直接用 |
|------|------|---------|
| **CI 失败自动修复** | GitHub Actions 失败 → Claude 自动读代码 → 修复 → 开 PR | ✅ 完整 YAML |
| **Obsidian 知识库** | 本地笔记库 AI 化，自然语言查询和生成 | ✅ 配置示例 |
| **Draw.io 架构图** | Claude 读代码 → 自动生成架构图 XML | ✅ MCP 配置 |
| **Notion MCP** | 打通 Notion 知识空间，AI 管理笔记 | ✅ Token 配置 |

**完整 13 个案例清单**（含 PPT Skill、Figma MCP、飞书 CLI、远程 Bug 修复等）已列入 roadmap，持续更新中。

---

## CI 自动修复：重点案例详解

这是我觉得最有价值的案例之一。

**传统链路**：收到通知 → 打开日志 → 定位代码 → 修复 → 提交 → 等 CI 重跑 → 确认通过 → 开 PR

**Claude Code 链路**：CI 失败 → 自动触发 Claude → 读代码 → 修复 → 开 PR → 等你合并

全程不需要你介入。GitHub Actions 配置直接复制使用：

```yaml
name: Claude Code Auto-Fix on Failure
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
jobs:
  auto-fix:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_sha }}
      - name: Run Claude Code
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code
          claude "读取代码，运行测试，找到导致失败的最小改动，修复它。"
      - name: Create PR
        if: success()
        uses: peter-evans/create-pull-request@v6
```

---

## 为什么 Claude Code 值得学？

很多人问 Codex 和 Claude Code 到底用哪个。

我的判断标准：

| 维度 | Claude Code | Codex |
|------|------------|-------|
| 代码生成能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 安全合规性 | ⭐⭐⭐⭐⭐（Anthropic 企业策略） | ⭐⭐⭐ |
| 企业场景适配 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| MCP 生态 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 中文资料 | ❌ 几乎为零（这是空白） | 已有 CodexGuide |

如果你在企业环境，Claude Code 是更稳妥的选择——Anthropic 的安全策略、数据合规、审计能力都更强。

---

## 怎么使用这份全攻略？

**第一次接触 Claude Code：**

从入门四步开始（安装 → 订阅 → 认识界面 → 第一个任务），约 2 小时跑通完整闭环。

**已经有基础，想深入工程化：**

重点看任务执行机制 + 验证方式 + AGENTS.md + 安全配置，这是拉开效率差距的关键。

**团队想推广：**

先看团队落地 playbook，按三阶段路径走（个人提效 → 项目试点 → 团队推广）。

---

## 获取全攻略

文档完全开源，免费使用。

**本地备份**：`/mnt/e/OneDrive/superma output/知识库/ClaudeCode全攻略_v2/`

**包含内容**：16 节系统指南 + 13 个案例清单 + 完整配置示例，可直接下载使用。

---

## 最后说几句

做这份全攻略的过程中，我反复提醒自己一件事——

> **完成比完美重要。**

文档一定有不足，案例一定有遗漏。但只要它能帮一个人少走一个弯路，这两周就没白花。

如果你觉得有用，转发给你身边在用或者想用 Claude Code 的人。

下篇见。

---

*阿超 AI · 公众号「阿超AI」*
*觉得有用？点个在看支持一下*
