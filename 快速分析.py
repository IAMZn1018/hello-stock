"""
快速分析脚本 - 最简单的使用方式
直接运行这个文件即可！
"""
from app.utils import StockComprehensiveAnalyzer

# ============ 在这里修改你要分析的股票 ============
STOCK_CODE = "301308"
STOCK_NAME = "江波龙"
# ==============================================

if __name__ == "__main__":
    print("=" * 80)
    print(f"开始分析: {STOCK_NAME}({STOCK_CODE})")
    print("=" * 80)

    # 创建分析器
    analyzer = StockComprehensiveAnalyzer()

    # 分析股票（自动获取所有数据）
    result = analyzer.analyze_stock(STOCK_CODE, STOCK_NAME)

    # 生成并打印报告
    report = analyzer.generate_report(result, detailed=True)
    print("\n" + report)

    # 显示关键信息
    print("\n" + "=" * 80)
    print("关键信息摘要")
    print("=" * 80)

    summary = result['summary']
    print(f"\n📊 综合评分: {summary['overall_score']:.1f} 分")
    print(f"⚠️  风险等级: {summary['risk_level']}")
    print(f"💡 操作建议: {summary['recommendation']}")

    if summary.get('opportunities'):
        print("\n✅ 机会:")
        for opp in summary['opportunities']:
            print(f"   {opp}")

    if summary.get('risks'):
        print("\n⚠️  风险:")
        for risk in summary['risks']:
            print(f"   {risk}")

    print("\n" + "=" * 80)
    print("分析完成！")
    print("=" * 80)
