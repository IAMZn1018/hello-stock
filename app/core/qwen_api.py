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

# 创建全局实例
qwen_api = QwenAPI()