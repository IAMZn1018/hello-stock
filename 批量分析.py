"""
批量分析脚本 - 分析多只股票并排名
"""
from app.utils.stock_comprehensive_analyzer import StockComprehensiveAnalyzer
import time

# ============ 在这里添加你的自选股 ============
MY_STOCKS = [
    ("002115", "三维通信"),
    ("000001", "平安银行"),
    ("600036", "招商银行"),
    ("600519", "贵州茅台"),
    ("000858", "五粮液"),
]
# ===========================================

if __name__ == "__main__":
    print("=" * 80)
    print("批量股票分析")
    print("=" * 80)
    print(f"共有 {len(MY_STOCKS)} 只股票待分析\n")
    
    # 创建分析器
    analyzer = StockComprehensiveAnalyzer()
    
    # 存储分析结果
    results = []
    
    # 逐个分析
    for i, (code, name) in enumerate(MY_STOCKS, 1):
        print(f"[{i}/{len(MY_STOCKS)}] 正在分析: {name}({code})")
        print("-" * 80)
        
        try:
            # 分析股票
            result = analyzer.analyze_stock(code, name, kline_days=60)
            
            if result['success']:
                summary = result['summary']
                technical = result.get('technical_analysis', {})
                
                # 提取关键信息
                results.append({
                    "code": code,
                    "name": name,
                    "score": summary['overall_score'],
                    "recommendation": summary['recommendation'],
                    "risk_level": summary['risk_level'],
                    "price": technical.get('basic_info', {}).get('close', 0),
                    "change_pct": technical.get('basic_info', {}).get('change_pct', 0),
                    "tech_score": summary.get('score_details', {}).get('技术面', 0),
                    "fund_score": summary.get('score_details', {}).get('资金面', 0),
                })
                
                print(f"  ✓ 评分: {summary['overall_score']:.1f}  建议: {summary['recommendation']}  风险: {summary['risk_level']}")
            else:
                print(f"  ✗ 分析失败")
                
        except Exception as e:
            print(f"  ✗ 出错: {e}")
        
        # 避免请求过快
        if i < len(MY_STOCKS):
            time.sleep(1)
        
        print()
    
    # ========== 显示汇总结果 ==========
    if results:
        print("\n" + "=" * 80)
        print("分析汇总")
        print("=" * 80)
        
        # 按综合评分排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"\n{'排名':<4} {'股票名称':<10} {'代码':<8} {'评分':<6} {'建议':<6} {'当前价':<8} {'涨跌幅':<8}")
        print("-" * 80)
        
        for i, stock in enumerate(results, 1):
            print(f"{i:<4} {stock['name']:<10} {stock['code']:<8} {stock['score']:>5.1f} {stock['recommendation']:<6} {stock['price']:>7.2f} {stock['change_pct']:>6.2f}%")
        
        # ========== 推荐股票 ==========
        print("\n" + "=" * 80)
        print("推荐关注（评分≥70分）")
        print("=" * 80)
        
        recommended = [s for s in results if s['score'] >= 70]
        
        if recommended:
            for stock in recommended:
                print(f"\n✨ {stock['name']}({stock['code']})")
                print(f"   综合评分: {stock['score']:.1f}分")
                print(f"   操作建议: {stock['recommendation']}")
                print(f"   风险等级: {stock['risk_level']}")
                print(f"   技术面: {stock['tech_score']:.0f}分  资金面: {stock['fund_score']:.0f}分")
        else:
            print("\n暂无评分达到70分以上的股票")
        
        # ========== 需要注意的股票 ==========
        print("\n" + "=" * 80)
        print("需要注意（评分<50分或建议规避）")
        print("=" * 80)
        
        needs_attention = [s for s in results if s['score'] < 50 or s['recommendation'] == '规避']
        
        if needs_attention:
            for stock in needs_attention:
                print(f"\n⚠️  {stock['name']}({stock['code']})")
                print(f"   综合评分: {stock['score']:.1f}分")
                print(f"   操作建议: {stock['recommendation']}")
                print(f"   风险等级: {stock['risk_level']}")
        else:
            print("\n所有股票评分正常")
        
        # ========== 统计信息 ==========
        print("\n" + "=" * 80)
        print("统计信息")
        print("=" * 80)
        
        avg_score = sum(s['score'] for s in results) / len(results)
        highest = max(results, key=lambda x: x['score'])
        lowest = min(results, key=lambda x: x['score'])
        
        buy_count = sum(1 for s in results if s['recommendation'] == '买入')
        hold_count = sum(1 for s in results if s['recommendation'] == '持有')
        watch_count = sum(1 for s in results if s['recommendation'] == '观望')
        avoid_count = sum(1 for s in results if s['recommendation'] == '规避')
        
        print(f"\n平均评分: {avg_score:.1f}分")
        print(f"最高分: {highest['name']} {highest['score']:.1f}分")
        print(f"最低分: {lowest['name']} {lowest['score']:.1f}分")
        print(f"\n操作建议分布:")
        print(f"  买入: {buy_count} 只")
        print(f"  持有: {hold_count} 只")
        print(f"  观望: {watch_count} 只")
        print(f"  规避: {avoid_count} 只")
    
    print("\n" + "=" * 80)
    print("分析完成！")
    print("=" * 80)

