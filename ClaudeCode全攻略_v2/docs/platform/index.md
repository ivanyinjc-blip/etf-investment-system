---
description: "Claude Code 多端入口详解：VSCode / JetBrains / CLI / Cloud，对比各入口适用场景与选择决策树。"
---

# 入口地图：选对适合你的入口

Claude Code 的能力分散在多个入口中，每个入口有自己的节奏和擅长场景。选对入口，是高效使用 Claude Code 的第一步。

::: tip 最后核对
官方资料最后核对日期：2026-05-27。核心来源：[Anthropic Claude Code 文档](https://code.claude.com/docs/)
:::

## 四大入口一览

| 入口 | 适合场景 | 核心优势 | 劣势 | 推荐指数 |
|------|---------|---------|------|---------|
| **VSCode 插件** | 主力开发、代码解释、inline edit | 原生融合、实时高亮、无缝跳转 | 需 VSCode 环境 | ⭐⭐⭐⭐⭐ |
| **JetBrains** | Java/Kotlin/大型企业项目 | 深度集成、复杂项目支持 | 性能占用较大 | ⭐⭐⭐⭐ |
| **CLI 命令行** | 脚本自动化、Server 环境、最高自由 | 最高控制权、可管道化 | 无图形界面 | ⭐⭐⭐⭐ |
| **Cloud 网页** | 快速试用、多设备同步、零配置 | 打开浏览器即可用 | 功能受限、网络要求 | ⭐⭐⭐ |

## 入口详解

### VSCode 插件（主力入口）

**适用人群**：日常开发者、习惯在编辑器工作的程序员

**核心功能**：
- 侧边栏对话窗口，随时唤起
- Inline Edit：选中代码后直接让 Claude 修改，无需切换窗口
- 代码高亮与跳转：Claude 理解代码结构后直接操作
- 终端集成：命令执行结果直接回到对话
- 多文件编辑：同时修改多个文件保持上下文

**安装方式**：
1. VSCode 扩展市场搜索 "Claude"
2. 安装 Anthropic 官方插件
3. 登录 API Key 或 OAuth

**快捷键**：
| 快捷键 | 功能 |
|--------|------|
| `Cmd/Ctrl + L` | 打开 Claude 对话 |
| `Cmd/Ctrl + Shift + ;` | Inline Edit |
| `Esc` | 停止当前任务 |

---

### JetBrains 全家桶

**适用人群**：Java/Kotlin 大型项目开发者、企业内部工具用户

**支持 IDE**：IntelliJ / PyCharm / WebStorm / GoLand / Rider 等

**安装步骤**：
1. JetBrains 插件市场搜索 "Claude"
2. 安装后重启 IDE
3. 配置 API Key

**与 VSCode 差异**：
- 更深度集成，适合大型单体仓库
- 支持更复杂的项目结构理解
- 企业用户首选

---

### CLI 命令行（最高自由）

**适用人群**：开发者、运维、自动化脚本编写者

**完整命令参考**：

```bash
# 启动
claude                    # 交互模式
claude "解释 main.py"    # 一次性任务
claude -p "修复错误"     # 无会话查询

# 会话管理
claude -c                # 继续上次对话
claude -r                # 恢复历史会话

# 会话内命令
/help                     # 显示所有命令
/clear                    # 清除 context
/compact                  # 压缩历史
/rewind                   # 回退状态
/memory                   # 管理记忆
/permissions              # 权限管理
/status                   # 当前状态

# 选项
claude --model opus       # 指定模型
claude --verbose          # 详细输出
```

---

### Cloud 网页版

**适用人群**：快速试用、不想安装软件、多设备用户

**地址**：code.claude.com

**功能**：浏览器直接使用 Claude Code，无需安装

**限制**：功能相对桌面版有限，适合简单任务

---

## 选择决策树

三个问题快速判断：

```
问题1：你日常在哪个环境工作？
├── VSCode / JetBrains → 用对应插件
├── 纯命令行 / Server → CLI
└── 想快速试用 → Cloud

问题2：任务复杂度如何？
├── 简单小改动 → IDE 插件最方便
├── 复杂多文件修改 → CLI + IDE 配合
└── 自动化脚本 → CLI

问题3：是否需要多工具协同？
├── GitHub/Git → CLI
├── 浏览器自动化 → IDE + MCP
└── 内部系统集成 → CLI + API
```

---

## 多入口协作最佳实践

**推荐模式**：CLI 为主力，IDE 辅助

- **日常开发**：VSCode 插件完成代码解释、局部修改
- **复杂任务**：CLI 开启 session，读取多文件、跑测试
- **自动化**：CLI 脚本化，pipeline 集成
- **快速验证**：Cloud 版临时使用

**Session 共享**：当前不支持跨入口共享 session，但可以在不同入口间切换使用同一个 API Key。
