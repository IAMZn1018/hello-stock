#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话管理Agent
"""

import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
from utils.database import get_db_session, close_db_session
import sys
sys.path.append('../app')
from core.qwen_api import qwen_api
from models.chat import ChatSession, ChatMessage
from utils.similarity import find_most_similar_context

class ChatManagementAgent(AgentBase):
    """对话管理Agent，负责管理用户与系统的对话交互"""
    
    def __init__(self, name: str = "ChatManagementAgent") -> None:
        """初始化对话管理Agent"""
        super().__init__(name=name)
        
    def create_chat_session(self, user_id: str) -> dict:
        """
        创建新的聊天会话
        
        Args:
            user_id (str): 用户ID
            
        Returns:
            dict: 会话信息
        """
        db = get_db_session()
        try:
            db_session = ChatSession(user_id=user_id)
            db.add(db_session)
            db.commit()
            db.refresh(db_session)
            
            return {
                "success": True,
                "data": {
                    "session_id": db_session.id,
                    "user_id": db_session.user_id,
                    "created_at": db_session.created_at
                }
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"创建会话失败: {str(e)}"
            }
        finally:
            close_db_session(db)
    
    def save_chat_message(self, session_id: int, role: str, content: str, image_path: str = None) -> dict:
        """
        保存聊天消息
        
        Args:
            session_id (int): 会话ID
            role (str): 角色(user/assistant)
            content (str): 消息内容
            image_path (str): 图片路径(可选)
            
        Returns:
            dict: 消息信息
        """
        db = get_db_session()
        try:
            # 更新会话的更新时间
            db_session = db.query(ChatSession).filter(
                ChatSession.id == session_id
            ).first()
            
            if not db_session:
                return {
                    "success": False,
                    "error": "会话未找到"
                }
            
            # 保存消息
            db_message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content,
                image_path=image_path
            )
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            
            return {
                "success": True,
                "data": {
                    "message_id": db_message.id,
                    "session_id": db_message.session_id,
                    "role": db_message.role,
                    "content": db_message.content,
                    "image_path": db_message.image_path,
                    "created_at": db_message.created_at
                }
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"保存消息失败: {str(e)}"
            }
        finally:
            close_db_session(db)
    
    def chat_with_context(self, user_id: str, query: str, image_path: str = None) -> dict:
        """
        带上下文的智能对话
        
        Args:
            user_id (str): 用户ID
            query (str): 用户查询
            image_path (str): 图片路径(可选)
            
        Returns:
            dict: 对话结果
        """
        db = get_db_session()
        try:
            # 创建或获取会话
            db_session = db.query(ChatSession).filter(
                ChatSession.user_id == user_id
            ).first()
            
            if not db_session:
                db_session = ChatSession(user_id=user_id)
                db.add(db_session)
                db.commit()
                db.refresh(db_session)
            
            # 保存用户消息
            user_message = ChatMessage(
                session_id=db_session.id,
                role="user",
                content=query,
                image_path=image_path
            )
            db.add(user_message)
            
            # 获取相关上下文
            context = self._get_relevant_context(db, user_id, query)
            
            # 构造对话历史
            messages = []
            if context:
                messages.append({"role": "system", "content": f"相关历史对话: {context}"})
            
            # 添加用户当前问题
            content = query
            if image_path:
                content += f" (附图片: {image_path})"
            
            messages.append({"role": "user", "content": content})
            
            # 调用大模型API
            result = qwen_api.chat_with_context(messages)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"对话失败: {result['error']}"
                }
            
            # 保存助手回复
            assistant_message = ChatMessage(
                session_id=db_session.id,
                role="assistant",
                content=result["data"]
            )
            db.add(assistant_message)
            
            # 提交所有更改
            db.commit()
            db.refresh(user_message)
            db.refresh(assistant_message)
            
            return {
                "success": True,
                "data": {
                    "session_id": db_session.id,
                    "user_message_id": user_message.id,
                    "assistant_message_id": assistant_message.id,
                    "response": result["data"]
                }
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"对话处理失败: {str(e)}"
            }
        finally:
            close_db_session(db)
    
    def _get_relevant_context(self, db, user_id: str, current_query: str) -> str:
        """
        获取最相关的聊天记录作为上下文
        
        Args:
            db: 数据库会话
            user_id (str): 用户ID
            current_query (str): 当前查询
            
        Returns:
            str: 相关上下文
        """
        # 获取用户最近的聊天记录
        recent_messages = db.query(ChatMessage).join(
            ChatSession
        ).filter(
            ChatSession.user_id == user_id
        ).order_by(
            ChatMessage.created_at.desc()
        ).limit(20).all()
        
        if not recent_messages:
            return ""
        
        # 将消息转换为文本列表
        contexts = []
        for msg in recent_messages:
            contexts.append(f"{msg.role}: {msg.content}")
        
        # 使用相似度算法找到最相关的上下文
        similar_contexts = find_most_similar_context(current_query, contexts, top_k=3)
        
        # 组合最相关的上下文
        relevant_contexts = []
        for idx, similarity in similar_contexts:
            if similarity > 0.1:  # 相似度阈值
                relevant_contexts.append(contexts[idx])
        
        return " | ".join(relevant_contexts)
    
    def reply(self, x: dict = None) -> dict:
        """
        Agent回复方法
        
        Args:
            x (dict): 输入消息
            
        Returns:
            dict: 回复消息
        """
        if x is None:
            return Msg(self.name, "请提供对话内容", "assistant")
        
        # 解析输入消息
        if isinstance(x, Msg):
            content = x.content
        else:
            content = x
            
        # 如果内容包含用户ID和查询，则进行对话
        if isinstance(content, dict) and "user_id" in content and "query" in content:
            result = self.chat_with_context(
                content["user_id"], 
                content["query"],
                content.get("image_path")
            )
            return Msg(self.name, result, "assistant")
        else:
            return Msg(self.name, "请提供有效的用户ID和查询内容", "assistant")