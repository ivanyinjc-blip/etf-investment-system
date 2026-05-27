# 07 - 验证方式与结果检查

> 本章核心观点：**验证比执行更重要。** 代码写得再快，改完不能跑等于零。

---

## 1. 为什么验证比执行更重要

### 反面案例

```
任务：修改用户登录逻辑
执行：Claude 花了 3 分钟改了 5 个文件
结果：用户反馈登录功能挂了
原因：没有运行测试，只做了"看起来对"的检查
```

### 正面案例

```
任务：修改用户登录逻辑
执行：
  1. 改 src/auth/login.ts（添加新验证规则）
  2. 运行 npm test -- auth.test.ts（测试通过 ✓）
  3. 运行 npm run dev（启动服务，手动测试登录流程 ✓）
  4. git commit
结果：功能正常上线，无回退
```

### 验证的价值

| 价值 | 说明 |
|------|------|
| **减少返工** | 早发现早修复，修复成本指数级降低 |
| **建立信任** | 经过验证的代码才能交付 |
| **记录状态** | 验证通过 = 某个时间点的稳定快照 |
| **支撑重构** | 有测试的代码才能安全重构 |

> **记住：没有验证的代码是半成品。**

---

## 2. 四种验证方式

### 2.1 测试验证

最可靠的验证方式，通过自动化测试确认功能正确性。

#### 单元测试（Unit Test）

针对最小代码单元（函数、类）的测试。

```bash
# 运行单个测试文件
npm test -- auth.test.ts

# 运行单个测试用例
npm test -- --testNamePattern="should reject invalid token"
```

**适用场景**：
- 纯函数逻辑
- 数据转换
- 工具函数

#### 集成测试（Integration Test）

测试多个模块协同工作的测试。

```bash
# 运行集成测试
npm run test:integration

# 或使用 supertest 测试 API
request(app)
  .post('/api/users/login')
  .send({ email: 'test@example.com', password: '123456' })
  .expect(200)
```

**适用场景**：
- API 端点
- 数据库操作
- 多模块协作

#### 端到端测试（E2E）

模拟真实用户操作的测试。

```bash
# 使用 Playwright E2E 测试
npx playwright test --grep "login flow"
```

**适用场景**：
- 关键业务流程
- 跨页面交互
- 登录/支付等核心功能

#### 测试验证的 Checkpoint 模板

```bash
# 给 Claude 的标准测试指令
请在修改后执行以下测试：
1. 单元测试：npm test -- <相关文件>
2. 集成测试：npm run test:integration
3. 如果有 E2E：npx playwright test
4. 覆盖率检查：npm run test:coverage
```

---

### 2.2 构建验证

确保代码能成功编译、打包，不引入语法错误或类型错误。

#### TypeScript 类型检查

```bash
# 纯类型检查（不生成文件）
npx tsc --noEmit

# 指定配置文件
npx tsc --noEmit -p tsconfig.json
```

#### 打包构建

```bash
# 前端项目
npm run build          # Vite/Webpack/Rollup 打包
npm run preview        # 预览构建结果

# Node.js 项目
npm run build          # TypeScript 编译
node dist/index.js     # 运行编译后的代码

# 检查构建产物
ls -la dist/
```

#### 构建验证 Checkpoint

```
构建验证标准：
□ TypeScript 类型检查通过（tsc --noEmit）
□ 构建命令成功执行（npm run build）
□ 产物文件正常生成
□ 产物大小在预期范围内（无异常膨胀）
```

---

### 2.3 截图验证

前端 UI 的可视化验证，适用于样式调整、组件修改。

#### 方法一：本地预览 + 截图

```bash
# 启动开发服务器
npm run dev

# 使用 Playwright 截图
npx playwright screenshot http://localhost:3000/dashboard dashboard.png
```

#### 方法二：Storybook 可视化测试

```bash
# 启动 Storybook
npm run storybook

# 截图特定组件
npx playwright screenshot http://localhost:6006/?path=/story/button--primary button.png
```

#### 方法三：报告生成

生成 PDF/HTML 报告进行人工检查：

```bash
# 生成测试报告
npm run test -- --reporter=html
# 打开 test-report.html 检查
```

#### 截图验证 Checkpoint

```
截图验证标准：
□ 页面正常渲染（无白屏/错误提示）
□ 关键元素可见（标题、表单、按钮）
□ 样式符合预期（颜色、间距、字体）
□ 响应式布局正常（移动端视图）
```

---

### 2.4 日志验证

通过程序输出、日志文件检查程序运行状态。

#### 查看标准输出

```bash
# 运行命令并查看输出
npm run dev 2>&1 | head -50

# 实时查看日志
tail -f logs/app.log
```

#### 检查错误日志

```bash
# 查看最近错误
grep -i "error" logs/app.log | tail -20

# 查看特定时间段的日志
grep "2026-05-27 14:" logs/app.log
```

#### 性能日志

```bash
# 检查启动时间
npm run dev 2>&1 | grep -i "ready\|started\|listening"

# 检查构建时间
npm run build 2>&1 | grep -i "built\|compiled\|done"
```

#### 日志验证 Checkpoint

```
日志验证标准：
□ 程序正常启动（无 FATAL 级别错误）
□ 无新增 ERROR 日志
□ 警告数量未显著增加
□ 性能指标在正常范围
```

---

## 3. 给 Claude 验证标准的方法

### 核心原则：描述期望结果，让 Claude 自验

**错误方式**：
> "帮我改一下登录函数"（没有验证标准）

**正确方式**：
> "帮我改一下登录函数，期望：
> 1. 有效 token 返回用户信息
> 2. 无效 token 返回 401
> 3. 测试用例要通过
> 4. 不要改动其他模块"

### 标准格式

```
## 任务
<具体要做什么>

## 验证标准
- [ ] 标准1：<期望结果>
- [ ] 标准2：<期望结果>
- [ ] 标准3：<期望结果>

## 禁止事项
- 不要改动 <某些文件/模块>
- 不要改变 <某些接口/行为>
```

### 示例：给一个完整的验证标准

```markdown
## 任务
修改 src/services/payment.ts 的退款逻辑，支持部分退款。

## 验证标准
- [ ] 原退款逻辑不受影响（全额退款仍然工作）
- [ ] 新增部分退款功能：amount 参数可小于 originalAmount
- [ ] amount > originalAmount 时抛出 ValidationError
- [ ] amount < 0 时抛出 ValidationError
- [ ] 单元测试 payment.test.ts 全部通过
- [ ] 集成测试 /api/refund 通过
- [ ] 日志中记录退款金额和原金额

## 禁止事项
- 不要修改 src/services/order.ts
- 不要改变 API 返回格式
- 不要添加新的支付渠道
```

---

## 4. 验证失败的处理流程

```
发现验证失败
    │
    ├─ 立即停止：不要带着失败的改动继续
    │
    ├─ 分析错误：看错误信息，判断原因
    │   ├─ 编译/类型错误 → 修正语法或类型定义
    │   ├─ 测试失败 → 看断言，理解期望 vs 实际
    │   ├─ 构建失败 → 检查依赖或配置
    │   └─ 运行时错误 → 读堆栈，找触发条件
    │
    ├─ 决定策略：
    │   ├─ 简单错误 → 立即修复
    │   ├─ 复杂错误 → /rewind 回退后重做
    │   └─ 无法修复 → 回退，拆解任务
    │
    └─ 重新验证：确认修复后再继续
```

### 常见验证失败的处理

| 失败类型 | 典型原因 | 修复方向 |
|---------|---------|---------|
| `npm test` 失败 | 断言不符预期 | 修正实现逻辑 |
| `tsc --noEmit` 失败 | 类型不匹配 | 添加类型注解 |
| `npm run build` 失败 | 依赖缺失/冲突 | 调整依赖版本 |
| 运行时报错 | 边界条件未处理 | 添加异常处理 |
| 页面白屏 | 组件渲染错误 | 检查 JSX/Props |

---

## 5. 自动化验证脚本的写法

### 脚本结构模板

```bash
#!/bin/bash
# verify.sh - 自动化验证脚本

set -e  # 遇错即停

echo "=== 步骤 1: 类型检查 ==="
npx tsc --noEmit

echo "=== 步骤 2: 单元测试 ==="
npm test -- --coverage

echo "=== 步骤 3: 构建 ==="
npm run build

echo "=== 步骤 4: 产物检查 ==="
test -f dist/index.js && echo "构建产物存在 ✓"
test -f dist/bundle.js && echo "Bundle 存在 ✓"

echo "=== 全部验证通过 ==="
```

### 在项目中使用

```bash
# 添加到 package.json
{
  "scripts": {
    "verify": "./verify.sh",
    "verify:quick": "npm test && npm run build"
  }
}

# 使用
npm run verify
```

### Claude 专用验证脚本

```bash
#!/bin/bash
# verify-for-claude.sh - Claude Code 专用验证脚本

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

run_check() {
  local name=$1
  local cmd=$2
  echo -e "${YELLOW}检查: ${name}${NC}"
  if eval "$cmd"; then
    echo -e "${GREEN}✓ ${name} 通过${NC}"
    return 0
  else
    echo -e "${RED}✗ ${name} 失败${NC}"
    return 1
  fi
}

failed=0

run_check "类型检查" "npx tsc --noEmit" || ((failed++))
run_check "单元测试" "npm test -- --passWithNoTests" || ((failed++))
run_check "构建" "npm run build" || ((failed++))

if [ $failed -eq 0 ]; then
  echo -e "\n${GREEN}所有验证通过 ✓${NC}"
  exit 0
else
  echo -e "\n${RED}${failed} 项验证失败${NC}"
  exit 1
fi
```

---

## 6. 最佳实践：每改必验，小步快跑

### 每改必验原则

每完成一个小改动，立即验证，再进行下一个。

```
改一点 → 验证 → 改下一点 → 验证 → ...
```

**不要**：
```
改 10 点 → 验证 → 发现 5 个错误 → 不知道哪个引入了哪个
```

### 小步快跑的工作流

```
[任务] 修改用户头像上传功能

[步骤 1] 改文件验证逻辑
  ├─ Edit: src/utils/validateImage.ts
  ├─ Bash: npm test -- validateImage.test.ts
  └─ Result: ✓ 通过

[步骤 2] 改文件上传逻辑
  ├─ Edit: src/services/upload.ts
  ├─ Bash: npm test -- upload.test.ts
  └─ Result: ✓ 通过

[步骤 3] 改前端组件
  ├─ Edit: src/components/AvatarUpload.tsx
  ├─ Bash: npm run build
  └─ Result: ✓ 通过

[步骤 4] 集成验证
  ├─ Bash: npm run test:integration
  └─ Result: ✓ 通过

[完成] git commit
```

### 验证频率建议

| 项目类型 | 最低验证频率 |
|---------|------------|
| 核心业务逻辑 | 每改一个函数验证一次 |
| 工具函数 | 每改一个函数验证一次 |
| UI 组件 | 每次修改后截图验证 |
| 配置变更 | 每次修改后重启验证 |
| 安全相关 | 每次修改后完整测试 |

---

## 本章小结

| 核心原则 | 具体做法 |
|---------|---------|
| 验证 > 执行 | 写完代码第一件事是验证，不是继续写 |
| 四种验证方式 | 测试 / 构建 / 截图 / 日志 |
| 给验证标准 | 用 Checkpoint 列表描述期望结果 |
| 失败处理 | 停 → 分析 → 回退/修复 → 重验 |
| 每改必验 | 小步修改，立即验证，不带错继续 |
| 自动化 | 写验证脚本，减少人工检查 |

下一章我们将讨论：**AGENTS.md 配置与最佳实践**——如何持久化项目级指令。
