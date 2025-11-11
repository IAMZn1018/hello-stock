import os
import httpx
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from PIL import Image
import base64

# 加载环境变量
load_dotenv()

class QwenAPI:
    """Qwen大模型API调用类"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("QWEN_API_KEY")
        self.model = model or os.getenv("QWEN_MODEL", "qwen-max")
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_stock_image(self, image_path: str, query: str) -> Dict[str, Any]:
        """
        分析股票日线图片
        
        Args:
            image_path: 图片路径
            query: 用户查询问题
            
        Returns:
            分析结果字典
        """
        # 读取并编码图片
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 构造请求数据
        payload = {
            "model": self.model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "image": f"data:image/jpeg;base64,{encoded_image}"
                            },
                            {
                                "text": f"请分析这张股票日线图，并回答以下问题: {query}"
                            }
                        ]
                    }
                ]
            },
            "parameters": {
                "temperature": 0.5,
                "max_tokens": 2000
            }
        }
        
        # 发送请求
        try:
            response = httpx.post(
                f"{self.base_url}/services/aigc/text-generation/generation",
                headers=self._get_headers(),
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "success": True,
                "data": result.get("output", {}).get("text", ""),
                "raw_response": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def chat_with_context(self, messages: list, context: Optional[str] = None) -> Dict[str, Any]:
        """
        带上下文的对话
        
        Args:
            messages: 对话消息列表
            context: 上下文信息
            
        Returns:
            对话结果字典
        """
        # 如果有上下文，添加到消息开头
        if context:
            messages.insert(0, {
                "role": "system",
                "content": f"以下是相关的上下文信息：{context}"
            })
        
        # 构造请求数据
        payload = {
            "model": self.model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 1500
            }
        }
        
        # 发送请求
        try:
            response = httpx.post(
                f"{self.base_url}/services/aigc/text-generation/generation",
                headers=self._get_headers(),
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "success": True,
                "data": result.get("output", {}).get("text", ""),
                "raw_response": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def analyze_stock_data(self, stock_data: str) -> Dict[str, Any]:
        """
        分析股票数据并生成综合评价
        
        Args:
            stock_data: 格式化后的股票数据（包含技术指标、资金面、基本面等）
            
        Returns:
            分析结果字典，包含评分、建议、关键要点等
        """
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
4. analysis提供详细的分析逻辑
5. 确保输出的是有效的JSON格式"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"请分析以下股票数据：\n\n{stock_data}\n\n请严格按照JSON格式输出分析结果。"
            }
        ]
        
        payload = {
            "model": self.model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": 0.3,  # 降低随机性，提高稳定性
                "max_tokens": 2000
            }
        }
        
        try:
            response = httpx.post(
                f"{self.base_url}/services/aigc/text-generation/generation",
                headers=self._get_headers(),
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
            # 提取生成的文本
            generated_text = result.get("output", {}).get("text", "")
            
            # 尝试解析JSON
            import json
            import re
            
            # 提取JSON部分（可能包含在```json```代码块中）
            json_match = re.search(r'```json\s*(.*?)\s*```', generated_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # 尝试直接找JSON对象
                json_match = re.search(r'\{.*\}', generated_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    json_str = generated_text
            
            try:
                analysis_result = json.loads(json_str)
                return {
                    "success": True,
                    "data": analysis_result,
                    "raw_text": generated_text
                }
            except json.JSONDecodeError as e:
                # 如果JSON解析失败，返回原始文本
                return {
                    "success": False,
                    "error": f"JSON解析失败: {str(e)}",
                    "raw_text": generated_text,
                    "data": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

# 创建全局实例
qwen_api = QwenAPI()