# src/chatbot/__init__.py
from fastapi import FastAPI
from .router import router
from .retriever import STATE, load_state

def setup(app: FastAPI) -> None:
    # 掛上 /api 路由
    app.include_router(router)

    # 啟動時把資料/embedding 載入（只做一次）
    @app.on_event("startup")
    def _chatbot_startup():
        if not STATE.chunks or STATE.embedder is None or STATE.embeddings is None:
            load_state()
