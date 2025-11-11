from fastapi import FastAPI
from app.routers import stock, chat, risk, market
from app.database import init_db

app = FastAPI(
    title="Hello Stock - AI股票分析助手",
    description="基于大模型的股票分析和交易助手系统",
    version="1.0.0"
)

# 初始化数据库
init_db()

# 注册路由
app.include_router(stock.router, prefix="/api/stock", tags=["股票分析"])
app.include_router(chat.router, prefix="/api/chat", tags=["对话管理"])
app.include_router(risk.router, prefix="/api/risk", tags=["风险控制"])
app.include_router(market.router, prefix="/api/market", tags=["市场分析"])

@app.get("/")
async def root():
    return {"message": "欢迎使用Hello Stock - AI股票分析助手"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}