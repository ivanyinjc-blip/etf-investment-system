---
title: "桌面 App 下载与安装"
description: "详细指南：如何下载安装 Claude Code桌面应用、登录认证及常见问题排查"
---

# 桌面 App 下载与安装

Claude Code 是 Anthropic 官方推出的命令行辅助工具，支持 macOS、Linux 和 Windows（通过 WSL2）。本文详细介绍从下载到首次启动的完整流程。

---

## 下载地址

Claude Code 桌面应用的官方下载渠道有两个：

| 渠道 | 地址 | 说明 |
|------|------|------|
| Anthropic 官网 | https://www.anthropic.com/claude-code | 首页产品入口 |
| 直接下载 | https://code.claude.com | Claude Code 专用下载站 |

> **Tip**：建议直接访问 `code.claude.com`，下载页面会依据你的操作系统自动推荐对应版本，无需手动选择。

---

## 系统要求

### macOS

- **最低版本**：macOS 13.5 (Ventura) 或更高
- **芯片**：Apple Silicon (M1/M2/M3) 或 Intel
- **内存**：建议 8GB 以上
- **磁盘**：至少 500MB 可用空间

### Linux

- **内核**：Ubuntu 20.04 / Debian 11 及以上，或其他主流发行版
- **架构**：x86_64 或 ARM64
- **依赖**：GLIBC 2.31+
- **内存**：建议 8GB 以上

### Windows

- **方式**：通过 WSL2 安装（不支持原生 Windows）
- **WSL2 要求**：Windows 11 或 Windows 10 2004+
- **发行版**：Ubuntu 20.04+ 推荐
- **注意**：Windows 原生版尚在规划中，当前请使用 WSL2

---

## 安装步骤

### macOS 安装

1. 访问 https://code.claude.com 下载 `.dmg` 安装包
2. 双击打开 `.dmg` 文件
3. 将 **Claude Code.app** 拖入 `应用程序` 文件夹
4. 首次启动时，右键点击应用 → **打开**（绕过 Gatekeeper 警告）
5. 终端会自动引导登录流程

### Linux 安装

**方式一：APT 安装（推荐 Ubuntu/Debian）**

```bash
# 添加 Anthropic 官方仓库
curl -fsSL https://downloads.anthropic.com/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/anthropic-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/anthropic-archive-keyring.gpg] https://downloads.anthropic.com/debian stable main" | sudo tee /etc/apt/sources.list.d/anthropic.list

# 安装
sudo apt update && sudo apt install claude-code
```

**方式二：RPM 安装（Fedora/RHEL）**

```bash
sudo rpm --import https://downloads.anthropic.com/rpm/gpg
echo "[anthropic]
name=Anthropic
baseurl=https://downloads.anthropic.com/rpm
enabled=1
gpgcheck=1
gpgkey=https://downloads.anthropic.com/rpm/gpg" | sudo tee /etc/yum.repos.d/anthropic.repo

sudo dnf install claude-code
```

**方式三：独立二进制（通用）**

```bash
# 下载最新版本
curl -fsSL https://downloads.anthropic.com/claude-code/latest/linux-x86_64.tar.gz -o claude-code.tar.gz

# 解压到指定目录
sudo tar -xzf claude-code.tar.gz -C /usr/local/bin --strip-components=1

# 验证安装
claude --version
```

### Windows (WSL2) 安装

```bash
# 在 WSL2 终端内执行
curl -fsSL https://downloads.anthropic.com/claude-code/latest/linux-x86_64.tar.gz -o claude-code.tar.gz
sudo tar -xzf claude-code.tar.gz -C /usr/local/bin --strip-components=1
```

> **Tip**：确保 Windows 主机已安装 Claude Code Desktop 客户端（从 Microsoft Store 或官网下载），WSL2 内的 CLI 会自动与桌面客户端通信。

---

## 登录与认证

Claude Code 支持两种认证方式：**OAuth（推荐）** 和 **API Key**。

### 方式一：OAuth 登录（交互式）

```bash
claude
```

首次启动会自动打开浏览器，引导你用 Anthropic 账号授权。授权成功后，CLI 会自动获取会话凭证，**无需手动复制 Token**。

### 方式二：API Key 认证

如果你有 Anthropic API Key，可以手动配置：

```bash
# 设置环境变量（临时生效）
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"

# 或者持久化写入配置文件
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"' >> ~/.bashrc
source ~/.bashrc
```

> **注意**：API Key 认证适用于服务器/自动化场景，OAuth 认证会自动管理 Token 刷新，体验更流畅。

---

## 首次启动检查清单

运行以下命令，确认安装完全正常：

```bash
# 1. 检查版本（确认安装成功）
claude --version

# 2. 检查认证状态
claude auth status

# 3. 测试基本交互
claude
# 输入：你好，请确认Claude Code已正常连接
# 预期：Claude Code 应能正常回复

# 4. 检查工具集是否可用
# 在 Claude Code 对话中输入：
/tools
# 应列出所有可用工具（Read/Edit/Bash/Glob/Grep等）
```

---

## 常见安装问题

### 1. macOS 提示"无法打开，因为来着未知开发者"

```
问题：Gatekeeper 阻止了非 App Store 应用
解决：右键点击 .dmg → 选择"打开" → 确认提示框中选择"打开"
```

### 2. Linux 安装后找不到命令

```bash
# 检查 PATH 是否包含 /usr/local/bin
echo $PATH

# 手动确认可执行文件位置
which claude
ls -la /usr/local/bin/claude

# 若权限不足
chmod +x /usr/local/bin/claude
```

### 3. WSL2 下无法启动 GUI 授权页面

```bash
# 确保 DISPLAY 变量正确（Windows 端需安装 XServer 如 VcXsrv）
export DISPLAY=:0

# 或者使用 Windows 主机 IP
export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0
```

### 4. 防火墙/代理导致网络不通

```bash
# 检查能否访问 Anthropic API
curl -s https://api.anthropic.com/v1/models | head -20

# 若使用代理
export HTTPS_PROXY="http://127.0.0.1:7890"
export HTTP_PROXY="http://127.0.0.1:7890"

# 或者在配置文件中设置
mkdir -p ~/.config/claude-code
echo 'proxy: "http://127.0.0.1:7890"' >> ~/.config/claude-code/config.json
```

### 5. 权限被拒绝（Permission Denied）

```bash
# 检查安装目录权限
ls -la /usr/local/bin/claude

# 修复权限
sudo chown $(whoami):$(whoami) /usr/local/bin/claude
sudo chmod +x /usr/local/bin/claude
```

### 6. 版本过旧

```bash
# macOS
brew upgrade claude-code

# Linux APT
sudo apt update && sudo apt upgrade claude-code

# Linux 独立二进制
curl -fsSL https://downloads.anthropic.com/claude-code/latest/linux-x86_64.tar.gz -o claude-code.tar.gz
sudo tar -xzf claude-code.tar.gz -C /usr/local/bin --strip-components=1
```

---

## 下一步

安装完成后，你可以：

- 📖 继续阅读 [订阅 Plus / Pro / Team](./02-subscribe.md)，解锁更多功能
- 🔍 前往 [了解 Claude Code 基本组成](./03-overview.md)，熟悉界面与工具
- 🚀 直接跳到 [用 Claude Code 完成第一个任务](./04-first-task.md)，开始你的第一个任务
