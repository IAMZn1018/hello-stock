import math
from typing import List, Tuple
from collections import Counter

def cosine_similarity(text1: str, text2: str) -> float:
    """
    计算两个文本之间的余弦相似度
    
    Args:
        text1: 第一个文本
        text2: 第二个文本
        
    Returns:
        余弦相似度值 (0-1之间)
    """
    # 分词并转换为小写
    words1 = text1.lower().split()
    words2 = text2.lower().split()
    
    # 创建词频向量
    vec1 = Counter(words1)
    vec2 = Counter(words2)
    
    # 获取所有唯一词汇
    all_words = set(vec1.keys()) | set(vec2.keys())
    
    # 构建向量
    vector1 = [vec1.get(word, 0) for word in all_words]
    vector2 = [vec2.get(word, 0) for word in all_words]
    
    # 计算点积
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    
    # 计算向量的模
    magnitude1 = math.sqrt(sum(a * a for a in vector1))
    magnitude2 = math.sqrt(sum(b * b for b in vector2))
    
    # 避免除零错误
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # 计算余弦相似度
    return dot_product / (magnitude1 * magnitude2)

def find_most_similar_context(query: str, contexts: List[str], top_k: int = 3) -> List[Tuple[int, float]]:
    """
    在上下文列表中找到与查询最相似的几个上下文
    
    Args:
        query: 查询文本
        contexts: 上下文列表
        top_k: 返回最相似的前k个上下文
        
    Returns:
        包含(索引, 相似度)元组的列表，按相似度降序排列
    """
    similarities = []
    
    for i, context in enumerate(contexts):
        similarity = cosine_similarity(query, context)
        similarities.append((i, similarity))
    
    # 按相似度降序排序并返回前top_k个
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]