#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Qwen API模块单元测试
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.qwen_api import QwenAPI

class TestQwenAPI(unittest.TestCase):
    """QwenAPI类测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.api_key = "test_api_key"
        self.model = "qwen-max"
        self.qwen_api = QwenAPI(self.api_key, self.model)
    
    @patch('app.core.qwen_api.httpx.post')
    def test_analyze_stock_image_success(self, mock_post):
        """测试股票图片分析成功情况"""
        # 模拟HTTP响应
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "output": {
                "text": "这是一个上升趋势的股票图表，建议买入。"
            }
        }
        mock_post.return_value = mock_response
        
        # 调用被测试的方法
        result = self.qwen_api.analyze_stock_image("test_image_path.png", "请分析这张股票图表")
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["data"], "这是一个上升趋势的股票图表，建议买入。")
        mock_post.assert_called_once()
    
    @patch('app.core.qwen_api.httpx.post')
    def test_analyze_stock_image_http_error(self, mock_post):
        """测试股票图片分析HTTP错误情况"""
        # 模拟HTTP错误
        mock_post.side_effect = Exception("HTTP Error")
        
        # 调用被测试的方法
        result = self.qwen_api.analyze_stock_image("test_image_path.png", "请分析这张股票图表")
        
        # 验证结果
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "HTTP Error")
    
    @patch('app.core.qwen_api.httpx.post')
    def test_chat_with_context_success(self, mock_post):
        """测试带上下文对话成功情况"""
        # 模拟HTTP响应
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "output": {
                "text": "根据市场分析，建议您关注科技板块。"
            }
        }
        mock_post.return_value = mock_response
        
        # 调用被测试的方法
        messages = [
            {"role": "user", "content": "我应该关注哪些板块？"}
        ]
        result = self.qwen_api.chat_with_context(messages)
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["data"], "根据市场分析，建议您关注科技板块。")
        mock_post.assert_called_once()
    
    @patch('app.core.qwen_api.httpx.post')
    def test_chat_with_context_http_error(self, mock_post):
        """测试带上下文对话HTTP错误情况"""
        # 模拟HTTP错误
        mock_post.side_effect = Exception("Network Error")
        
        # 调用被测试的方法
        messages = [
            {"role": "user", "content": "我应该关注哪些板块？"}
        ]
        result = self.qwen_api.chat_with_context(messages)
        
        # 验证结果
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Network Error")

if __name__ == '__main__':
    unittest.main()