"""
股票综合分析器
整合问财诊股数据、东方财富K线数据和技术分析，生成完整的股票分析报告
"""
from typing import Dict, Optional
from .wencai_api import WenCaiAPI
from .eastmoney_api import EastMoneyAPI
from .technical_analysis import StockAnalyzer
from app.core.deepseek_api import DeepSeekAPI


class StockComprehensiveAnalyzer:
    """股票综合分析器，整合多个数据源"""
    
    def __init__(self, use_ai: bool = True):
        """
        初始化分析器
        
        Args:
            use_ai: 是否使用AI大模型进行分析，默认True
        """
        self.wencai_api = WenCaiAPI()
        self.eastmoney_api = EastMoneyAPI()
        self.technical_analyzer = StockAnalyzer()
        self.use_ai = use_ai
        if use_ai:
            self.deepseek_api = DeepSeekAPI()
    
    def analyze_stock(self, stock_code: str, stock_name: str = None, kline_days: int = 120) -> Dict:
        """
        综合分析股票
        
        Args:
            stock_code: 股票代码，如 "002115"
            stock_name: 股票名称，如 "三维通信"（可选）
            kline_days: K线数据天数，默认120天
        
        Returns:
            综合分析结果字典
            
        Example:
            >>> analyzer = StockComprehensiveAnalyzer()
            >>> result = analyzer.analyze_stock("002115", "三维通信")
            >>> print(result['summary'])
        """
        print(f"开始分析股票: {stock_name or stock_code}")
        
        # 1. 获取问财诊股数据
        print("  [1/3] 获取问财诊股数据...")
        diagnosis = self.wencai_api.get_stock_diagnosis(stock_name or stock_code)
        
        # 2. 获取K线数据
        print("  [2/3] 获取K线历史数据...")
        # 构建secid（市场代码.股票代码）
        secid = self._build_secid(stock_code)
        kline_data = self.eastmoney_api.get_stock_history(secid=secid, lmt=kline_days)
        
        # 3. 技术分析
        print("  [3/3] 进行技术分析...")
        technical_result = None
        if kline_data:
            technical_result = self.technical_analyzer.analyze(kline_data)
        
        # 整合结果
        result = {
            "stock_code": stock_code,
            "stock_name": stock_name or stock_code,
            "diagnosis": diagnosis,
            "kline_data": kline_data,
            "technical_analysis": technical_result,
            "success": True
        }
        
        # 生成综合评分和建议
        result["summary"] = self._generate_summary(diagnosis, technical_result)
        
        print("分析完成！")
        return result
    
    def _build_secid(self, stock_code: str) -> str:
        """
        构建secid（市场代码.股票代码）
        
        Args:
            stock_code: 股票代码
        
        Returns:
            secid字符串，如 "0.002115"
        """
        # 判断市场：
        # 0: 深圳（创业板00、中小板002、深市主板000）
        # 1: 上海（主板60、科创板688）
        if stock_code.startswith('6'):
            market = '1'
        elif stock_code.startswith('688'):
            market = '1'
        else:
            market = '0'
        
        return f"{market}.{stock_code}"
    
    def _generate_summary(self, diagnosis: Dict, technical: Dict) -> Dict:
        """
        生成综合分析摘要
        
        Args:
            diagnosis: 问财诊股数据
            technical: 技术分析结果
        
        Returns:
            综合摘要字典
        """
        # 如果启用AI分析，尝试使用大模型
        if self.use_ai:
            try:
                ai_summary = self._generate_ai_summary(diagnosis, technical)
                if ai_summary:
                    return ai_summary
            except Exception as e:
                print(f"AI分析失败，使用规则评分: {e}")
        
        # Fallback: 使用原有的规则评分
        return self._generate_rule_based_summary(diagnosis, technical)
    
    def _generate_ai_summary(self, diagnosis: Dict, technical: Dict) -> Optional[Dict]:
        """
        使用大模型生成分析摘要
        
        Args:
            diagnosis: 问财诊股数据
            technical: 技术分析结果
        
        Returns:
            AI生成的摘要，失败返回None
        """
        # 准备数据给大模型
        stock_data = self._format_data_for_ai(diagnosis, technical)
        
        # 调用大模型
        result = self.deepseek_api.analyze_stock_data(stock_data)
        
        if result['success'] and result['data']:
            ai_result = result['data']
            
            # 确保必要字段存在
            summary = {
                "overall_score": ai_result.get("overall_score", 50.0),
                "risk_level": ai_result.get("risk_level", "中等风险"),
                "recommendation": ai_result.get("recommendation", "观望"),
                "key_points": ai_result.get("key_points", []),
                "risks": ai_result.get("risks", []),
                "opportunities": ai_result.get("opportunities", []),
                "score_details": ai_result.get("score_details", {}),
                "ai_analysis": ai_result.get("analysis", ""),
                "generated_by": "DeepSeek AI"
            }
            
            return summary
        
        return None
    
    def _format_data_for_ai(self, diagnosis: Dict, technical: Dict) -> str:
        """
        格式化数据供大模型分析
        
        Args:
            diagnosis: 问财诊股数据
            technical: 技术分析结果
        
        Returns:
            格式化后的字符串
        """
        data_parts = []
        
        # 1. 基本信息
        if technical and "error" not in technical:
            basic = technical.get('basic_info', {})
            data_parts.append(f"""【基本信息】
股票代码: {basic.get('stock_code', 'N/A')}
股票名称: {basic.get('stock_name', 'N/A')}
日期: {basic.get('date', 'N/A')}
当前价: {basic.get('close', 'N/A')} 元
涨跌幅: {basic.get('change_pct', 'N/A')}%
成交量: {basic.get('volume', 'N/A')} 手
换手率: {basic.get('turnover_rate', 'N/A')}%""")
        
        # 2. 技术指标
        if technical and "error" not in technical:
            ma = technical.get('technical_indicators', {}).get('ma', {})
            macd = technical.get('technical_indicators', {}).get('macd', {})
            kdj = technical.get('technical_indicators', {}).get('kdj', {})
            rsi = technical.get('technical_indicators', {}).get('rsi', {})
            sr = technical.get('support_resistance', {})
            
            data_parts.append(f"""【技术指标】
均线系统:
  趋势: {ma.get('trend', 'N/A')}
  排列: {ma.get('alignment', 'N/A')}
  MA5: {ma.get('ma5', 'N/A')}  MA10: {ma.get('ma10', 'N/A')}
  MA20: {ma.get('ma20', 'N/A')}  MA60: {ma.get('ma60', 'N/A')}

MACD指标:
  信号: {macd.get('signal', 'N/A')}
  DIF: {macd.get('dif', 'N/A')}  DEA: {macd.get('dea', 'N/A')}

KDJ指标:
  信号: {kdj.get('signal', 'N/A')}
  K: {kdj.get('k', 'N/A')}  D: {kdj.get('d', 'N/A')}  J: {kdj.get('j', 'N/A')}

RSI指标:
  RSI6: {rsi.get('rsi6', 'N/A')}  RSI12: {rsi.get('rsi12', 'N/A')}

支撑压力位:
  支撑位: {sr.get('support', 'N/A')} 元
  压力位: {sr.get('resistance', 'N/A')} 元
  当前价: {sr.get('current', 'N/A')} 元""")
        
        # 3. 资金面数据（如果有）
        if diagnosis:
            has_fund_data = any(key in diagnosis for key in [
                '历史主力资金流向', '北向资金流向情况', 'DDE散户数量变化'
            ])
            if has_fund_data:
                data_parts.append("【资金面】\n包含: 主力资金流向、北向资金、DDE散户数据")
        
        # 4. 基本面数据（如果有）
        if diagnosis:
            has_fundamental_data = any(key in diagnosis for key in [
                '财务数据', '估值指标', '十大股东持股比例'
            ])
            if has_fundamental_data:
                data_parts.append("【基本面】\n包含: 财务数据、估值指标、股东信息")
        
        # 5. 消息面数据（如果有）
        if diagnosis:
            has_news_data = any(key in diagnosis for key in [
                '重要新闻', '所属概念列表', '投顾点评'
            ])
            if has_news_data:
                data_parts.append("【消息面】\n包含: 重要新闻、概念题材、投顾点评")
        
        return "\n\n".join(data_parts)
    
    def _generate_rule_based_summary(self, diagnosis: Dict, technical: Dict) -> Dict:
        """
        使用规则生成分析摘要（原有逻辑）
        
        Args:
            diagnosis: 问财诊股数据
            technical: 技术分析结果
        
        Returns:
            规则生成的摘要
        """
        summary = {
            "overall_score": 0,
            "risk_level": "未知",
            "recommendation": "观望",
            "key_points": [],
            "risks": [],
            "opportunities": [],
            "generated_by": "Rule"
        }
        
        scores = []
        
        # 1. 技术面评分（权重40%）
        if technical and "error" not in technical:
            tech_score = self._evaluate_technical(technical, summary)
            scores.append(("技术面", tech_score, 0.4))
        
        # 2. 资金面评分（权重30%）
        if diagnosis:
            fund_score = self._evaluate_funds(diagnosis, summary)
            scores.append(("资金面", fund_score, 0.3))
        
        # 3. 基本面评分（权重20%）
        if diagnosis:
            fundamental_score = self._evaluate_fundamentals(diagnosis, summary)
            scores.append(("基本面", fundamental_score, 0.2))
        
        # 4. 消息面评分（权重10%）
        if diagnosis:
            news_score = self._evaluate_news(diagnosis, summary)
            scores.append(("消息面", news_score, 0.1))
        
        # 计算加权平均分
        if scores:
            total_score = sum(score * weight for _, score, weight in scores)
            summary["overall_score"] = round(total_score, 1)
            summary["score_details"] = {name: score for name, score, _ in scores}
        
        # 根据综合评分给出建议
        summary["recommendation"] = self._get_recommendation(summary["overall_score"])
        summary["risk_level"] = self._get_risk_level(summary["overall_score"])
        
        return summary
    
    def _evaluate_technical(self, technical: Dict, summary: Dict) -> float:
        """评估技术面，返回0-100分"""
        score = 50.0  # 基础分
        
        ma = technical['technical_indicators']['ma']
        macd = technical['technical_indicators']['macd']
        kdj = technical['technical_indicators']['kdj']
        
        # 均线趋势（30分）
        if ma['trend'] == "强势上涨":
            score += 30
            summary['key_points'].append("✓ 均线多头排列，趋势强劲")
        elif ma['trend'] == "弱势下跌":
            score -= 20
            summary['risks'].append("✗ 均线空头排列，趋势偏弱")
        else:
            summary['key_points'].append("○ 均线纠缠，震荡整理")
        
        # MACD信号（20分）
        if "金叉" in macd['signal']:
            score += 20
            summary['opportunities'].append("✓ MACD金叉，买入信号")
        elif "死叉" in macd['signal']:
            score -= 15
            summary['risks'].append("✗ MACD死叉，卖出信号")
        
        # KDJ信号（20分）
        if "买入" in kdj['signal'] or "金叉" in kdj['signal']:
            score += 15
            summary['opportunities'].append("✓ KDJ金叉向上")
        elif "超买" in kdj['signal']:
            score -= 10
            summary['risks'].append("⚠ KDJ超买，注意回调")
        elif "超卖" in kdj['signal']:
            score += 10
            summary['opportunities'].append("✓ KDJ超卖，可能反弹")
        
        return max(0, min(100, score))
    
    def _evaluate_funds(self, diagnosis: Dict, summary: Dict) -> float:
        """评估资金面，返回0-100分"""
        score = 50.0
        
        # 从诊股数据中提取资金信息（这里需要根据实际数据结构调整）
        if '历史主力资金流向' in diagnosis:
            summary['key_points'].append("○ 包含主力资金流向数据")
            score += 10
        
        if '北向资金流向情况' in diagnosis:
            summary['key_points'].append("○ 包含北向资金数据")
            score += 5
        
        if 'DDE散户数量变化' in diagnosis:
            summary['key_points'].append("○ 包含DDE散户数据")
            score += 5
        
        return max(0, min(100, score))
    
    def _evaluate_fundamentals(self, diagnosis: Dict, summary: Dict) -> float:
        """评估基本面，返回0-100分"""
        score = 50.0
        
        if '财务数据' in diagnosis:
            summary['key_points'].append("○ 包含财务数据")
            score += 15
        
        if '估值指标' in diagnosis:
            summary['key_points'].append("○ 包含估值指标")
            score += 10
        
        return max(0, min(100, score))
    
    def _evaluate_news(self, diagnosis: Dict, summary: Dict) -> float:
        """评估消息面，返回0-100分"""
        score = 50.0
        
        if '重要新闻' in diagnosis:
            summary['key_points'].append("○ 包含重要新闻")
            score += 10
        
        if '所属概念列表' in diagnosis:
            summary['key_points'].append("○ 包含概念题材")
            score += 10
        
        return max(0, min(100, score))
    
    def _get_recommendation(self, score: float) -> str:
        """根据评分给出操作建议"""
        if score >= 75:
            return "买入"
        elif score >= 60:
            return "持有"
        elif score >= 45:
            return "观望"
        else:
            return "规避"
    
    def _get_risk_level(self, score: float) -> str:
        """根据评分给出风险等级"""
        if score >= 70:
            return "低风险"
        elif score >= 50:
            return "中等风险"
        else:
            return "高风险"
    
    def generate_report(self, analysis_result: Dict, detailed: bool = True) -> str:
        """
        生成分析报告
        
        Args:
            analysis_result: analyze_stock返回的分析结果
            detailed: 是否生成详细报告
        
        Returns:
            格式化的报告文本
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"股票综合分析报告 - {analysis_result['stock_name']}({analysis_result['stock_code']})")
        lines.append("=" * 80)
        
        summary = analysis_result.get('summary', {})
        
        # 综合评分
        lines.append(f"\n【综合评分】{summary.get('overall_score', 0):.1f} 分")
        lines.append(f"风险等级：{summary.get('risk_level', '未知')}")
        lines.append(f"操作建议：{summary.get('recommendation', '观望')}")
        
        # 各维度评分
        if 'score_details' in summary:
            lines.append("\n【分项评分】")
            for name, score in summary['score_details'].items():
                lines.append(f"  {name}: {score:.1f} 分")

        # 关键要点
        if summary.get('key_points'):
            lines.append("\n【关键要点】")
            for point in summary['key_points']:
                lines.append(f"  {point}")

        # 机会提示
        if summary.get('opportunities'):
            lines.append("\n【机会提示】")
            for opp in summary['opportunities']:
                lines.append(f"  {opp}")

        # 风险提示
        if summary.get('risks'):
            lines.append("\n【风险提示】")
            for risk in summary['risks']:
                lines.append(f"  {risk}")

        # AI详细分析（如果有）
        if summary.get('ai_analysis'):
            lines.append("\n【AI详细分析】")
            lines.append(f"{summary['ai_analysis']}")

        # 分析方式标注
        if summary.get('generated_by'):
            lines.append(f"\n[分析方式: {summary['generated_by']}]")
        
        # 详细技术分析
        if detailed and analysis_result.get('technical_analysis'):
            tech = analysis_result['technical_analysis']
            if 'error' not in tech:
                lines.append(f"\n{'=' * 80}")
                lines.append("技术分析详情")
                lines.append("=" * 80)
                
                # 基本信息
                basic = tech['basic_info']
                lines.append(f"\n【基本信息】")
                lines.append(f"  日期: {basic['date']}")
                lines.append(f"  收盘价: {basic['close']} 元")
                lines.append(f"  涨跌幅: {basic['change_pct']}%")
                lines.append(f"  成交量: {basic['volume']:,} 手")
                lines.append(f"  换手率: {basic['turnover_rate']}%")
                
                # 均线系统
                ma = tech['technical_indicators']['ma']
                lines.append(f"\n【均线系统】")
                lines.append(f"  趋势: {ma['trend']}")
                lines.append(f"  排列: {ma['alignment']}")
                if 'ma5' in ma:
                    lines.append(f"  MA5: {ma['ma5']:.2f}  MA10: {ma['ma10']:.2f}")
                    lines.append(f"  MA20: {ma['ma20']:.2f}  MA60: {ma['ma60']:.2f}")
                
                # MACD
                macd = tech['technical_indicators']['macd']
                lines.append(f"\n【MACD】")
                lines.append(f"  信号: {macd['signal']}")
                if 'dif' in macd:
                    lines.append(f"  DIF: {macd['dif']}  DEA: {macd['dea']}  HIST: {macd['hist']}")
                
                # KDJ
                kdj = tech['technical_indicators']['kdj']
                lines.append(f"\n【KDJ】")
                lines.append(f"  信号: {kdj['signal']}")
                if 'k' in kdj:
                    lines.append(f"  K: {kdj['k']}  D: {kdj['d']}  J: {kdj['j']}")
                
                # 支撑压力位
                sr = tech['support_resistance']
                lines.append(f"\n【支撑压力位】")
                lines.append(f"  当前价: {sr['current']} 元")
                lines.append(f"  支撑位: {sr['support']} 元 (距离 {sr['support_distance']}%)")
                lines.append(f"  压力位: {sr['resistance']} 元 (距离 {sr['resistance_distance']}%)")
        
        lines.append("\n" + "=" * 80)
        lines.append("报告生成完成")
        lines.append("=" * 80)
        
        return "\n".join(lines)

