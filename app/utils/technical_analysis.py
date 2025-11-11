"""
技术分析模块
提供K线数据解析和技术指标计算功能
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class KLineParser:
    """K线数据解析器"""
    
    @staticmethod
    def parse_kline_data(kline_response: Dict) -> pd.DataFrame:
        """
        解析东方财富K线数据
        
        Args:
            kline_response: 东方财富API返回的K线数据
        
        Returns:
            包含K线数据的DataFrame
            
        Example:
            >>> parser = KLineParser()
            >>> df = parser.parse_kline_data(response_data)
        """
        if 'data' not in kline_response or 'klines' not in kline_response['data']:
            return pd.DataFrame()
        
        klines = kline_response['data']['klines']
        stock_name = kline_response['data'].get('name', '')
        stock_code = kline_response['data'].get('code', '')
        
        # 解析K线数据
        data_list = []
        for kline in klines:
            parts = kline.split(',')
            if len(parts) >= 11:
                data_list.append({
                    'date': parts[0],
                    'open': float(parts[1]),
                    'close': float(parts[2]),
                    'high': float(parts[3]),
                    'low': float(parts[4]),
                    'volume': float(parts[5]),
                    'amount': float(parts[6]),
                    'amplitude': float(parts[7]),
                    'change_pct': float(parts[8]),
                    'change_amount': float(parts[9]),
                    'turnover_rate': float(parts[10])
                })
        
        df = pd.DataFrame(data_list)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['stock_name'] = stock_name
            df['stock_code'] = stock_code
        
        return df


class TechnicalIndicators:
    """技术指标计算器"""
    
    @staticmethod
    def calculate_ma(df: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> pd.DataFrame:
        """
        计算移动平均线
        
        Args:
            df: K线数据DataFrame
            periods: 均线周期列表
        
        Returns:
            添加了均线列的DataFrame
        """
        for period in periods:
            df[f'ma{period}'] = df['close'].rolling(window=period).mean()
        return df
    
    @staticmethod
    def calculate_macd(df: pd.DataFrame, fast=12, slow=26, signal=9) -> pd.DataFrame:
        """
        计算MACD指标
        
        Args:
            df: K线数据DataFrame
            fast: 快线周期
            slow: 慢线周期
            signal: 信号线周期
        
        Returns:
            添加了MACD指标的DataFrame
        """
        # 计算EMA
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
        
        # MACD线（DIF）
        df['macd_dif'] = ema_fast - ema_slow
        
        # 信号线（DEA）
        df['macd_dea'] = df['macd_dif'].ewm(span=signal, adjust=False).mean()
        
        # MACD柱状图
        df['macd_hist'] = (df['macd_dif'] - df['macd_dea']) * 2
        
        return df
    
    @staticmethod
    def calculate_kdj(df: pd.DataFrame, n=9, m1=3, m2=3) -> pd.DataFrame:
        """
        计算KDJ指标
        
        Args:
            df: K线数据DataFrame
            n: RSV周期
            m1: K值平滑周期
            m2: D值平滑周期
        
        Returns:
            添加了KDJ指标的DataFrame
        """
        # 计算RSV
        low_min = df['low'].rolling(window=n).min()
        high_max = df['high'].rolling(window=n).max()
        df['rsv'] = (df['close'] - low_min) / (high_max - low_min) * 100
        
        # 计算K值
        df['kdj_k'] = df['rsv'].ewm(com=m1-1, adjust=False).mean()
        
        # 计算D值
        df['kdj_d'] = df['kdj_k'].ewm(com=m2-1, adjust=False).mean()
        
        # 计算J值
        df['kdj_j'] = 3 * df['kdj_k'] - 2 * df['kdj_d']
        
        # 删除临时列
        df.drop('rsv', axis=1, inplace=True)
        
        return df
    
    @staticmethod
    def calculate_rsi(df: pd.DataFrame, periods: List[int] = [6, 12, 24]) -> pd.DataFrame:
        """
        计算RSI指标
        
        Args:
            df: K线数据DataFrame
            periods: RSI周期列表
        
        Returns:
            添加了RSI指标的DataFrame
        """
        for period in periods:
            # 计算价格变动
            delta = df['close'].diff()
            
            # 分离上涨和下跌
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            # 计算平均涨跌
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            
            # 计算RSI
            rs = avg_gain / avg_loss
            df[f'rsi{period}'] = 100 - (100 / (1 + rs))
        
        return df
    
    @staticmethod
    def calculate_boll(df: pd.DataFrame, period=20, std_multiplier=2) -> pd.DataFrame:
        """
        计算布林带指标
        
        Args:
            df: K线数据DataFrame
            period: 周期
            std_multiplier: 标准差倍数
        
        Returns:
            添加了布林带指标的DataFrame
        """
        # 中轨（移动平均线）
        df['boll_mid'] = df['close'].rolling(window=period).mean()
        
        # 标准差
        std = df['close'].rolling(window=period).std()
        
        # 上轨
        df['boll_upper'] = df['boll_mid'] + std_multiplier * std
        
        # 下轨
        df['boll_lower'] = df['boll_mid'] - std_multiplier * std
        
        return df
    
    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        计算所有技术指标
        
        Args:
            df: K线数据DataFrame
        
        Returns:
            添加了所有技术指标的DataFrame
        """
        if df.empty:
            return df
        
        df = TechnicalIndicators.calculate_ma(df)
        df = TechnicalIndicators.calculate_macd(df)
        df = TechnicalIndicators.calculate_kdj(df)
        df = TechnicalIndicators.calculate_rsi(df)
        df = TechnicalIndicators.calculate_boll(df)
        
        return df


class TrendAnalyzer:
    """趋势分析器"""
    
    @staticmethod
    def analyze_ma_trend(df: pd.DataFrame) -> Dict[str, str]:
        """
        分析均线趋势
        
        Args:
            df: K线数据DataFrame（需包含均线数据）
        
        Returns:
            均线趋势分析结果
        """
        if df.empty or len(df) < 60:
            return {"trend": "数据不足", "alignment": "未知"}
        
        latest = df.iloc[-1]
        
        # 判断均线排列
        ma5 = latest.get('ma5', 0)
        ma10 = latest.get('ma10', 0)
        ma20 = latest.get('ma20', 0)
        ma60 = latest.get('ma60', 0)
        
        # 多头排列：短期均线 > 长期均线
        if ma5 > ma10 > ma20 > ma60:
            alignment = "多头排列"
            trend = "强势上涨"
        # 空头排列：短期均线 < 长期均线
        elif ma5 < ma10 < ma20 < ma60:
            alignment = "空头排列"
            trend = "弱势下跌"
        else:
            alignment = "均线纠缠"
            trend = "震荡整理"
        
        return {
            "trend": trend,
            "alignment": alignment,
            "ma5": ma5,
            "ma10": ma10,
            "ma20": ma20,
            "ma60": ma60
        }
    
    @staticmethod
    def analyze_macd_signal(df: pd.DataFrame) -> Dict[str, str]:
        """
        分析MACD信号
        
        Args:
            df: K线数据DataFrame（需包含MACD数据）
        
        Returns:
            MACD信号分析结果
        """
        if df.empty or len(df) < 2:
            return {"signal": "数据不足"}
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        dif = latest['macd_dif']
        dea = latest['macd_dea']
        hist = latest['macd_hist']
        
        prev_dif = prev['macd_dif']
        prev_dea = prev['macd_dea']
        
        # 判断金叉死叉
        if prev_dif <= prev_dea and dif > dea:
            signal = "金叉 - 买入信号"
        elif prev_dif >= prev_dea and dif < dea:
            signal = "死叉 - 卖出信号"
        elif dif > dea and hist > 0:
            signal = "多头 - 持有"
        elif dif < dea and hist < 0:
            signal = "空头 - 观望"
        else:
            signal = "震荡 - 等待"
        
        return {
            "signal": signal,
            "dif": round(dif, 3),
            "dea": round(dea, 3),
            "hist": round(hist, 3)
        }
    
    @staticmethod
    def analyze_kdj_signal(df: pd.DataFrame) -> Dict[str, str]:
        """
        分析KDJ信号
        
        Args:
            df: K线数据DataFrame（需包含KDJ数据）
        
        Returns:
            KDJ信号分析结果
        """
        if df.empty:
            return {"signal": "数据不足"}
        
        latest = df.iloc[-1]
        
        k = latest['kdj_k']
        d = latest['kdj_d']
        j = latest['kdj_j']
        
        # 判断超买超卖
        if k > 80 and d > 80:
            signal = "超买 - 注意回调风险"
        elif k < 20 and d < 20:
            signal = "超卖 - 可能反弹"
        elif k > d and j > k:
            signal = "金叉向上 - 买入"
        elif k < d and j < k:
            signal = "死叉向下 - 卖出"
        else:
            signal = "震荡 - 观望"
        
        return {
            "signal": signal,
            "k": round(k, 2),
            "d": round(d, 2),
            "j": round(j, 2)
        }
    
    @staticmethod
    def get_support_resistance(df: pd.DataFrame, days=60) -> Dict[str, float]:
        """
        计算支撑位和压力位
        
        Args:
            df: K线数据DataFrame
            days: 回看天数
        
        Returns:
            支撑位和压力位
        """
        if df.empty:
            return {"support": 0, "resistance": 0}
        
        # 取最近N天的数据
        recent_df = df.tail(days)
        
        # 支撑位：近期最低价
        support = recent_df['low'].min()
        
        # 压力位：近期最高价
        resistance = recent_df['high'].max()
        
        # 当前价
        current_price = df.iloc[-1]['close']
        
        return {
            "support": round(support, 2),
            "resistance": round(resistance, 2),
            "current": round(current_price, 2),
            "support_distance": round((current_price - support) / current_price * 100, 2),
            "resistance_distance": round((resistance - current_price) / current_price * 100, 2)
        }


class StockAnalyzer:
    """股票综合分析器"""
    
    def __init__(self):
        self.parser = KLineParser()
        self.indicators = TechnicalIndicators()
        self.trend_analyzer = TrendAnalyzer()
    
    def analyze(self, kline_response: Dict) -> Dict:
        """
        综合分析股票
        
        Args:
            kline_response: 东方财富K线API响应
        
        Returns:
            综合分析结果
        """
        # 解析K线数据
        df = self.parser.parse_kline_data(kline_response)
        if df.empty:
            return {"error": "K线数据为空"}
        
        # 计算技术指标
        df = self.indicators.calculate_all_indicators(df)
        
        # 趋势分析
        ma_trend = self.trend_analyzer.analyze_ma_trend(df)
        macd_signal = self.trend_analyzer.analyze_macd_signal(df)
        kdj_signal = self.trend_analyzer.analyze_kdj_signal(df)
        support_resistance = self.trend_analyzer.get_support_resistance(df)
        
        # 获取最新数据
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        # 构建分析结果
        result = {
            "basic_info": {
                "stock_code": latest['stock_code'],
                "stock_name": latest['stock_name'],
                "date": latest['date'].strftime('%Y-%m-%d'),
                "close": round(latest['close'], 2),
                "change_pct": round(latest['change_pct'], 2),
                "volume": int(latest['volume']),
                "amount": round(latest['amount'], 2),
                "turnover_rate": round(latest['turnover_rate'], 2)
            },
            "technical_indicators": {
                "ma": ma_trend,
                "macd": macd_signal,
                "kdj": kdj_signal,
                "rsi": {
                    "rsi6": round(latest.get('rsi6', 0), 2),
                    "rsi12": round(latest.get('rsi12', 0), 2),
                    "rsi24": round(latest.get('rsi24', 0), 2)
                },
                "boll": {
                    "upper": round(latest.get('boll_upper', 0), 2),
                    "mid": round(latest.get('boll_mid', 0), 2),
                    "lower": round(latest.get('boll_lower', 0), 2)
                }
            },
            "support_resistance": support_resistance,
            "dataframe": df  # 保留完整数据供进一步分析
        }
        
        return result
    
    def get_trade_suggestion(self, analysis_result: Dict) -> str:
        """
        根据分析结果给出交易建议
        
        Args:
            analysis_result: 分析结果
        
        Returns:
            交易建议文本
        """
        if "error" in analysis_result:
            return "数据不足，无法给出建议"
        
        ma_trend = analysis_result['technical_indicators']['ma']['trend']
        macd_signal = analysis_result['technical_indicators']['macd']['signal']
        kdj_signal = analysis_result['technical_indicators']['kdj']['signal']
        
        suggestions = []
        
        # 根据各指标给建议
        if "多头" in ma_trend:
            suggestions.append("均线多头排列，趋势向好")
        elif "空头" in ma_trend:
            suggestions.append("均线空头排列，谨慎操作")
        
        if "金叉" in macd_signal:
            suggestions.append("MACD金叉，买入信号")
        elif "死叉" in macd_signal:
            suggestions.append("MACD死叉，卖出信号")
        
        if "超买" in kdj_signal:
            suggestions.append("KDJ超买，注意回调")
        elif "超卖" in kdj_signal:
            suggestions.append("KDJ超卖，关注反弹")
        
        return "；".join(suggestions) if suggestions else "震荡行情，观望为主"

