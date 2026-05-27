---
title: "用 Claude Code 完成第一个任务"
description: "手把手教程：从零开始，用Claude Code完成第一个低风险任务，包含完整四步闭环流程和示例"
---

# 用 Claude Code 完成第一个任务

万事开头难，但只要完成第一个任务，你就会发现 Claude Code 有多顺手。本教程专为零基础新手设计，帮你从零到一走完全流程。

---

## 选择第一个任务的原则

**强烈建议选择低风险任务**，原因如下：

| ✅ 推荐任务 | ❌ 避免任务 |
|-----------|-----------|
| 修改 README 文档 | 生产环境数据库操作 |
| 给代码补注释 | 批量删除文件 |
| 修复拼写错误 | 修改支付逻辑 |
| 补充单元测试 | 危险的重构 |
| 整理项目结构 | 未备份的重要文件 |

> **目标**：第一次只练流程，不追求复杂任务。成功率比任务难度重要 100 倍。

---

## 四步闭环

Claude Code 完成任务遵循一套标准流程：**说明 → 执行 → 验证 → 沉淀**。

---

### Step 1：说明（Write Instructions）

这是最关键的一步。你需要把任务清晰地告诉 Claude Code：

```
【任务说明模板】
目标：_______________
范围：_______________
禁止事项：_______________
期望输出：_______________
```

**示例**：

```
目标：为 src/utils.py 文件中的 calculate_total 函数补上文档注释
范围：只修改 src/utils.py，不动其他文件
禁止事项：不要修改函数逻辑，只加注释
期望输出：函数上方有三引号文档字符串，说明参数、返回值、功能
```

### Step 2：执行（Execute）

Claude Code 收到任务后会：

1. **读取相关文件**（Read 工具）
2. **理解代码逻辑**
3. **提出修改方案**（Ask 模式会先确认，Auto 模式直接执行）
4. **执行修改**（Edit 工具）
5. **汇报状态**

**你需要做的**：观察 Claude 的每一步操作，理解它在做什么。

**Example 交互过程**：

```
你：请给 src/utils.py 的 calculate_total 函数补上文档注释

Claude：收到！我来执行以下步骤：
1. 读取 src/utils.py 文件
2. 找到 calculate_total 函数
3. 在函数上方添加三引号文档字符串
4. 说明参数类型和返回值

[Claude 使用 Edit 工具完成修改]

Claude：✅ 已完成修改：
- 文件：src/utils.py
- 改动：在 calculate_total 函数上方添加了文档注释
- 内容：说明了参数 prices (List[float]) 和返回值 float

请确认修改是否符合预期？
```

### Step 3：验证（Verify）

Claude 完成后，你**必须亲自验证**：

#### 验证清单

```
□ 修改的是正确的文件吗？
□ 修改的范围是否在预期内（没有误改其他内容）？
□ 实际效果是否达到预期？
□ 运行测试是否通过（如果有测试的话）？
```

#### 验证方法

```bash
# 方法1：查看修改内容
git diff src/utils.py

# 方法2：直接读取文件
Read: "src/utils.py"

# 方法3：运行相关测试
pytest tests/test_utils.py

# 方法4：查看语法是否正确
python -m py_compile src/utils.py
```

> **Tip**：即使 Claude 说了"已完成"，你也一定要自己检查一遍。这是建立信任的过程。

### Step 4：沉淀（Document）

把成功的流程记录下来，写入你的 `AGENTS.md` 或项目文档：

```
## Claude Code 使用记录

### 任务类型：补文档注释
### 成功流程：
1. 先 Read 目标文件，确认要修改的函数位置
2. 用清晰的模板说明任务（目标/范围/禁止/期望）
3. 让 Claude 执行，Ask 模式逐个确认
4. 用 git diff 验证修改内容
5. 用 pytest 运行测试确认无副作用
```

> **沉淀的价值**：下次遇到类似任务，直接复制成功流程，不需要重新摸索。

---

## 第一个任务的完整示例（截图式引导）

以下是一个完整的低风险任务示例：给 README.md 添加安装说明。

---

### 场景

你的项目 `my-project` 有一个 README.md，但没有安装说明。你想让它更完善。

```
📁 my-project/
├── README.md       ← 我们要改这个
├── src/
└── requirements.txt
```

### 第一步：在 Claude Code 中输入任务

```
你：请在 README.md 的 ## Installation 章节下，添加以下安装步骤：

1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py runserver

要求：
- 使用代码块格式
- 命令要准确
- 不要修改文件其他内容
```

### 第二步：Claude 读取文件

Claude 会自动执行 Read 工具，查看 README.md 的当前内容：

```
[Claude] 正在读取 README.md...
[Claude] 已读取文件，找到 ## Installation 章节。
```

### 第三步：Claude 提出修改方案（Ask 模式）

```
[Claude] 计划执行以下修改：

在 README.md 的 ## Installation 章节下，添加：

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

是否确认执行？
- [批准] [拒绝] [修改]
```

### 第四步：你批准，Claude 执行

```
你：批准

[Claude] ✅ 已完成修改
```

### 第五步：你验证结果

```bash
# 查看修改
git diff README.md

# 输出示例：
+ ```bash
+ pip install -r requirements.txt
+ python manage.py migrate
+ python manage.py runserver
+ ```
```

✅ 验证通过，修改内容正确！

### 第六步：沉淀

把这次成功经验写入 AGENTS.md 或个人笔记。

---

## 验收标准

完成以下检查，确认你已真正掌握 Claude Code 的使用流程：

| 检查项 | 标准 |
|-------|------|
| 能清晰描述任务目标 | 知道要什么，不知道不要什么 |
| 能说明任务范围 | 明确修改哪些文件，不改哪些 |
| 能验证修改结果 | 用 git diff / Read / 测试确认正确 |
| 能记录成功流程 | 把经验沉淀到文档 |

> **恭喜你**：如果以上 4 项都能做到，说明你已经完成了第一个 Claude Code 任务闭环！🎉

---

## 常见坑与避坑指南

### 坑1：任务描述太模糊

```
❌ 错误示例：
"帮我改一下代码"

✅ 正确示例：
"把 src/app.py 中 get_user() 函数的返回值从 dict 改为 User 对象（Pydantic Model）"
```

### 坑2：忘记验证就提交

```
❌ 危险操作：
Claude 完成后直接 git commit -a -m "update"

✅ 正确操作：
git diff → 检查修改内容 → pytest → 测试通过 → git commit
```

### 坑3：一次性给太多任务

```
❌ 错误示例：
"帮我重构整个项目，改命名、补注释、加测试、写文档"

✅ 正确操作：
每次只给一个任务，完成后验证，再给下一个
```

### 坑4：不知道 Claude 做了什么

```
✅ 正确操作：
在 Claude 执行过程中，观察它的每一步操作（Read了什么？Edit了什么？）
不懂就问："你为什么要这样做？"
```

---

## 下一步

- 📖 阅读 [入口地图：选对适合你的入口](./05-platform.md)，找到最顺手的 Claude Code 入口
- 🔄 尝试更多低风险任务，逐步提升复杂度
- 📝 每次成功任务都记录到 AGENTS.md，构建你自己的 Claude Code 最佳实践
