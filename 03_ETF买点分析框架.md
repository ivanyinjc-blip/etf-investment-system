# ETF买点分析框架：七维因子实战系统

作者：superma｜创建时间：2026-05-21

---

## 核心研究成果

### 最重要的3个发现（2026-05-12 实测）

**🔑 发现1：量比>5x是死亡信号，3x~5x是危险区**
- 量比>5x + RSI>70 + 大盘平稳 = 典型"反弹出货"组合，必然失败
- 量比3x~5x = 机构可能出货，需其他条件配合
- 量比1.5x~2.5x = 最佳买点，温和放量
- 案例：中韩半导体2026-01-29量比7.09x → 5日后-7.77%（失败）

**🔑 发现2：大盘超跌>-5%后启动，才是最佳时机**
- 2024-09-27：大盘前10日+16.2% → ETF三板块联动，全部双重成功
- 2025-01-10：大盘前10日-6.4%超跌 → ETF成功
- 大盘平稳期（-3%~+8%）的启动，往往是陷阱

**🔑 发现3：当日涨幅>8%需次日确认（可能是诱多）**
- 需要大盘配合才能确认是真启动
- 当日+2%~+6%是最健康的启动幅度

---

## Step 1: 数据获取

> ⚠️ **重要**：MiniMax MCP `mcp_ifind_stock_get_stock_performance` 查询ETF历史行情返回空，必须用Tushare Python API直接调用，或腾讯K线API。

```python
import tushare as ts
ts.set_token('09b1e6bd44802d199f3c9af64abaa2ccb18635cdf87dae245e631ecb')
pro = ts.pro_api()

# ETF日线（注意是fund_daily，不是daily；字段是vol不是volume）
df = pro.fund_daily(ts_code='513350.SH', start_date='20240101', end_date='20260511')
```

**腾讯财经K线API（推荐备选）：**
```python
import urllib.request, json, re

url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sz513350,day,,,500,qfq"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com/'})
with urllib.request.urlopen(req, timeout=15) as r:
    raw = r.read().decode('utf-8')
obj = json.loads(re.search(r'=(.+)', raw).group(1))
data = obj['data']['sz513350']
key = 'day' if 'day' in data else 'qfqday'  # 必须检查！
klines = data[key]
# 返回: [[date, open, close, high, low, volume], ...]
```

---

## Step 2: 七维因子计算

```python
def calc_7_dimensions(klines, idx, closes, volumes, daily_pcts):
    """计算启动点的七维因子"""
    curr_p = closes[idx]

    # 1. 均线系统
    ma5 = sum(closes[idx-5:idx]) / 5
    ma10 = sum(closes[idx-10:idx]) / 10
    ma20 = sum(closes[idx-20:idx]) / 20

    # 2. 成交量
    vol_today = volumes[idx]
    vol10_avg = sum(volumes[idx-10:idx]) / 10
    vol_ratio = vol_today / vol10_avg if vol10_avg > 0 else 0

    # 3. 波动率
    pcts10 = [abs(daily_pcts[j]) for j in range(idx-11, idx-1) if j < len(daily_pcts)]
    avg10_vol = sum(pcts10) / len(pcts10) if pcts10 else 0

    # 4. RSI
    rsi_vals = calc_rsi(closes, 14)
    rsi = rsi_vals[idx-1] if idx > 0 else 50

    # 5. MACD金叉
    dif_vals = calc_dif(closes)
    dea_vals = calc_dea(dif_vals, 9)
    golden_cross = dif_vals[idx-1] < dea_vals[idx-1] and dif_vals[idx] >= dea_vals[idx] if idx >= 1 else False

    # 6. 当日涨幅
    today_pct = daily_pcts[idx-1] if idx > 0 else 0

    # 7. 启动后5日/20日涨幅
    chg5 = (closes[idx+5] - curr_p) / curr_p * 100 if idx + 5 < len(closes) else 0
    chg20 = (closes[idx+20] - curr_p) / curr_p * 100 if idx + 20 < len(closes) else 0

    return {
        "price_vs_ma5": (curr_p - ma5) / ma5 * 100,
        "price_vs_ma20": (curr_p - ma20) / ma20 * 100,
        "ma5_vs_ma10": (ma5 - ma10) / ma10 * 100,
        "vol_ratio": vol_ratio,
        "avg10_vol": avg10_vol,
        "rsi": rsi,
        "golden_cross": golden_cross,
        "today_pct": today_pct,
        "chg5": chg5,
        "chg20": chg20,
    }
```

---

## Step 3: 判断标准

### 一票否决制（触发任何一个，直接放弃）

| 指标 | 放弃条件 | 原因 |
|------|---------|------|
| 量比 | **>5x** | 机构大量出货，必然失败 |
| RSI | >85 | 极度超买 |
| 大盘当日 | 暴跌>-3% | 系统性风险未完 |
| 均线 | MA5 < MA10 | 空头排列 |

### 七维评分表

| 星级 | 条件 | 达标值 | 权重 |
|------|------|--------|------|
| ★★★★★ | 大盘前10日跌幅 | >5%（超跌反弹） | 30% |
| ★★★★☆ | MA5 > MA10（均线多头） | >1.5% | 20% |
| ★★★★☆ | 量比 | 1.5x~2.5x（非放量出货） | 20% |
| ★★★☆☆ | 价格 vs MA20 | +8%~15% | 15% |
| ★★★☆☆ | 前10日均波动 | <1.5% | 15% |

**评分≥80分 = 高胜率买入区 | 60-80分 = 标准仓 | <40分 = 放弃**

### 各维度速查表

| 维度 | ✅ 达标 | ⚠️ 警惕 | ❌ 放弃 |
|------|--------|--------|--------|
| 大盘前10日 | 跌>5%或涨>8% | -3%~+3% | 大盘当日跌>3% |
| 均线 | MA5>MA10>MA20 | MA5>MA10 | MA5<MA10 |
| 量比 | **1.5x~2.5x ✅** | <1.2x（缩量） | **>5x ❌（出货）** |
| 前10日波动 | <1.5% | 1.5%~2% | >2% |
| RSI | 45~70 | 70~80 | >82 |
| 当日涨幅 | 2%~6% | 1%~2% | >8%（需确认） |

---

## Step 4: 超哥五步法策略制定

> 核心原则：买入时就设定好所有出场条件，不涨之后才想怎么卖

### 第一步：阶段识别

| 阶段 | 特征 | 止损宽度 | 操作 |
|------|------|---------|------|
| 抄底/低位建仓 | 近期暴跌15%+，RSI<50 | 宽止损（-15%） | 给更宽空间 |
| 追高/趋势确认 | 放量突破前高，量比1.5x~2.5x | 标准止损（-7~10%） | 追求买确认 |
| 趋势跟踪/持有 | 均线多头排列，已创新高 | 移动止盈（-12%） | 让利润奔跑 |

### 第二步：波动率定边界

```python
def calc_volatility_params(df, current_price):
    pct_chgs = df['pct_chg'].values / 100
    avg10 = abs(pct_chgs[-10:]).mean()
    vol10_yuan = current_price * avg10
    return {
        "avg10_vol%": avg10,
        "2x_vol": vol10_yuan * 2,   # 普通止损
        "3x_vol": vol10_yuan * 3,   # 宽止损（抄底）
        "4x_vol": vol10_yuan * 4,   # 移动止盈
    }
```

### 第三步：止损设定——支撑 × 波动率倍数交集

```python
def calc_stop_loss(cost_price, vol_params, structural_support, phase="追高"):
    x = {"抄底": 3.0, "追高": 2.5, "趋势": 2.0}.get(phase, 2.5)
    vol_stop = cost_price * (1 - vol_params["avg10_vol%"] * x)
    return max(vol_stop, structural_support)
```

### 第四步：分级止盈——前高 + 密集区

| 级别 | 目标 | 减仓 | 逻辑 |
|------|------|------|------|
| 一级 | 第一道结构阻力（前高/成交密集区） | 50% | 大概率遇阻回落 |
| 二级 | 第二道强阻力（心理关口/前低） | 50%剩余 | 心理关口 |
| 终极 | 历史前高/极值 | 全卖 | 不恋战 |

### 第五步：动态跟踪——突破后切换移动止盈

```python
def check_trailing_stop(current_price, history_high, highest_close, trailing_pct=0.12):
    if current_price > history_high:
        return {"mode": "trailing", "stop": highest_close * (1 - trailing_pct)}
    return {"mode": "normal", "stop": None}
```

### 五步法实操案例对比

| 维度 | 513350 中韩半导体 | 512710 军工龙头 |
|------|-----------------|----------------|
| 阶段识别 | 反弹初期（+20.5%），方向不明 | 弱势反弹（+10.5%），下跌中继概率大 |
| 波动率 | 3.11%（高波动） | 1.195%（普通波动） |
| 止损 | 3.573（-9.5%，缺口支撑） | 0.680（-15%，前低下方） |
| 一级止盈 | 4.23（+7.1%，前高阻力） | 0.870（+8.75%，套牢盘密集区） |
| 二级止盈 | 4.37（+10.6%，成交密集区） | 0.920（+15.0%，3月前低） |
| 终极止盈 | 4.65（+17.7%，历史前高） | 0.985（+23.1%，历史前高） |
| 移动止盈 | 突破后回撤-12%清仓 | 突破后回撤-12%清仓 |

---

## 持仓报告格式

```python
def format_position_report(name, date, entry, current, stop, pnl_pct, action, next_watch):
    return f"""
┌─────────────────────────────────────────────────────────────┐
│ 📊 【持仓跟踪】{name} {date}                              │
├──────────────────┬──────────────────────────────────────────┤
│ 持仓成本          │ {entry}元                                   │
│ 当前价格          │ {current}元                                  │
│ 盈亏              │ {pnl_pct}%                                 │
│ 止损价            │ {stop}元                                    │
├──────────────────┴──────────────────────────────────────────┤
│ 今日操作：{action}                                          │
│ 明日关注：{next_watch}                                      │
└─────────────────────────────────────────────────────────────┘
"""
```

---

## 关键Pitfalls

1. **Sina Kline API NoneType问题**：EMA计算时，前period个数据点是None，直接相加会报错。必须先过滤valid值。
2. **量比陷阱**：量比>5x在大部分情况下是机构出货，不是启动信号。只有在大盘超跌反弹背景下才可能是真启动。
3. **当日大阳线**：当日涨幅>8%的阳线不能直接追入，需要看次日是否延续。诱多概率>50%。
4. **均线多头≠立即买入**：MA5>MA10只是必要条件，必须结合大盘背景和量比综合判断。
5. **见光死陷阱**：卫星ETF、军工ETF等事件驱动型标的，利好消息落地=卖点而非买点。
6. **硬止损判断标准**：使用"昨收价 vs 成本×0.97"而非"当前价 vs 成本×0.97"，避免盘中波动误导。
7. **BIAS(5)替代布林位置**：布林中轨是动态MA20，价格回落时MA20也在上移，永远等不到"触及布林中轨"。用BIAS(5)<3%作为入场标准。

---

*版本：v1.0 | 更新日期：2026-05-19*
