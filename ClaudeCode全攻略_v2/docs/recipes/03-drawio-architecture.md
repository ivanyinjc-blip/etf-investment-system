# Claude Code × Draw.io MCP：AI 自动绘制架构图

> 让 Claude 读取代码，自动生成 draw.io 格式的架构图，从「想画图」到「出图」只要 10 分钟

---

## 场景

- 需要快速生成系统架构图，但手绘费时费力
- 想让 AI 理解代码结构后自动出图
- 需要在汇报、方案设计、技术文档中使用专业架构图
- 希望生成后可编辑（不是 PNG 死图）

---

## 工具栈

| 工具 | 用途 |
|------|------|
| Claude Code | AI 对话 + 代码理解 |
| Draw.io MCP Server | 生成 draw.io XML 格式文件 |
| Draw.io / draw.io desktop | 打开和编辑生成的图文件 |

---

## 核心步骤

### Step 1：安装 draw.io MCP 服务器

```bash
# 通过 npm 全局安装
npm install -g @modelcontextprotocol/server-drawio

# 或者通过 npx 直接运行（不需要全局安装）
npx -y @modelcontextprotocol/server-drawio
```

### Step 2：配置 Claude Code 使用 draw.io MCP

编辑 `~/.claude/settings.json`（全局）或项目目录下 `.claude/settings.json`：

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-drawio"]
    }
  }
}
```

配置后重启 Claude Code，MCP 工具自动加载。

### Step 3：Claude 读取代码，理解模块关系

```bash
# 进入项目目录
cd ~/my-project

# 启动 Claude，对话中让它理解代码结构
claude
```

**示例对话**：

```
用户：这是一个微服务项目，请读取 src/ 目录下的所有代码，理解服务划分和模块依赖关系，然后用 draw.io 格式生成一张系统架构图。

Claude：[Claude 会分析代码结构，然后调用 draw.io MCP 生成 .drawio 文件]
```

### Step 4：手动在 draw.io 打开编辑

```bash
# Claude 生成的文件路径
ls *.drawio

# macOS 用 draw.io 打开
open architecture.drawio

# Linux
xdg-open architecture.drawio

# Windows
start architecture.drawio
```

生成的 `.drawio` 文件是 XML 格式，可以用 draw.io 打开后进一步编辑、调整样式、添加标注。

---

## MCP 配置（完整 settings.json 示例）

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-drawio"]
    }
  }
}
```

如果需要自定义参数：

```json
{
  "mcpServers": {
    "drawio": {
      "command": "node",
      "args": ["/path/to/drawio-mcp-server/dist/index.js"],
      "env": {
        "DRAWIO_DEFAULT_STYLE": "sketch"
      }
    }
  }
}
```

---

## 生成的 draw.io XML 结构示例

Claude 通过 MCP 生成的 XML 大致结构：

```xml
<mxfile>
  <diagram name="系统架构图">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 服务节点 -->
        <mxCell id="2" value="API Gateway" style="rounded=1;whiteSpace=wrap;"
                vertex="1" parent="1">
          <mxGeometry x="200" y="50" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="User Service" vertex="1" parent="1">
          <mxGeometry x="50" y="150" width="100" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="4" value="Order Service" vertex="1" parent="1">
          <mxGeometry x="200" y="150" width="100" height="60" as="geometry"/>
        </mxCell>
        <!-- 连接线 -->
        <mxCell id="5" source="3" target="4" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 效果与收益

| 步骤 | 传统方式 | Claude + Draw.io MCP |
|------|---------|---------------------|
| 理解代码结构 | 人工阅读 30 分钟 | AI 2 分钟 |
| 画图 | 手绘 / 工具拖拽 1 小时 | 自动生成 2 分钟 |
| 修改 | 重新拖拽 | 编辑 XML 或重新生成 |
| 产出质量 | 取决于绘图能力 | 专业、一致 |

**总耗时：从 1.5 小时 → 10 分钟**

---

## 适用场景

### ✅ 非常适合
- 技术方案设计阶段的快速原型
- 系统架构文档（微服务架构、模块关系）
- 流程图（用户流程、数据流向）
- 汇报材料中的专业图表
- 技术博客配图

### ⚠️ 限制
- 复杂拓扑结构（大量节点）可能需要手动调整
- 默认样式偏基础，可在 draw.io 中美化
- MCP 工具调用受限于模型工具定义，可能需要分步骤生成

---

## 进阶用法

### 分层架构图生成

```
用户：请生成一张四层架构图：
- 接入层：CDN、负载均衡
- 应用层：API Gateway、认证服务
- 服务层：用户服务、订单服务、商品服务
- 数据层：MySQL、Redis、Kafka
用 draw.io 格式输出。
```

### 时序图生成

```
用户：请根据以下 API 调用流程生成一张时序图：
1. 客户端请求 → API Gateway
2. Gateway → 认证服务验证 Token
3. 认证服务返回用户信息
4. Gateway → 订单服务创建订单
5. 订单服务 → 消息队列发送事件
6. 通知服务消费事件 → 发送通知
```

### 自定义样式

在 CLAUDE.md 中预设样式规范：

```markdown
## 架构图样式规范
- 节点形状：服务用圆角矩形，数据库用圆柱形
- 颜色：接入层用蓝色系，应用层用绿色系，数据层用灰色系
- 字体：思源黑体，节点名 14pt，说明 11pt
- 连线：带箭头，实线表示同步，虚线表示异步
```

---

## 常见问题

**Q: npx 每次都要下载，速度慢怎么办？**
A: 先全局安装 `npm install -g @modelcontextprotocol/server-drawio`，然后 MCP 配置中用全局路径。

**Q: 生成的图太简单，怎么让它更专业？**
A: 在 prompt 中明确指定样式规范（颜色、字体、形状），或者在 draw.io 中手动美化后保存模板。

**Q: 支持哪些图表类型？**
A: 架构图、流程图、时序图、ER 图、网络拓扑图等 draw.io 支持的类型都支持。

**Q: 能否直接嵌入到 Markdown 文档中？**
A: 可以，将 .drawio 文件导出为 SVG 或 PNG，然后在 Markdown 中引用。
