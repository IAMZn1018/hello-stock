"""
股票综合分析使用示例
演示如何使用综合分析器，自动获取问财诊股数据和K线数据，生成完整分析报告
"""
from app.utils.stock_comprehensive_analyzer import StockComprehensiveAnalyzer


def example_single_stock_analysis():
    """单只股票综合分析示例"""
    print("=" * 80)
    print("示例 1: 单只股票综合分析")
    print("=" * 80)
    
    # 创建综合分析器
    analyzer = StockComprehensiveAnalyzer()
    
    # 分析股票（自动获取所有数据）
    stock_code = "002115"
    stock_name = "三维通信"
    
    result = analyzer.analyze_stock(
        stock_code=stock_code,
        stock_name=stock_name,
        kline_days=120  # 获取120天的K线数据
    )
    
    if result['success']:
        # 生成并打印报告
        report = analyzer.generate_report(result, detailed=True)
        print("\n" + report)
    else:
        print("分析失败！")


def example_quick_analysis():
    """快速分析示例（只看摘要）"""
    print("\n\n" + "=" * 80)
    print("示例 2: 快速分析（仅摘要）")
    print("=" * 80)
    
    analyzer = StockComprehensiveAnalyzer()
    
    # 分析股票
    result = analyzer.analyze_stock("002115", "三维通信", kline_days=60)
    
    if result['success']:
        # 只生成简要报告
        report = analyzer.generate_report(result, detailed=False)
        print("\n" + report)


def example_batch_analysis():
    """批量分析多只股票"""
    print("\n\n" + "=" * 80)
    print("示例 3: 批量分析多只股票")
    print("=" * 80)
    
    analyzer = StockComprehensiveAnalyzer()
    
    # 要分析的股票列表
    stocks = [
        ("002115", "三维通信"),
        ("000001", "平安银行"),
        ("600036", "招商银行")
    ]
    
    results = []
    
    for code, name in stocks:
        print(f"\n正在分析: {name}({code})")
        print("-" * 80)
        
        try:
            result = analyzer.analyze_stock(code, name, kline_days=60)
            if result['success']:
                summary = result['summary']
                print(f"  综合评分: {summary['overall_score']:.1f}")
                print(f"  操作建议: {summary['recommendation']}")
                print(f"  风险等级: {summary['risk_level']}")
                results.append((name, summary['overall_score'], summary['recommendation']))
        except Exception as e:
            print(f"  分析失败: {e}")
    
    # 按评分排序
    if results:
        print("\n" + "=" * 80)
        print("综合评分排名")
        print("=" * 80)
        results.sort(key=lambda x: x[1], reverse=True)
        for i, (name, score, rec) in enumerate(results, 1):
            print(f"{i}. {name:10s} - {score:5.1f}分 - {rec}")


def example_custom_analysis():
    """自定义分析示例"""
    print("\n\n" + "=" * 80)
    print("示例 4: 自定义分析")
    print("=" * 80)
    
    analyzer = StockComprehensiveAnalyzer()
    
    # 只用股票代码（不提供名称）
    result = analyzer.analyze_stock("002115", kline_days=200)
    
    if result['success']:
        # 访问原始数据
        print("\n可以访问的数据:")
        print(f"  - 问财诊股数据: {'✓' if result['diagnosis'] else '✗'}")
        print(f"  - K线数据: {'✓' if result['kline_data'] else '✗'}")
        print(f"  - 技术分析: {'✓' if result['technical_analysis'] else '✗'}")
        
        # 自定义处理
        if result['technical_analysis']:
            tech = result['technical_analysis']
            df = tech['dataframe']
            print(f"\n  K线数据条数: {len(df)}")
            print(f"  数据时间范围: {df.iloc[0]['date'].strftime('%Y-%m-%d')} ~ {df.iloc[-1]['date'].strftime('%Y-%m-%d')}")
            print(f"  期间涨跌幅: {((df.iloc[-1]['close'] - df.iloc[0]['close']) / df.iloc[0]['close'] * 100):.2f}%")


def example_export_to_json():
    """导出分析结果为JSON"""
    print("\n\n" + "=" * 80)
    print("示例 5: 导出分析结果")
    print("=" * 80)
    
    import json
    
    analyzer = StockComprehensiveAnalyzer()
    result = analyzer.analyze_stock("002115", "三维通信", kline_days=60)
    
    if result['success']:
        # 准备导出数据（移除不能序列化的部分）
        export_data = {
            "stock_code": result['stock_code'],
            "stock_name": result['stock_name'],
            "summary": result['summary'],
        }
        
        # 如果需要技术分析数据
        if result.get('technical_analysis') and 'error' not in result['technical_analysis']:
            tech = result['technical_analysis']
            export_data['technical'] = {
                "basic_info": tech['basic_info'],
                "indicators": tech['technical_indicators'],
                "support_resistance": tech['support_resistance']
            }
        
        # 保存到文件
        filename = f"analysis_{result['stock_code']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n分析结果已导出到: {filename}")
        print(f"文件大小: {len(json.dumps(export_data, ensure_ascii=False))/ 1024:.2f} KB")


if __name__ == "__main__":
    # 运行示例（根据需要选择）
    
    # 示例1：完整的单只股票分析
    example_single_stock_analysis()
    
    # 示例2：快速分析
    # example_quick_analysis()
    
    # 示例3：批量分析（需要较长时间）
    # example_batch_analysis()
    
    # 示例4：自定义分析
    # example_custom_analysis()
    
    # 示例5：导出JSON
    # example_export_to_json()

