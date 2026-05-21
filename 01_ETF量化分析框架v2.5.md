# ETF量化分析框架 v2.5

作者：superma｜创建时间：2026-05-21
原框架版本：v2.5（2026-05-19）

---

## ⚠️ 重大更新（v2.5 — 2026-05-19）

### 双数据库协同架构

**以后所有ETF分析必须先查 tushare.db 历史数据，再补充实时数据。**

┌────────────────────────────────────────────────────────────────────────────┐
│  数据库一：tushare.db (DuckDB) — 历史数据（主数据库）                       │
│  路径：/mnt/e/OneDrive/superma output/agent-system/tushare_pipeline/data/  │
│  数据量：2,672,154条日线，覆盖19980407~20260518，全市场2,102只ETF           │
│  Python路径：需要 /usr/bin/python3.12（含duckdb）                           │
│  读取方式：                                                                 │
│    # 方式1：直接DuckDB（推荐 /usr/bin/python3.12）                           │
│    import sys                                                               │
│    sys.path.insert(0, '/home/ivanyinjc/.local/lib/python3.12/site-packages') │
│    import duckdb                                                            │
│    DB = '/mnt/e/OneDrive/superma output/agent-system/tushare_pipeline/data/tushare.db'
│    conn = duckdb.connect(DB)                                                │
│    df = conn.execute("SELECT * FROM fund_daily WHERE ts_code='513050.SH' ORDER BY trade_date DESC LIMIT 30").df()
│                                                                              │
│    # 方式2：本地API封装（推荐，语法更简洁）                                   │
│    import sys                                                               │
│    sys.path.insert(0, '/mnt/e/OneDrive/superma output/agent-system')         │
│    from tushare_pipeline.local_api import fund_daily, fund_basic, query      │
│    df = fund_daily('513050.SH', start_date='20260501', end_date='20260518') │
│    df = fund_basic()   # 所有ETF基础信息                                    │
└──────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  数据库二：market_etf.db (SQLite) — 技术指标缓存                             │
│  路径：/mnt/e/OneDrive/superma output/etf-research/data/                     │
│  数据量：20只重点ETF指标缓存（ADX/RSI/MACD/BIAS等）                         │
│  表结构：etf_basic / etf_daily / etf_indicators / watched_etf / update_log   │
│  读取方式：                                                                 │
│    import sqlite3                                                           │
│    conn = sqlite3.connect('/mnt/e/OneDrive/superma output/etf-research/data/market_etf.db')
│    df = conn.execute("SELECT * FROM etf_indicators WHERE ts_code='513050'").fetchall()
└──────────────────────────────────────────────────────────────────────────────┘

**标准工作流：**
```
1. fund_daily 查历史K线（tushare.db）→ 计算技术指标
2. 腾讯API补充今日实时数据（index_daily仅同步到20260430）
3. market_etf.db 缓存20只重点ETF指标
4. 输出分析报告
```

**⚠️ Python环境限制：**
- DuckDB只在 `/usr/bin/python3.12` 可用（系统级安装）
- Hermes虚拟环境（`which python3`）不含duckdb
- 调用tushare.db必须用 `/usr/bin/python3.12` 或通过 `local_api.py` 间接调用

**用户持仓代码映射：**
| 持仓代码 | tushare代码 | 市场 |
|---------|-------------|------|
| 513050 | 513050.SH | 上交所 |
| 516010 | 516010.SH | 上交所 |
| 563230 | 563230.SH | 上交所 |
| 512710 | 512710.SH | 上交所 |
| 159995 | 159995.SZ | 深交所 |

---

## 核心架构

### 五态识别系统
```
强反弹（ADX≤10）→ RSI严重超卖 → 8成仓抄底
    ↓
弱反弹（10<ADX≤15）→ RSI超卖 → 5成仓
    ↓
震荡市（15<ADX≤25）→ 布林带 → 7成仓高抛低吸
    ↓
弱趋势（25<ADX≤35）→ 轻仓跟进
    ↓
强趋势（ADX>35）→ 均线动量 → 满仓顺势
```

### 四套策略体系
| 策略 | 市场状态 | 触发条件 | 仓位 |
|------|---------|---------|------|
| A.均线动量 | ADX>35 强趋势 | MA5金叉MA20+放量 | 满仓 |
| B.布林回归 | 15<ADX<25 震荡 | 触及下轨+RSI<40 | 7成 |
| C.RSI超跌 | 10<ADX<15 弱反弹 | RSI<30+MFI<40 | 5成 |
| D.CCI补充 | 通用 | CCI>100持仓/<-100空仓 | — |

### 风险管理三大模块
1. **VaR风险预算**：日VaR(95%) = 持仓市值 × 日波动率 × 1.65，单笔亏损 ≤ VaR预算50%
2. **ATR动态止损**：止损价 = 买入价 - 2.5 × ATR(14)
3. **极端行情熔断**：单日亏>3%禁开新仓；单日亏>5%强制减至50%；连亏3天策略暂停1天

---

## 实战教训（19条，2026-05-14~2026-05-19）

### 教训1：腾讯K线数据 'day' vs 'qfqday'（2026-05-14）

部分ETF（如纳指ETF 159941.SZ）K线数据存在 `qfqday` 键而非 `day`：

```python
# ❌ 错误：只用 'day'
klines = j['data'][prefix]['day']

# ✅ 正确：同时检查两个键
key = 'day' if 'day' in data else 'qfqday'
klines = data[key]
```

### 教训2：持仓XLS字段解析（2026-05-14）

`.xls` 文件是GBK编码的TSV格式，列索引含义如下：

```
[0]证券代码  [1]证券名称  [2]证券数量  [3]库存数量  [4]可卖数量
[5]买入均价    ← 每份买入价格（原成本）
[6]参考成本    ← 持仓总成本（元）= 买入均价 × 证券数量
[7]参考成本价  ← 券商参考成本单价
[8]参考盈亏成本价 ← 盈亏参考单价
[9]当前价      [10]最新市值  [11]浮动盈亏(元)  [12]盈亏比例(%)  [13]个股仓位(%)
```

**易错点：**
- `买入均价 [5]` ≠ `参考成本价 [7]`（两者不同）
- 计算综合成本时，必须用 `[5]买入均价 × 原持仓数量` 作为原持仓成本基准
- 不要用 `[7]参考成本价 × 数量`（那是券商系统计算的参考值）

**正确计算综合成本（加仓后）：**
```python
# 原持仓成本
orig_cost = buy_avg_old * qty_old   # 用[5]买入均价 × 数量
# 卖出回收
sell_back = sell_price * qty_sell
# 新增买入成本
add_cost = buy_price_new * qty_new
# 综合成本
new_total_cost = orig_cost - sell_back + add_cost
new_qty = qty_old - qty_sell + qty_new
new_buy_avg = new_total_cost / new_qty
```

### 教训3：ADX强反弹态 + RSI不超卖 → 信号冲突（2026-05-14）

v2.0框架"强反弹→8成仓抄底"的条件是 ADX≤10 **且 RSI<40**：

```python
if adx <= 10:
    if rsi < 40:
        position = 0.8  # 8成仓
    else:
        position = 0.3  # ⚠️ RSI不超卖，最多3成试探
```

### 教训4：震荡市加仓铁律（2026-05-14 实盘教训）

**0514两笔加仓全部违反B策略，抄底抄到半山腰：**

**512710军工ETF + 563230卫星ETF（今日）：**
- ADX=19~22 → 震荡市 ✅
- 布林带位置82~84% → 在上半部，非底部 ❌
- 距布林下轨还有7~14%空间 → 未触及下轨 ❌
- RSI=58~62 → 未超卖 ❌
- 结果：加仓后立刻大跌-4.9% / -5.8%

**正确B策略触发条件（两个必须同时满足）：**
```python
if 15 < adx <= 25:  # 震荡市
    if cur_price <= bb_lower * 1.03:  # 价格触及或接近布林下轨（3%容差）
        if rsi < 40:  # RSI超卖
            position = 0.7  # ✅ 可7成仓加仓
        else:
            position = 0.3  # ⚠️ RSI不超卖，最多3成试探
    else:
        position = 0  # ❌ 价格未触下轨，禁止加仓
```

### 教训5：加仓时机量化检查表（2026-05-14 新增铁律）

**每次加仓前必须逐项核对，全部✅才可执行：**

```python
def can_add_position(code, cur_price, adx, rsi, bb_upper, bb_lower, mfi, event_calendar):
    bb_range = bb_upper - bb_lower
    bb_pos = (cur_price - bb_lower) / bb_range * 100  # 布林位置%
    bb_dist_to_lower = (cur_price - bb_lower) / cur_price * 100  # 距下轨距离%

    # 检查1: 五态合规性
    if adx <= 10:
        if rsi < 40: pos, reason = 0.8, "强反弹+RSI超卖"
        else: pos, reason = 0.3, "强反弹但RSI未超卖→最多3成"
    elif adx <= 15:
        if rsi < 40: pos, reason = 0.5, "弱反弹+RSI超卖"
        else: pos, reason = 0.3, "弱反弹但RSI未超卖→最多3成"
    elif adx <= 25:
        if bb_dist_to_lower <= 3 and rsi < 40:
            pos, reason = 0.7, "震荡市触下轨+RSI超卖"
        elif bb_dist_to_lower <= 5:
            pos, reason = 0.3, "震荡市接近下轨但RSI未超卖→3成试探"
        else:
            pos, reason = 0, "震荡市未触下轨→禁止加仓"
    elif adx <= 35:
        pos, reason = 0.4, "弱趋势→4成仓"
    else:
        pos, reason = 0, "强趋势→禁止逆势加仓"

    # 检查2: RSI警戒线
    if rsi > 70:
        return False, 0, f"RSI={rsi:.1f}>70超买区→禁止加仓"
    # 检查3: MFI警戒线
    if mfi and mfi > 80:
        return False, 0, f"MFI={mfi:.1f}>80→资金面超买，禁止加仓"
    # 检查4: BIAS警戒线
    if bias and bias > 15:
        return False, 0, f"BIAS={bias:.1f}%>15%→正偏离过大，禁止加仓"
    # 检查5: 事件驱动"见光死"
    if event_calendar and event_today in event_calendar:
        return False, 0, f"今日有{event}事件→见光死高危日，禁止加仓"
    # 检查6: 加仓后立刻破成本3%=选错买点
    cost = get_cost(code)
    if (cost - cur_price) / cost > 0.03:
        return False, 0, "加仓价距成本>3%→买点错误，应等止跌"

    return True, pos, reason
```

### 教训6：加仓后立刻跌破成本3% → 绝对止损信号（2026-05-14）

**加仓军工的教训：**
```
买入价0.800，今日收盘0.774（已亏-3.25%）
→ 跌破成本3%，说明加仓时机完全错误
→ 必须严格执行止损，不可死扛
```

**操作原则：**
```
加仓后如果出现以下任意情况，立刻止损：
  ① 加仓后2日内跌幅超过3% → 选点错误，无条件止损
  ② 跌破加仓价的ATR止损线 → 触发即走
  ③ 大盘放量下跌日加仓 → 次日大概率继续跌

宁可止损认错，不可死扛等反弹。
```

### 教训7：事件驱动型标的的正确操作（见光死）（2026-05-14）

**563230卫星ETF：**
- 蓝箭朱雀二号火箭发射时间：5月14日 11:00
- 价格走势：开盘1.635 → 11点冲高1.643 → 单边下跌至收盘1.542（-5.75%）
- 规律：**利好事件兑现=主力拉高出货时机，不是加仓买点**

**事件驱动操作规范：**
```
① 事件兑现前1-2天：提前埋伏，等利好落地当天早盘高开减仓
② 事件落地当天（"见光日"）：绝对不追，不加仓，应减仓
③ 卫星ETF/军工ETF等主题炒作：短期涨幅>15%后遇到催化剂=最佳卖点
④ 判断"见光死"特征：事件当天量比>1.5x + 价格高开低走+涨幅收窄
⑤ 事件前已大涨>20%的标的，事件当天绝不可加仓
```

### 教训8：腾讯行情API实时数据 codes参数格式（2026-05-14）

**❌ 错误格式（加号分隔）：**
```python
url = f'https://qt.gtimg.cn/q=sh513050+sh516010+...'  # 超时或无数据
```

**✅ 正确格式（逗号分隔）：**
```python
url = f'https://qt.gtimg.cn/q=sh513050,sh516010,...'  # 正常返回
```

### 教训9：均线刚多头排列时减仓 → 连续被震荡出局（2026-05-15）

**现象（三笔交易共同模式）：**
1. 均线系统刚形成多头排列（MA5上穿MA10/MA20），行情启动初期
2. 立刻减仓/清仓
3. 随后经历3-5%的小幅震荡
4. 触及止损线被迫出局
5. 震荡结束后，标的在消息面+资金面支撑下继续走强，但已无仓位参与

**根本原因：**
| 维度 | 原因 | 权重 |
|:---|:---|:---:|
| 时序判断 | 将"均线刚多头排列"等同于"行情已走完"，实际是行情20-30%分位 | 30% |
| 止损设计 | 止损幅度过窄（-3%），小于正常震荡幅度（3-5%） | 25% |
| 持仓耐心 | 希望买入即涨，结构性行情演化需要时间 | 25% |
| 信号识别 | 混淆短期噪音和中期趋势 | 20% |

**铁律：**
```
① 均线刚多头排列 = 持仓区，不是卖点
② 止损幅度 ≥ 近期最大回调的1.5倍
③ 震荡期用仓位管理（高位减半仓+设止损），不直接全减
④ 出现牛市信号但无仓位，宁可追高也要上车
```

### 教训10：固定交易系统 —— 五步决策标准（2026-05-15）

**每次操作必须按顺序回答这五个问题：**

```
第一步：大盘是否配合？
  → 指数环境、赚钱效应、资金面

第二步：是否是买点？
  → 技术面位置（布林/MA/前高）+ RSI状态 + 催化事件

第三步：买入多少比例？
  → 根据五态+信号强度（10%试探/30%确认/50%重仓/80%满仓）

第四步：买入后持有策略？
  → 目标位 + 持有逻辑 + 分批止盈计划

第五步：止盈/止损条件？
  → 具体价格 + 具体条件，绝对禁止随意操作
```

**买入必须有技术支撑，卖出必须符合既定策略：**
```
买入：支撑位 + 信号 + 仓位 → 三者缺一不可
卖出：触发条件 + 理由 + 计划 → 三者必须对应
```

### 教训11：趋势初期踏空比追高被套更危险（2026-05-15）

**现象：** 半导体/通讯/AI每次结构性行情都错过，因为"不敢追高，等回调"。

**结构性行情特征：**
```
① 启动后不回头的概率 > 70%（不会给二次上车机会）
② 回调幅度通常只有3-5%，触发止损后立刻反弹
③ 均线刚多头排列的位置是行情的20-30%分位，不是终点
```

**正确做法：**
```
趋势初期（均线刚多头排列）：重仓持有，不猜顶
趋势中段（MA5走平）：高位减半仓
趋势末端（均线收敛+背离）：清仓
```

### 教训12：ADX边界值判定陷阱（2026-05-15）

**框架五态定义：**
```
弱趋势：25 < ADX ≤ 35（ADX=35 属于弱趋势，不是强趋势）
强趋势：ADX > 35（严格大于35，ADX=35.0 不算）
```

**常见错误：** 把 ADX=35.0 写成"强趋势"→ 五态判断与框架定义矛盾

### 教训13：布林位置作为入场参考的逻辑缺陷 —— 用BIAS(5)替代（2026-05-15）

**❌ 错误做法：**
```
布林位置 = (收盘价 - 下轨) / (上轨 - 下轨) × 100%
布林中轨 = MA20（动态值，随价格上升而上移）

规则："等价格回踩布林中轨(1.453)再入场"
```

**问题：** 布林中轨是动态MA20。当价格回落时，MA20也在上移——永远等不到价格"触及"布林中轨。

**✅ 正确做法：用BIAS(5)替代布林位置**

```
BIAS(5) = (收盘价 - MA5) / MA5 × 100%

判断规则：
BIAS(5) > +8%   → 超涨警告区，不追，等回调
BIAS(5) 3%~8%   → 可接受操作区间，可以操作
BIAS(5) < +3%   → 回踩充分，最佳入场点
```

### 教训14：三层止损体系 —— 硬止损+ATR软止损+移动止损（2026-05-15）

```python
# 第一层：硬止损（绝对红线，不可突破）
# 入场价 × 0.97 = 硬止损线（-3%）
# 收盘跌破硬止损线 → 当日收盘清仓
hard_stop = entry_price * 0.97

# 第二层：ATR软止损（趋势保护，趋势确认前使用）
# 止损线 = 入场价 - 2.5 × ATR(14)
# 收盘跌破ATR止损线 → 减仓50%
atr_stop = entry_price - 2.5 * atr14

# 第三层：移动止损（趋势确认后使用，随均线上移）
# 趋势确认：ADX > 35（严格大于35，ADX=35.0不算强趋势）
# 收盘跌破 MA5 × 0.98 → 减仓50%
# 收盘跌破 MA5 × 0.96 → 再减50%
# MA5死叉MA20 → 清仓
```

### 教训15：最少持有天数规则 —— 强制持有10个交易日防震荡洗出（2026-05-15）

**最少持有天数规则：**
```python
# 规则：建仓后10个交易日内，禁止主动卖出（硬止损除外）
# 例外条款（满足任一才可在10天内主动减仓）：
#   ① 连续2天BIAS(5) < -3%（趋势可能破坏）
#   ② 大盘系统性暴跌（单日-3%以上）
#   ③ 达到预设止盈目标（+15%以上）且五态非强趋势
```

**止盈纪律（分批止盈 + 趋势延续信号）：**
```python
# 止盈不是"卖出所有"而是"分批撤退"
# 止盈触发 AND 五态强趋势（ADX>35）→ 不执行止盈，继续持有
# 止盈触发 AND 五态非强趋势 → 执行分批止盈

止盈档位：
  +10%档：减仓1/3
  +20%档：再减1/3
  +30%档：清仓

趋势延续信号（出现任一则不止盈）：
  ① ADX从低位上升超过10个点
  ② +DI > -DI 超过10个点（多头主导加强）
  ③ RSI始终不破60
  ④ 缩量不破MA5
```

### 教训16：建仓前必须确认五态和仓位上限（2026-05-15）

**仓位上限（五态对应）：**
| 五态 | 仓位上限 | 条件 |
|:---|:---:|:---|
| 强反弹 RSI<30 | 80% | RSI严重超卖 |
| 弱反弹 | 30% | RSI未确认超卖 |
| 震荡市 | 30% | 无明确趋势 |
| 弱趋势 | 40% | 趋势不完整 |
| 强趋势 | 80% | 趋势确认 |

### 教训17：事件驱动型标的，事件当天绝对不追（2026-05-15）

```
事件驱动标的操作规范：
  ① 事件兑现前1-2天：提前埋伏，等利好落地当天早盘高开减仓
  ② 事件落地当天（"见光日"）：绝对不追，不加仓，应减仓
  ③ 事件前已大涨>15%的标的，事件当天必须减仓
  ④ 事件当天量比>1.5x + 价格高开低走 → 确认见光死，立刻清仓
```

### 教训18：mootdx实时分钟数据——盘中分析的核心工具（2026-05-15）

**mootdx覆盖全部持仓ETF：**
```
✅ minute() — 120条分钟数据，包含当前盘中实时价格
✅ quotes() — 五档盘口+46字段实时报价
✅ bars() — 多周期K线（1/5/15/30/60分钟）
✅ 覆盖全部持仓ETF：562500/513050/516010/159995/159981/512710/563230
```

### 教训19：ADX计算必须用Wilder平滑——简单均值算法严重失真（2026-05-19）

**❌ 错误算法（简单均值，会严重失真）：**
```python
# 这是错的！简单均值不对
dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100
adx = np.mean([dx] * 14)  # ❌ 直接均值，严重低估ADX
```

**✅ 正确算法（Wilder EMA平滑，标准ADX）：**
```python
def calc_adx_wilder(highs, lows, closes, period=14):
    n = len(closes)
    tr_list = np.array([
        max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1]))
        for i in range(1, n)
    ])
    up_dm = np.zeros(n-1)
    down_dm = np.zeros(n-1)
    for i in range(1, n):
        up = highs[i] - highs[i-1]
        down = lows[i-1] - lows[i]
        up_dm[i-1] = up if (up > down and up > 0) else 0
        down_dm[i-1] = down if (down > up and down > 0) else 0

    atr = np.mean(tr_list[:period])
    plus_dm_s = np.mean(up_dm[:period])
    minus_dm_s = np.mean(down_dm[:period])

    dx_list = []
    for i in range(period, len(tr_list)):
        atr = (atr * (period - 1) + tr_list[i]) / period
        plus_dm_s = (plus_dm_s * (period - 1) + up_dm[i]) / period
        minus_dm_s = (minus_dm_s * (period - 1) + down_dm[i]) / period
        plus_di = plus_dm_s / atr * 100 if atr > 0 else 0
        minus_di = minus_dm_s / atr * 100 if atr > 0 else 0
        di_sum = plus_di + minus_di
        dx = abs(plus_di - minus_di) / di_sum * 100 if di_sum > 0 else 0
        dx_list.append(dx)

    if len(dx_list) < period:
        return 0.0, 0.0, 0.0
    adx = np.mean(dx_list[:period])
    for i in range(period, len(dx_list)):
        adx = (adx * (period - 1) + dx_list[i]) / period  # Wilder EMA

    return float(adx), float(plus_di), float(minus_di)
```

**误差实测对比（2026-05-18）：**
| ETF | 错误ADX | 正确ADX | 五态（错误） | 五态（正确） |
|:-----|:-------:|:-------:|:------------|:------------|
| 515790光伏 | 3.4 | **14.0** | 无趋势（❌） | 弱反弹 ✅ |
| 159131港股通 | 38.0 | 37.3 | 强趋势 | 强趋势 |
| 159611电力 | 36.1 | 31.4 | 强趋势 | 弱趋势 |

**结论：** 简单均值算法在ADX<20时误差极大。**所有ADX计算必须用Wilder平滑版本。**

---

*框架版本历史：v2.1（教训1-8，2026-05-14）→ v2.2（教训9-11，2026-05-15）→ v2.3（教训12-13，2026-05-15）→ v2.4（教训14-17，2026-05-15）→ v2.5（教训18+双数据库协同，2026-05-19）→ v2.6（教训19：ADX必须用Wilder平滑，2026-05-19）*
