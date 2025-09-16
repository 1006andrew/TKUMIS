# src/chatbot/router.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from opencc import OpenCC

from .schemas import QuestionRequest, ChatResponse
from .retriever import STATE, retrieve_top_k_chunks
from .ollama_client import query_ollama

router = APIRouter(prefix="/api", tags=["chatbot"])

cc_t2s = OpenCC("t2s")
cc_s2t = OpenCC("s2t")

@router.post("/chat", response_model=ChatResponse)
def chat(payload: QuestionRequest):
    if STATE.embedder is None or STATE.embeddings is None or not STATE.chunks:
        raise HTTPException(status_code=503, detail="系統尚未初始化完成")

    q_trad = payload.question.strip()
    if not q_trad:
        raise HTTPException(status_code=400, detail="問題不可為空白")
    q_simp = cc_t2s.convert(q_trad)

    top_chunks = retrieve_top_k_chunks(
        query=q_simp,
        chunks=STATE.chunks,
        embeddings=STATE.embeddings,
        model=STATE.embedder,
        k=3
    )
    context = "\n---\n".join(top_chunks)

    ans_simp = query_ollama(context=context, question=q_trad)
    ans_trad = cc_s2t.convert(ans_simp)

    # 在伺服器 cmd 印出問題和答案
    print(f"[User 問題] {q_trad}")
    print(f"[Bot 回答] {ans_trad}\n{'='*40}")

    return JSONResponse(content=ChatResponse(answer=ans_trad).dict())
