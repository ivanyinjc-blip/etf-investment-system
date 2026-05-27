# Claude Code × GitHub Actions：CI 失败自动修复实测

> 每次 CI 失败不再需要人工排查，Claude 自动定位根因并修复，周期从「天」缩短到「分钟」

---

## 背景：传统 CI 失败的痛点

```
CI 失败 → 开发者收到通知 → 本地复现 → 读日志 → 定位问题 → 修复 → 提交 → 等 CI 重跑
        ↑
        平均耗时 2-4 小时，频繁失败时团队士气低、迭代慢
```

**核心问题**：
- 人工排查日志成本高
- 环境差异导致本地无法复现
- 低级错误（拼写、类型、依赖）反复出现
- 深夜/节假日无人响应

---

## 核心流程

```
CI 失败触发
    ↓
自动触发 Claude Code（通过 workflow_run 事件）
    ↓
Claude 读取失败日志 + 代码 → 定位根因
    ↓
Claude 修复代码（最小改动原则）
    ↓
Claude 提交 PR（包含修复说明）
    ↓
团队人工 Review + 合并
```

---

## 完整 GitHub Actions 配置

**文件路径**：`.github/workflows/claude-auto-fix.yml`

```yaml
name: Claude Code Auto-Fix on Failure

on:
  workflow_run:
    workflows: ["CI"]          # 监听名为 "CI" 的 workflow
    types: [completed]

permissions:
  contents: write              # 允许写代码（提交修复）
  pull-requests: write         # 允许创建 PR

jobs:
  auto-fix:
    # 仅在原 workflow 失败时执行
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest

    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

    steps:
      # 1. 拉取失败那次提交对应的代码
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_sha }}
          fetch-depth: 0

      # 2. 安装 Claude Code CLI
      - name: Install Claude Code
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code

      # 3. 运行 Claude 自动修复
      # 可根据项目类型自定义提示词
      - name: Run Claude Code
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          CLAUDE_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude "这是一个 Node.js 项目。请读取失败日志（位于 $GITHUB_WORKSPACE），找到测试失败的根本原因，定位到具体代码文件，做最小改动修复，然后提交。"

      # 4. 验证修复是否通过
      - name: Verify Fix
        run: |
          npm install
          npm test

      # 5. 自动创建 PR
      - name: Create Pull Request
        if: success()
        uses: peter-evans/create-pull-request@v6
        with:
          title: "🤖 Claude Code 自动修复：${{ github.event.workflow_run.name }}"
          body: |
            ## 自动修复报告

            由 Claude Code 自动检测并修复。

            - 原 CI workflow：[#${{ github.run_id }}](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }})
            - 修复时间：$(date -u '+%Y-%m-%d %H:%M UTC')

            请人工 Review 后合并。
          branch: claude-auto-fix/${{ github.run_id }}
          delete-branch: true
```

---

## 关键配置说明

### 触发过滤
```yaml
on:
  workflow_run:
    workflows: ["CI"]      # 精确匹配 workflow 名称
    types: [completed]      # 仅在完成时触发
```
- 只监听名为 `CI` 的 workflow（改为你的实际 workflow 名）
- `completed` + `conclusion == 'failure'` 双重保障，避免误触发

### 权限配置
| 权限 | 用途 |
|------|------|
| `contents: write` | 克隆代码、提交修复 commit |
| `pull-requests: write` | 创建 Pull Request |

### 环境变量
```yaml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```
- 必须在 GitHub 仓库 Settings → Secrets 中添加 `ANTHROPIC_API_KEY`
- API Key 需要有足够的 API 调用额度

### 触发workflow示例（被监听的CI workflow）
```yaml
# .github/workflows/ci.yml（被监听的原始 CI）
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install && npm test
```

---

## 适用场景

### ✅ 非常适合
- 频繁有 CI 失败的团队（尤其是开源项目）
- 需要 24/7 无人值守保障的 CI 环境
- Node.js / Python / Go / Java 等主流语言项目
- 追求快速迭代、缩短修复周期的开发团队

### ⚠️ 注意事项
- 修复仅做**最小改动**，复杂逻辑问题仍需人工介入
- 需确保 `ANTHROPIC_API_KEY` 额度充足
- 建议配合标签（label）过滤，只对特定标签的 PR 触发自动修复
- 代码安全敏感的团队，建议先做人工 Review 再合并

---

## 效果与收益

| 指标 | 传统方式 | Claude 自动修复 |
|------|---------|---------------|
| 平均修复时间 | 2-4 小时 | 5-15 分钟 |
| 人工介入次数 | 每次失败都需要 | 仅 Review + 合并 |
| 深夜响应 | ❌ 无人 | ✅ 自动触发 |
| 重复低级错误 | 反复出现 | AI 一次学会根因 |

---

## 进阶配置

### 按文件路径过滤（减少误触发）
```yaml
- name: Run Claude Code
  env:
    CLAUDE_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    claude "请查看最近修改的文件，只修复与测试失败相关的代码，不需要全量扫描。"
```

### 多语言项目适配
```yaml
# Python 项目
- run: pip install -r requirements.txt && pytest

# Go 项目
- run: go mod download && go test ./...

# Java 项目
- run: mvn test
```

---

## 常见问题

**Q: API Key 额度用完了怎么办？**
A: 在 GitHub Secrets 中设置用量告警，或切换到 Claude Max 订阅计划。

**Q: Claude 修复错了怎么办？**
A: PR 需要人工 Review 才能合并，默认不会自动强制合并。

**Q: 能同时监听多个 workflow 吗？**
A: 可以，将 `workflows` 改为数组：`["CI", "Lint", "Test"]`

**Q: 如何避免循环触发（修复后又失败）？**
A: 建议设置 `concurrency` 限制，或在自动修复 workflow 中加上路径过滤。
