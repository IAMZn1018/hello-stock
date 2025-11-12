# 股票综合分析系统 - 使用指南

## 🚀 快速开始（3步搞定）

### 方法1：直接运行示例

```bash
# 进入项目目录
cd /Users/cds-dn-569/Documents/hello-stock

# 运行示例（分析三维通信）
python example_comprehensive_analysis.py
```

### 方法2：自己写代码（推荐）

```python
from app.utils import StockComprehensiveAnalyzer

# 1. 创建分析器
analyzer = StockComprehensiveAnalyzer()

# 2. 分析股票（输入股票代码和名称）
result = analyzer.analyze_stock("002115", "三维通信")

# 3. 查看报告
report = analyzer.generate_report(result)
print(report)
```

**就这么简单！3行代码搞定！**

---

## 📖 详细使用方法

### 1. 分析单只股票

```python
from app.utils import StockComprehensiveAnalyzer

analyzer = StockComprehensiveAnalyzer()

# 基础用法（使用默认120天K线）
result = analyzer.analyze_stock("002115", "三维通信")

# 自定义K线天数
result = analyzer.analyze_stock("002115", "三维通信", kline_days=200)

# 只用股票代码（不提供名称也可以）
result = analyzer.analyze_stock("002115")

# 查看分析结果
print(f"综合评分: {result['summary']['overall_score']}")
print(f"操作建议: {result['summary']['recommendation']}")
```

### 2. 生成报告

```python
# 生成详细报告（包含技术指标）
report = analyzer.generate_report(result, detailed=True)
print(report)

# 生成简要报告（只看评分和建议）
report = analyzer.generate_report(result, detailed=False)
print(report)
```

### 3. 批量分析多只股票

```python
analyzer = StockComprehensiveAnalyzer()

stocks = [
    ("002115", "三维通信"),
    ("000001", "平安银行"),
    ("600036", "招商银行"),
    ("600519", "贵州茅台")
]

results = []
for code, name in stocks:
    print(f"分析 {name}...")
    result = analyzer.analyze_stock(code, name)
    summary = result['summary']
    results.append((name, summary['overall_score'], summary['recommendation']))

# 按评分排序
results.sort(key=lambda x: x[1], reverse=True)

print("\n=== 股票评分排名 ===")
for i, (name, score, rec) in enumerate(results, 1):
    print(f"{i}. {name:10s} {score:5.1f}分 - {rec}")
```

### 4. 访问原始数据

```python
result = analyzer.analyze_stock("002115", "三维通信")

# 访问问财诊股数据
diagnosis = result['diagnosis']
print(diagnosis.keys())  # 查看有哪些数据

# 访问K线数据
kline_data = result['kline_data']

# 访问技术分析结果
tech = result['technical_analysis']
print(f"当前价: {tech['basic_info']['close']}")
print(f"MA5: {tech['technical_indicators']['ma']['ma5']}")

# 访问DataFrame（用于自定义分析）
df = tech['dataframe']
print(df.tail(10))  # 查看最近10天数据
```

### 5. 导出分析结果

```python
import json

result = analyzer.analyze_stock("002115", "三维通信")

# 导出为JSON
export_data = {
    "stock_code": result['stock_code'],
    "stock_name": result['stock_name'],
    "summary": result['summary'],
}

with open(f"analysis_{result['stock_code']}.json", 'w', encoding='utf-8') as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)

print("已保存到 analysis_002115.json")
```

---

## 🎯 常见使用场景

### 场景1：快速筛选股票

```python
# 从自选股中找出高分股票
analyzer = StockComprehensiveAnalyzer()

my_stocks = [
    ("002115", "三维通信"),
    ("000001", "平安银行"),
    # ... 你的自选股
]

high_score_stocks = []
for code, name in my_stocks:
    result = analyzer.analyze_stock(code, name)
    score = result['summary']['overall_score']
    if score >= 70:  # 评分70分以上
        high_score_stocks.append((name, score))

print("高分股票:", high_score_stocks)
```

### 场景2：监控特定股票

```python
# 每天监控某只股票的变化
import time

analyzer = StockComprehensiveAnalyzer()

while True:
    result = analyzer.analyze_stock("002115", "三维通信")
    summary = result['summary']
    
    print(f"\n时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"评分: {summary['overall_score']}")
    print(f"建议: {summary['recommendation']}")
    
    # 如果评分达到买入标准
    if summary['recommendation'] == "买入":
        print("⚠️ 买入信号！")
        # 这里可以发送通知
    
    time.sleep(3600)  # 每小时检查一次
```

### 场景3：对比分析

```python
# 对比同行业股票
analyzer = StockComprehensiveAnalyzer()

# 银行板块
banks = [("000001", "平安银行"), ("600036", "招商银行"), ("601398", "工商银行")]

print("=== 银行板块对比 ===")
for code, name in banks:
    result = analyzer.analyze_stock(code, name)
    tech = result['technical_analysis']
    summary = result['summary']
    
    print(f"\n{name}({code})")
    print(f"  评分: {summary['overall_score']:.1f}")
    print(f"  当前价: {tech['basic_info']['close']}")
    print(f"  涨跌幅: {tech['basic_info']['change_pct']}%")
    print(f"  建议: {summary['recommendation']}")
```

---

## 📊 返回数据结构

```python
result = {
    "stock_code": "002115",
    "stock_name": "三维通信",
    "success": True,
    
    # 综合分析摘要
    "summary": {
        "overall_score": 69.0,        # 综合评分
        "risk_level": "中等风险",      # 风险等级
        "recommendation": "持有",      # 操作建议
        "score_details": {            # 各维度评分
            "技术面": 65.0,
            "资金面": 70.0,
            "基本面": 75.0,
            "消息面": 70.0
        },
        "key_points": [...],          # 关键要点
        "opportunities": [...],       # 机会提示
        "risks": [...]               # 风险提示
    },
    
    # 原始数据
    "diagnosis": {...},              # 问财诊股数据
    "kline_data": {...},            # K线原始数据
    "technical_analysis": {         # 技术分析结果
        "basic_info": {...},        # 基本信息
        "technical_indicators": {...}, # 技术指标
        "support_resistance": {...},  # 支撑压力位
        "dataframe": DataFrame       # 完整K线DataFrame
    }
}
```

---

## ⚙️ 参数说明

### `analyze_stock()`参数

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| `stock_code` | str | ✅ | 股票代码，如"002115" | - |
| `stock_name` | str | ❌ | 股票名称，如"三维通信" | None |
| `kline_days` | int | ❌ | K线数据天数 | 120 |

### `generate_report()`参数

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| `analysis_result` | dict | ✅ | `analyze_stock()`返回的结果 | - |
| `detailed` | bool | ❌ | 是否生成详细报告 | True |

---

## 💡 提示

1. **第一次运行较慢**：需要下载问财和K线数据
2. **数据更新**：建议白天交易时间运行，数据最新
3. **股票代码格式**：直接用6位代码，如"002115"
4. **批量分析**：建议每次分析间隔1-2秒，避免请求过快
5. **保存结果**：可以把分析结果保存为JSON，方便后续查看

---

## 🔧 故障排除

### 问题1：网络请求失败
```python
# 解决方法：添加重试机制
import time

def analyze_with_retry(analyzer, code, name, max_retries=3):
    for i in range(max_retries):
        try:
            return analyzer.analyze_stock(code, name)
        except Exception as e:
            print(f"第{i+1}次尝试失败: {e}")
            if i < max_retries - 1:
                time.sleep(2)
    return None
```

### 问题2：数据不完整
```python
# 检查返回结果
result = analyzer.analyze_stock("002115", "三维通信")

if not result['diagnosis']:
    print("问财数据获取失败")
    
if not result['kline_data']:
    print("K线数据获取失败")
```

---

## 📝 完整示例

创建一个文件 `my_analysis.py`：

```python
"""
我的股票分析脚本
"""
from app.utils import StockComprehensiveAnalyzer

def main():
    # 创建分析器
    analyzer = StockComprehensiveAnalyzer()
    
    # 我的自选股
    my_stocks = [
        ("002115", "三维通信"),
        ("000001", "平安银行"),
        ("600036", "招商银行"),
    ]
    
    print("=" * 80)
    print("我的自选股分析报告")
    print("=" * 80)
    
    for code, name in my_stocks:
        print(f"\n正在分析: {name}({code})")
        print("-" * 80)
        
        # 分析股票
        result = analyzer.analyze_stock(code, name)
        
        # 生成报告
        report = analyzer.generate_report(result, detailed=True)
        print(report)

if __name__ == "__main__":
    main()
```

运行：
```bash
python my_analysis.py
```

---

## 🎓 进阶用法

查看更多示例：
- `example_comprehensive_analysis.py` - 综合分析示例
- `example_technical_analysis.py` - 技术分析示例
- `example_eastmoney_api.py` - 东方财富API示例
- `example_ths_crawler.py` - 涨停雷达爬虫示例

---

## 📞 需要帮助？

如果遇到问题，可以：
1. 查看示例文件
2. 检查网络连接
3. 确认股票代码正确
4. 查看错误提示信息

