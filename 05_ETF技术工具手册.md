# ETF技术工具手册

作者：superma｜创建时间：2026-05-21

---

## 腾讯财经K线API

### 基础URL
```
https://web.ifzq.gtimg.cn/appstock/app/fqkline/get
```

### 参数格式
```
?_var=kline_dayqfq&param={code},{type},{start},{end},{count},{fq}
```

| 参数 | 说明 | 示例 |
|:---|:---|:---|
| `code` | 股票代码（含交易所前缀） | `sh588080`、`sz513050` |
| `type` | K线类型 | `day`（日线） |
| `start` | 开始日期 | `2026-01-01` |
| `end` | 结束日期 | `2026-05-15` |
| `count` | 数据条数上限 | `200`、`1000` |
| `fq` | 复权类型 | `qfq`（前复权）、`none`（不复权） |

### ⚠️ 关键陷阱：`day` vs `qfqday` key

**不同标的返回的key不同，必须同时检查：**

```python
import urllib.request, json, re

url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh588080,day,2026-03-01,2026-05-15,200,qfq"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com/'})
resp = urllib.request.urlopen(req, timeout=10)
raw = resp.read().decode('utf-8')
obj = json.loads(re.search(r'=(.+)', raw).group(1))

# ✅ 正确：同时检查两个键
key = 'day' if 'day' in obj['data']['sh588080'] else 'qfqday'
klines_raw = obj['data']['sh588080'][key]
```

### 实时价格API

```
https://qt.gtimg.cn/q={codes}
```

**⚠️ codes参数用逗号分隔，不是加号：**

```python
# ✅ 正确
url = "https://qt.gtimg.cn/q=sh513050,sh516010,sh562500"

# ❌ 错误（会超时或无数据）
url = "https://qt.gtimg.cn/q=sh513050+sh516010+sh562500"
```

返回格式：每行一个标的，格式为 `v_sh513050="1,1.225,1.230,..."`

---

## mootdx实时分钟数据

### 环境要求
```
✅ 国内直连网络（TCP端口7709可通）
❌ 海外/WSL非直连环境 → TCP连接失败
```

### Python路径配置
```python
import sys
sys.path.insert(0, '/home/ivanyinjc/.local/lib/python3.12/site-packages')
from mootdx.quotes import Quotes

c = Quotes.factory(market='std')
```

### 核心功能

**minute() — 当日分时数据（120条）**
```python
m = c.minute(symbol='562500')
# 列: price, vol, volume
# 索引: 0-119（顺序编号，非时间戳）
```

**quotes() — 实时五档盘口**
```python
q = c.quotes(symbol=['562500', '159995', '159981'])
price = q['price'].iloc[0]       # 当前价
last_close = q['last_close'].iloc[0]  # 昨收
high = q['high'].iloc[0]         # 今高
low = q['low'].iloc[0]           # 今低
bid1 = q['bid1'].iloc[0]        # 买一价
ask1 = q['ask1'].iloc[0]        # 卖一价
```
⚠️ **字段名差异**: `close` → `last_close`，无`name`列

**bars() — 多周期K线**
```python
# category: 4=日线, 5=周线, 6=月线, 7=1分钟, 8=5分钟, 9=15分钟, 10=30分钟, 11=60分钟
k = c.bars(symbol='562500', category=9, offset=10)  # 15分钟K线
```

### 盘中RSI监控模板

```python
import sys, numpy as np
sys.path.insert(0, '/home/ivanyinjc/.local/lib/python3.12/site-packages')
from mootdx.quotes import Quotes

c = Quotes.factory(market='std')

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

for code in ['562500', '159995', '513050']:
    m = c.minute(symbol=code)
    q = c.quotes(symbol=[code])
    rsi = get_minute_rsi(code)
    price = q['price'].iloc[0]
    high = q['high'].iloc[0]
    low = q['low'].iloc[0]
    print(f"{code}: 现价={price} 区间={low}~{high} 分钟RSI={rsi}")
```

---

## 纯Python回测框架（无TA-Lib）

### 技术指标实现

**SMA**
```python
def sma(close, period):
    result = []
    for i in range(len(close)):
        if i < period - 1:
            result.append(np.nan)
        else:
            result.append(np.mean(close[i-period+1:i+1]))
    return np.array(result)
```

**EMA**
```python
def ema(close, period):
    k = 2 / (period + 1)
    result = [close[0]]
    for i in range(1, len(close)):
        result.append(close[i] * k + result[-1] * (1 - k))
    return np.array(result)
```

**MACD**
```python
def macd(close, fast=12, slow=26, signal=9):
    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    dif = ema_fast - ema_slow
    dea = ema(dif, signal)
    hist = (dif - dea) * 2
    return dif, dea, hist
```

**RSI（Wilder平滑）**
```python
def rsi(close, period=14):
    n = len(close)
    gains = np.zeros(n-1)
    losses = np.zeros(n-1)
    for i in range(1, n):
        diff = close[i] - close[i-1]
        gains[i-1] = max(diff, 0)
        losses[i-1] = max(-diff, 0)

    result = np.full(n, np.nan)
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    result[period] = 100.0 if avg_loss == 0 else 100 - 100 / (1 + avg_gain / avg_loss)

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        result[i+1] = 100.0 if avg_loss == 0 else 100 - 100 / (1 + avg_gain / avg_loss)
    return result
```

**ATR**
```python
def atr(high, low, close, period=14):
    n = len(high)
    tr = np.zeros(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr[i] = max(high[i]-low[i], abs(high[i]-close[i-1]), abs(low[i]-close[i-1]))

    atr_val = np.zeros(n)
    atr_val[0] = tr[0]
    k = 1 / period
    for i in range(1, n):
        atr_val[i] = tr[i] * k + atr_val[i-1] * (1 - k)
    return atr_val
```

**ADX（Wilder平滑）**
```python
def adx(high, low, close, period=14):
    n = len(high)
    plus_dm = np.zeros(n)
    minus_dm = np.zeros(n)
    tr = np.zeros(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr[i] = max(high[i]-low[i], abs(high[i]-close[i-1]), abs(low[i]-close[i-1]))
        up = high[i] - high[i-1]
        down = low[i-1] - low[i]
        plus_dm[i] = up if up > down and up > 0 else 0
        minus_dm[i] = down if down > up and down > 0 else 0

    atr_val = atr(high, low, close, period)
    plus_di = np.zeros(n)
    minus_di = np.zeros(n)
    for i in range(period, n):
        if atr_val[i] != 0:
            plus_di[i] = np.sum(plus_dm[i-period+1:i+1]) / atr_val[i] * 100
            minus_di[i] = np.sum(minus_dm[i-period+1:i+1]) / atr_val[i] * 100

    dx = np.zeros(n)
    for i in range(period, n):
        di_sum = plus_di[i] + minus_di[i]
        if di_sum != 0:
            dx[i] = abs(plus_di[i] - minus_di[i]) / di_sum * 100

    adx_val = np.zeros(n)
    adx_val[period] = dx[period]
    k = 1 / period
    for i in range(period + 1, n):
        if not np.isnan(dx[i]):
            adx_val[i] = dx[i] * k + adx_val[i-1] * (1 - k)
    return adx_val, plus_di, minus_di
```

### ADX自适应策略框架

```
市场状态判断：
  ADX > 25  → 趋势市场 → 启用均线策略（MA20/MA60金叉死叉）
  ADX < 20  → 震荡市场 → 启用RSI均值回归（RSI<30买入，RSI>70卖出）
  ADX 20-25 → 过渡区 → 不开新仓，持仓不动

止损：-5%硬止损
```

---

## XLS文件读取

**⚠️ .xls文件是GBK编码TSV，不是Excel二进制！**

```python
# ✅ 正确读法
with open(path, 'rb') as f:
    content = f.read().decode('gbk')
lines = content.strip().split('\r\n')

# ❌ 错误读法（xlrd会报BOF）
import xlrd; xlrd.open_workbook(path)
```

---

*版本：v1.0 | 更新日期：2026-05-19*
