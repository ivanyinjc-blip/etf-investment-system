# ETF每日工作流

作者：superma｜创建时间：2026-05-21

---

## 持仓监控工作流

### 核心数据源优先级

```
第1选择：mootdx TCP 7709（实时分钟数据，全覆盖）
  ↓ 失败时
第2选择：腾讯qt.gtimg.cn（GBK解码，逗号分隔）
  ↓ 失败时
第3选择：新浪hq.sinajs.cn（GBK解码）
  ↓ 失败时
第4选择：东方财富push2.eastmoney
  ↓ 失败时
第5选择：腾讯K线历史收盘价（估算，不可用实时）
```

### ETF前缀规则
```
上海ETF（51/58/16开头）→ sh前缀
深圳ETF（15/56开头）  → sz前缀
⚠️ 实测例外：562500 → sh562500（非sz）
⚠️ 实测例外：159995 → sz159995
```

### mootdx实时数据获取

```python
import sys
sys.path.insert(0, '/home/ivanyinjc/.local/lib/python3.12/site-packages')
from mootdx.quotes import Quotes

c = Quotes.factory(market='std')

# 实时五档盘口
q = c.quotes(symbol=['562500', '513050', '516010', '159995', '159981', '512710', '563230'])
# 字段：price, last_close, open, high, low, bid1, ask1, bid_vol1, ask_vol1

# 分钟RSI计算
def get_minute_rsi(code, n=14):
    m = c.minute(symbol=code)
    closes = m['price'].values
    deltas = np.diff(closes[-n:])
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = gains.mean()
    avg_loss = losses.mean()
    rs = avg_gain / avg_loss if avg_loss > 0 else 100
    return round(100 - 100 / (1 + rs), 1)
```

### 止损线监控

```python
cost = pos['cost_price']
stop = pos['stop_loss_price']
warn = pos['warning_price']

if price <= stop:
    alert = "🚨 跌破止损线！立即执行止损！"
elif price <= warn:
    alert = "⚠️ 预警：接近止损线！密切关注！"
else:
    alert = "✅ 安全：价格在预警线以上"
```

---

## 每日复盘工作流

### Step 1: 读取持仓（DB优先，memory备援）

```python
import sqlite3
db_path = "/mnt/e/OneDrive/superma output/etf-research/自选股数据/etf_trading.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 持仓
cur.execute("SELECT etf_code, etf_name, entry_price, cost_price, quantity, position_pct, stop_loss_price, status FROM positions")
positions = cur.fetchall()

# 信号池
cur.execute("SELECT * FROM signal_pool WHERE status = 'in_position'")
signals = cur.fetchall()

# 最新技术扫描
cur.execute("""
    SELECT * FROM scan_log
    WHERE scan_date = (SELECT MAX(scan_date) FROM scan_log)
    GROUP BY etf_code
""")
latest_scans = {row[2]: row for row in cur.fetchall()}
```

### Step 2: 腾讯实时行情

```python
import urllib.request

def get_tencent_etf_data(codes):
    """codes格式: ['sh513350', 'sh562500', 'sz159995']"""
    url = f"https://qt.gtimg.cn/q={','.join(codes)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read().decode('gbk')

    result = {}
    for line in data.strip().split('\n'):
        if '=' in line:
            val = line.split('=')[1].strip().strip('"')
            if val.startswith('1~'):
                parts = val.split('~')
                code = parts[2]
                result[code] = {
                    'name': parts[1],
                    'current': float(parts[3]),
                    'pre_close': float(parts[4]),
                    'change_pct': float(parts[32]),
                    'high': float(parts[33]),
                    'low': float(parts[34]),
                }
    return result
```

### Step 3: 计算持仓盈亏

```python
for pos in positions:
    code, name = pos[0], pos[1]
    entry = pos[2]  # 入场价
    qty = pos[4]    # 数量
    stop_loss = pos[6]

    if code in etf_data and qty:
        current = etf_data[code]['current']
        change_pct = etf_data[code]['change_pct']
        current_value = qty * current
        cost_value = qty * entry
        pnl = current_value - cost_value
        pnl_pct = (current - entry) / entry * 100
```

### Step 4: 输出复盘报告

保存路径：
- OneDrive：`E:\OneDrive\superma output\etf-research\每日复盘\YYYYMMDD-每日复盘.md`
- Obsidian：`E:\OneDrive\obsidian-vault\05_投资\daily\YYYY-MM-DD-复盘.md`
- 有道云：`ETF量化交易/每日监测`（FolderID: 38BDA2B18FD24852BC6692EC3AEA6222）

---

## 数据验证工作流

### 交叉验证时机

```
□ MCP返回证券名称与预期不符 → 立即切换腾讯K线
□ 技术指标值明显异常（RSI>100等）→ 独立验算
□ 多数据源同一指标不一致 → 以腾讯K线计算结果为准
□ 发现异常 → 切换备用数据源
```

### RSI独立验算

```python
def calc_rsi_14(prices_list):
    """从收盘价序列计算RSI(14)"""
    if len(prices_list) < 15:
        return None
    gains, losses = [], []
    for i in range(1, len(prices_list)):
        diff = prices_list[i] - prices_list[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))

    avg_gain = sum(gains[0:14]) / 14
    avg_loss = sum(losses[0:14]) / 14

    results = []
    for i in range(14, len(gains)):
        avg_gain = (avg_gain * 13 + gains[i]) / 14
        avg_loss = (avg_loss * 13 + losses[i]) / 14
        if avg_loss == 0:
            results.append(100.0)
        else:
            rs = avg_gain / avg_loss
            results.append(100 - 100/(1+rs))
    return results
```

### BOLL计算

```python
import math

def calc_boll(prices, n=20, k=2):
    """计算布林带，返回(上轨, 中轨, 下轨)"""
    if len(prices) < n:
        return None, None, None

    upper, mid, lower = [None]*len(prices), [None]*len(prices), [None]*len(prices)
    for i in range(n-1, len(prices)):
        window = prices[i-n+1:i+1]
        sma = sum(window) / n
        std = math.sqrt(sum((v - sma)**2 for v in window) / n)
        mid[i] = round(sma, 4)
        upper[i] = round(sma + k * std, 4)
        lower[i] = round(sma - k * std, 4)

    return upper, mid, lower
```

---

## 已知数据覆盖状态

| ETF | 代码 | 腾讯qt | 新浪 | 东方财富 | mootdx | 备注 |
|:---|:---|:---:|:---:|:---:|:---:|:---|
| 机器人ETF | 562500 | ✅ | ✅ | ✅ | ✅ | 完全覆盖 |
| 中概互联 | 513050 | ✅ | ✅ | ✅ | ✅ | 完全覆盖 |
| 游戏ETF | 516010 | ✅ | ✅ | ✅ | ✅ | 完全覆盖 |
| 军工ETF | 512710 | ✅ | ✅ | ✅ | ✅ | 完全覆盖 |
| 卫星ETF | 563230 | ✅ | ✅ | ✅ | ✅ | 完全覆盖 |
| 华夏能源 | 159995 | ❌ | ❌ | ❌ | ✅ | 无实时，靠mootdx |
| 能源化工 | 159981 | ❌ | ❌ | ❌ | ✅ | 无实时，靠mootdx |
| 标普油气 | 513350 | ❌ | ❌ | ❌ | ❌ | 仅历史K线 |

**无实时覆盖ETF的识别特征：**
```
新浪返回: var hq_str_shXXXXXX=" ";
腾讯qt返回: v_pv_none_match="1"
东方财富push2: Remote end closed / data=null
腾讯K线: 正常（历史日线数据存在，仅实时行情缺失）
```

---

## 坑点速查

1. **腾讯qt是GBK编码**，不是UTF-8 → `decode('gbk')`
2. **f107/f117不是涨跌额/涨跌幅**，必须自己算：`(close-pre_close)/pre_close*100`
3. **腾讯K线 `day` vs `qfqday`** — 先打印keys确认：`data['data'][code].keys()`
4. **数据库trade_date格式不统一** — 同一表里有些是整数`20260506`，有些是字符串`2026-05-06`，用`parse_date()`自动识别
5. **新浪hq.sinajs.cn实时接口** 并非所有ETF都有数据，但Kline API覆盖面更广
6. **新浪/腾讯对513350返回空** — 5/15实测 `v_pv_none_match="1"` 和 `hq_str_sz513350=""`，但ifzq历史K线正常
7. **mootdx需要国内直连TCP 7709** — WSL/海外环境无法使用

---

*版本：v1.0 | 更新日期：2026-05-19*
