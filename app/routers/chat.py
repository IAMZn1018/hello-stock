from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.base import get_db
from app.schemas import chat as schemas
from app.models import chat as models
from app.core.qwen_api import qwen_api
from app.utils.similarity import find_most_similar_context

router = APIRouter()

@router.post("/sessions/", response_model=schemas.ChatSession)
async def create_chat_session(session: schemas.ChatSessionCreate, db: Session = Depends(get_db)):
    """
    创建新的聊天会话
    """
    db_session = models.ChatSession(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.post("/messages/", response_model=schemas.ChatMessage)
async def create_chat_message(message: schemas.ChatMessageCreate, db: Session = Depends(get_db)):
    """
    创建新的聊天消息
    """
    # 更新会话的更新时间
    db_session = db.query(models.ChatSession).filter(
        models.ChatSession.id == message.session_id
    ).first()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="会话未找到")
    
    # 保存消息
    db_message = models.ChatMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.post("/query/", response_model=dict)
async def chat_with_context(query: schemas.ChatQuery, db: Session = Depends(get_db)):
    """
    带上下文的智能对话
    """
    # 创建或获取会话
    db_session = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == query.user_id
    ).first()
    
    if not db_session:
        db_session = models.ChatSession(user_id=query.user_id)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
    
    # 保存用户消息
    user_message = models.ChatMessage(
        session_id=db_session.id,
        role="user",
        content=query.query,
        image_path=query.image_path
    )
    db.add(user_message)
    
    # 获取相关上下文
    context = get_relevant_context(db, query.user_id, query.query)
    
    # 构造对话历史
    messages = []
    if context:
        messages.append({"role": "system", "content": f"相关历史对话: {context}"})
    
    # 添加用户当前问题
    content = query.query
    if query.image_path:
        content += f" (附图片: {query.image_path})"
    
    messages.append({"role": "user", "content": content})
    
    # 调用大模型API
    result = qwen_api.chat_with_context(messages)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=f"对话失败: {result['error']}")
    
    # 保存助手回复
    assistant_message = models.ChatMessage(
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
        "session_id": db_session.id,
        "user_message_id": user_message.id,
        "assistant_message_id": assistant_message.id,
        "response": result["data"]
    }

def get_relevant_context(db: Session, user_id: str, current_query: str) -> str:
    """
    获取最相关的聊天记录作为上下文
    """
    # 获取用户最近的聊天记录
    recent_messages = db.query(models.ChatMessage).join(
        models.ChatSession
    ).filter(
        models.ChatSession.user_id == user_id
    ).order_by(
        models.ChatMessage.created_at.desc()
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

@router.get("/sessions/{user_id}/history", response_model=List[schemas.ChatMessage])
async def get_chat_history(user_id: str, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取用户聊天历史
    """
    messages = db.query(models.ChatMessage).join(
        models.ChatSession
    ).filter(
        models.ChatSession.user_id == user_id
    ).order_by(
        models.ChatMessage.created_at.desc()
    ).limit(limit).all()
    
    return messages