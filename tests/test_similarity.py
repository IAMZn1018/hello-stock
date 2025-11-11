#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
相似度计算工具模块单元测试
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.similarity import cosine_similarity, find_most_similar_context

class TestSimilarity(unittest.TestCase):
    """相似度计算函数测试用例"""
    
    def test_cosine_similarity_exact_match(self):
        """测试余弦相似度完全匹配情况"""
        text1 = "科技股近期表现不错"
        text2 = "科技股近期表现不错"
        similarity = cosine_similarity(text1, text2)
        self.assertEqual(similarity, 1.0)
    
    def test_cosine_similarity_no_match(self):
        """测试余弦相似度无匹配情况"""
        text1 = "科技股近期表现不错"
        text2 = "银行股近期表现不佳"
        similarity = cosine_similarity(text1, text2)
        # 由于没有共同词汇，相似度应该为0
        self.assertEqual(similarity, 0.0)
    
    def test_cosine_similarity_partial_match(self):
        """测试余弦相似度部分匹配情况"""
        text1 = "科技股近期表现不错"
        text2 = "科技股近期走势强劲"
        similarity = cosine_similarity(text1, text2)
        # 应该有一定的相似度，但不是完全匹配
        self.assertGreater(similarity, 0.0)
        self.assertLess(similarity, 1.0)
    
    def test_find_most_similar_context_success(self):
        """测试查找最相似上下文成功情况"""
        query = "科技股现在适合买入吗？"
        contexts = [
            "user: 我关注的是科技股",
            "assistant: 科技股近期表现不错，但要注意风险",
            "user: 我的持仓成本是50元",
            "assistant: 建议设置止损位在45元"
        ]
        
        most_similar = find_most_similar_context(query, contexts)
        
        # 验证返回结果是一个列表
        self.assertIsInstance(most_similar, list)
        # 验证列表中的元素是元组
        if most_similar:
            self.assertIsInstance(most_similar[0], tuple)
    
    def test_find_most_similar_context_empty_contexts(self):
        """测试查找最相似上下文空上下文情况"""
        query = "科技股现在适合买入吗？"
        contexts = []
        
        most_similar = find_most_similar_context(query, contexts)
        
        # 验证返回结果为空列表
        self.assertEqual(most_similar, [])
    
    def test_find_most_similar_context_no_similar(self):
        """测试查找最相似上下文无相似情况"""
        query = "科技股现在适合买入吗？"
        contexts = [
            "user: 我关注的是银行股",
            "assistant: 银行股近期表现不佳",
            "user: 我的持仓成本是10元",
            "assistant: 建议设置止损位在9元"
        ]
        
        most_similar = find_most_similar_context(query, contexts)
        
        # 验证返回结果是一个列表
        self.assertIsInstance(most_similar, list)

if __name__ == '__main__':
    unittest.main()