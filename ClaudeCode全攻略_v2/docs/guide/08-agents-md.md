# 08 - AGENTS.md 配置与最佳实践

> 本章聚焦 Claude Code 的项目级持久化配置：AGENTS.md 的写法、最佳实践，以及如何与 OpenClaw 的 CLAUDE.md 区分使用。

---

## 1. 什么是 AGENTS.md

AGENTS.md 是 **Claude Code 的项目级指令文件**，用于将规则、工作流、约定持久化到项目中，让每次打开项目时 Claude 都能自动理解项目规范。

### 与普通注释的区别

| | 普通注释 | AGENTS.md |
|---|---|---|
| **作用范围** | 单个文件 | 整个项目 |
| **持久性** | 代码删除就没了 | 永久生效 |
| **执行约束** | Claude 可能忽略 | Claude 主动遵守 |
| **适用内容** | 代码解释 | 工作流、规则、约定 |

### AGENTS.md 能做什么

```markdown
# AGENTS.md
- 项目使用 pnpm，不使用 npm/yarn
- 测试命令：`pnpm test`
- 代码风格：单引号、尾逗号、4空格缩进
- 禁止：`any` 类型、裸 `catch`、魔法数字
```

---

## 2. AGENTS.md vs CLAUDE.md：两个系统的区别

> **注意**：这里的 CLAUDE.md 特指 OpenClaw 体系的全局配置，与 Claude Code 的 AGENTS.md 是两个独立系统。

| 维度 | AGENTS.md（Claude Code） | CLAUDE.md（OpenClaw） |
|------|-------------------------|---------------------|
| **工具** | Claude Code (`claude`) | OpenClaw (`openclaw`) |
| **作用范围** | 当前项目目录 | 全局 / 指定目录 |
| **加载时机** | 进入项目时自动加载 | 启动时加载 |
| **文件位置** | 项目根目录 `./AGENTS.md` | `~/.claude/CLAUDE.md` 或 `./CLAUDE.md` |
| **优先级** | 项目 > 全局 | 目录 > 全局 |
| **典型用途** | 项目规范、工作流、约定 | Agent 身份、团队架构、通用规则 |

### 两者如何协同

```
用户启动 Claude Code
    │
    ├─ 加载 ~/.claude/CLAUDE.md（全局配置）
    ├─ 进入项目目录
    ├─ 加载 ./AGENTS.md（项目配置）
    └─ 加载 .claude/rules/（路径范围规则）
    
用户启动 OpenClaw
    │
    ├─ 加载 ~/.claude/CLAUDE.md（全局配置）
    ├─ 加载 workspace/SOUL.md（Agent 身份）
    └─ 加载 workspace/AGENTS.md（可选）
```

**简单理解**：
- **AGENTS.md** → 约束 Claude Code（编程助手）
- **CLAUDE.md** → 约束 OpenClaw（多能力 Agent）

---

## 3. 位置优先级

Claude Code 加载配置文件的优先级（从高到低）：

```
1. .claude/commands/          ← 自定义命令（最高优先）
2. ./AGENTS.md                 ← 项目根目录
3. ./.claude/AGENTS.md         ← .claude 子目录
4. ~/.claude/AGENTS.md         ← 用户全局
5. ~/.claude/CLAUDE.md         ← 传统全局配置（兼容）
```

### 推荐的放置策略

| 场景 | 推荐位置 | 说明 |
|------|---------|------|
| 单人项目 | `./AGENTS.md` | 最简单，直接放在项目根目录 |
| 团队项目 | `./AGENTS.md` | 随代码库版本控制，团队共享 |
| 个人偏好 | `~/.claude/AGENTS.md` | 所有项目都适用的全局规则 |
| 路径特定规则 | `.claude/rules/` | 特定目录的特殊规则 |

---

## 4. 规则目录 .claude/rules/

`.claude/rules/` 目录用于存放 **路径范围规则**，只对特定目录下的文件生效。

### 目录结构

```
project/
├── .claude/
│   ├── AGENTS.md              # 项目全局规则
│   └── rules/
│       ├── frontend.md        # 只对 src/、components/ 生效
│       ├── backend.md         # 只对 server/、api/ 生效
│       └── tests.md           # 只对 tests/ 生效
├── src/
├── server/
└── tests/
```

### rules 文件的写法

```markdown
# .claude/rules/frontend.md
范围: src/, components/, pages/

# 前端特定规则
- 使用 CSS Modules 或 Tailwind，不要用 styled-components
- 组件文件用 PascalCase：UserCard.tsx
- 每个组件必须有 PropTypes 或 TypeScript 接口
```

### 规则冲突处理

如果不同 rules 文件对同一事物流出不同规定，按 **更具体的规则优先**：

```
AGENTS.md（全局） < rules/frontend.md（前端） < src/components/Button.tsx 的注释（单文件）
```

---

## 5. 有效指令示例

### 构建与测试命令

```markdown
# 构建命令
- 开发环境：`npm run dev`
- 构建：`npm run build`
- 测试：`npm test -- --coverage`
- 类型检查：`npx tsc --noEmit`
```

### 代码风格规则

```markdown
# 代码风格
- 缩进：2 空格（不是 4 空格）
- 字符串：单引号
- 分号：必须使用
- 尾逗号：多行时必须使用
- 导入排序：Node 内建 → 外部包 → 内部模块（用 @/ 别名）

# TypeScript
- 禁止 `any`，使用 `unknown` 代替
- 禁止 `as` 类型断言，优先用类型守卫
- 接口命名：I开头（如 IUserProps）或 PascalCase（如 UserProps）
```

### 工作流约定

```markdown
# 工作流
1. 修改前先 Read 相关文件
2. 小步修改，每次改一个函数
3. 修改后立即运行对应测试
4. 测试通过再继续

# Git 工作流
- commit message 格式：type(scope): description
- type: feat | fix | docs | style | refactor | test | chore
- 每个 commit 必须通过所有测试
```

### 项目结构说明

```markdown
# 目录结构
- src/api/         # API 调用层（axios 实例封装）
- src/components/  # 展示组件
- src/hooks/       # 自定义 React Hooks
- src/utils/       # 纯工具函数
- src/types/       # TypeScript 类型定义

# 命名约定
- 组件：PascalCase（UserCard.tsx）
- Hooks：camelCase 以 use 开头（useUserData.ts）
- 工具函数：camelCase（formatDate.ts）
- 类型文件：PascalCase（User.types.ts）
```

---

## 6. 团队 AGENTS.md 模板

```markdown
# 项目名 - AGENTS.md

## 技术栈
- Node.js 18+
- TypeScript 5.x
- React 18
- Vite
- pnpm

## 开发规范

### 代码风格
- 缩进：2 空格
- 字符串：单引号
- 分号：必须
- ESLint + Prettier 自动格式化

### TypeScript
- 严格模式：`strict: true`
- 禁止 `any` 类型
- 优先使用 `interface`，只在对联合类型建模时用 `type`
- 导出类型使用 `export type`

### Git
- 分支命名：feat/|fix/|hotfix/|release/
- Commit message：conventional commits
- 合并前必须通过 CI

## 工作流

### 任务执行
1. 理解需求（读需求文档 / 读相关代码）
2. 写测试（先写测试，再写实现）
3. 实现功能
4. 运行完整测试套件
5. 代码审查（自己先 review 一遍）

### 验证标准
- [ ] `npm test` 全部通过
- [ ] `npx tsc --noEmit` 无错误
- [ ] `npm run build` 成功
- [ ] 无 ESLint 错误

## 禁止事项
- 不要修改 `src/config/secrets.ts`（含敏感信息）
- 不要提交 `console.log`（用日志库）
- 不要直接操作 DOM（用 React）
- 不要在 render 中写业务逻辑（用 useMemo/useCallback）
```

---

## 7. 反面例子（哪些指令是噪音）

### ❌ 噪音指令 1：Claude 本身就知道的事

```markdown
# 不要这样写——Claude 本来就知道这些
- 使用合理的变量名
- 写注释解释代码
- 不要写死循环
- 代码要能运行
```

### ❌ 噪音指令 2：与已有工具重复的规则

```markdown
# 不要这样写——ESLint 已经强制执行了
- 分号必须使用
- 不能有未使用变量
- 缩进必须是 2 空格
```

### ❌ 噪音指令 3：无法验证的模糊规则

```markdown
# 不要这样写——无法验证，Claude 难以遵守
- "代码要优雅"
- "保持简洁"
- "不要过度设计"
```

### ❌ 噪音指令 4：过于细节的实现指令

```markdown
# 不要这样写——限制了 Claude 的创造力
- 必须用 for 循环，不能用 reduce
- 工具函数必须放在 utils/ 目录
- 每个文件不能超过 100 行
```

### ✅ 有效指令的特征

| 特征 | 说明 |
|------|------|
| **可验证** | 有明确的标准，Claude 可以自验 |
| **Claude 不知道** | 项目特有的规则，不是通用编程常识 |
| **有上下文** | 说明为什么有这个规则（帮助 Claude 理解） |
| **不过度约束** | 给出边界，不规定具体实现方式 |

---

## 8. 动态内存：/memory 命令

Claude Code 提供 `/memory` 命令，用于查看和管理会话内存。

### 相关命令

| 命令 | 功能 |
|------|------|
| `/memory` | 查看当前会话的内存条目 |
| `/memory add <text>` | 添加一个记忆条目 |
| `/memory remove <id>` | 删除指定记忆 |
| `/memory clear` | 清除所有记忆 |

### 记忆条目的用途

```markdown
# /memory add 的内容示例
- 用户偏好：使用 pnpm 而不是 npm
- 当前任务：重构支付模块，目标是支持 Stripe
- 已知问题：登录模块有个 race condition bug
```

### 记忆 vs AGENTS.md

| | 记忆（/memory） | AGENTS.md |
|---|---|---|
| **生命周期** | 当前会话 | 永久 |
| **内容类型** | 临时上下文、任务状态 | 持久规范、团队约定 |
| **适用场景** | 当前工作、临时注意事项 | 项目规则、通用约定 |

---

## 9. 最佳实践：保持 < 200 行，只写 Claude 不知道的

### 文件大小建议

**AGENTS.md 理想规模**：`50-150` 行

**原因**：
- Claude 的注意力有限，文件太长会被稀释
- 200 行以上的文件维护成本高
- 精简的文件更容易团队共享和 Code Review

### 只写 Claude 不知道的内容

```markdown
# 判断标准：这个规则 Claude 知道吗？

Claude 不知道（值得写）：
- 项目的技术栈和目录结构
- 团队的工作流约定（如何发布、如何分支）
- 特殊约束（本项目禁止用某库、本项目用某 ID 规则）
- 上下文知识（为什么要这样做、背后的业务逻辑）

Claude 知道（不要写）：
- 编程常识（不要用 any、变量要命名）
- 通用最佳实践（要写测试、要验证）
- 显而易见的规则
```

### 定期精简

建议每个季度检查一次 AGENTS.md：

- 删除已过时的规则
- 合并重复的规则
- 补充新发现的有效规则

---

## 本章小结

| 主题 | 关键要点 |
|------|---------|
| AGENTS.md 定义 | Claude Code 的项目级持久化配置 |
| 与 CLAUDE.md 区别 | Claude Code 专用 vs OpenClaw 通用 |
| 优先级 | .claude/commands > AGENTS.md > 全局 |
| .claude/rules/ | 路径范围的特定规则 |
| 有效指令 | 可验证 + Claude 不知道 + 有上下文 |
| 反面例子 | 常识重复、无法验证、过度约束 |
| /memory | 会话级临时记忆 |
| 最佳规模 | < 200 行，精简有效 |

下一章我们将讨论：**沙盒、审批与安全边界**——如何在享受便利的同时控制风险。
