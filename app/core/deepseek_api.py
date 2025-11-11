"""
DeepSeek API 封装
用于调用 DeepSeek 大模型进行股票分析
"""
import os
import requests
import json
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class DeepSeekAPI:
    """DeepSeek 大模型 API 调用类"""
    
    def __init__(self, api_key: str = None):
        """
        初始化 DeepSeek API
        
        Args:
            api_key: API密钥，如果不提供则从环境变量读取
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.timeout = 60.0
        
        if not self.api_key:
            print("警告: 未配置 DeepSeek API 密钥")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_stock_data(self, stock_data: str) -> Dict[str, Any]:
        """
        分析股票数据并生成综合评价
        
        Args:
            stock_data: 格式化后的股票数据
            
        Returns:
            分析结果字典，包含评分、建议、关键要点等
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "未配置 DeepSeek API 密钥",
                "data": None
            }
        
        system_prompt = """你是一位资深的股票分析师，擅长从多个维度综合分析股票。
请根据提供的数据，进行专业的股票分析，并按以下JSON格式输出：

{
  "overall_score": 75.5,
  "risk_level": "中等风险",
  "recommendation": "持有",
  "key_points": ["关键要点1", "关键要点2", "关键要点3"],
  "opportunities": ["机会提示1", "机会提示2"],
  "risks": ["风险提示1", "风险提示2"],
  "analysis": "详细的分析说明...",
  "score_details": {
    "技术面": 70.0,
    "资金面": 75.0,
    "基本面": 80.0,
    "消息面": 75.0
  }
}

评分标准：
- overall_score: 0-100分的综合评分
- risk_level: 低风险、中等风险、高风险
- recommendation: 买入、持有、观望、规避
- 技术面(权重40%): 考虑MA/MACD/KDJ/RSI等指标
- 资金面(权重30%): 考虑主力资金、北向资金、DDE等
- 基本面(权重20%): 考虑财务数据、估值指标
- 消息面(权重10%): 考虑新闻、概念题材

要求：
1. 综合评分要客观，基于数据分析
2. key_points列出3-5个最重要的观察点
3. opportunities和risks分别列出2-4个具体的机会和风险
4. analysis提供详细的分析逻辑和操作建议
5. 必须输出有效的JSON格式，不要有其他文字"""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"请分析以下股票数据：\n\n{stock_data}\n\n严格按照JSON格式输出。"
                }
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # 提取生成的文本
            if 'choices' in result and len(result['choices']) > 0:
                generated_text = result['choices'][0]['message']['content']
            else:
                return {
                    "success": False,
                    "error": "API返回格式错误",
                    "data": None
                }
            
            # 尝试解析JSON
            json_str = self._extract_json(generated_text)
            
            try:
                analysis_result = json.loads(json_str)
                return {
                    "success": True,
                    "data": analysis_result,
                    "raw_text": generated_text
                }
            except json.JSONDecodeError as e:
                # JSON解析失败，返回原始文本
                return {
                    "success": False,
                    "error": f"JSON解析失败: {str(e)}",
                    "raw_text": generated_text,
                    "data": None
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "请求超时",
                "data": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"请求失败: {str(e)}",
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"未知错误: {str(e)}",
                "data": None
            }
    
    def _extract_json(self, text: str) -> str:
        """
        从文本中提取JSON部分
        
        Args:
            text: 包含JSON的文本
            
        Returns:
            JSON字符串
        """
        # 尝试提取```json```代码块
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # 尝试提取```代码块
        json_match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # 尝试直接找JSON对象
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        # 如果都找不到，返回原文本
        return text
    
    def chat(self, message: str, system_prompt: str = None) -> Dict[str, Any]:
        """
        简单对话接口
        
        Args:
            message: 用户消息
            system_prompt: 系统提示词
            
        Returns:
            对话结果
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "未配置 DeepSeek API 密钥",
                "data": None
            }
        
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": message
        })
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                return {
                    "success": True,
                    "data": content,
                    "raw_response": result
                }
            else:
                return {
                    "success": False,
                    "error": "API返回格式错误",
                    "data": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }


# 创建全局实例
deepseek_api = DeepSeekAPI()

