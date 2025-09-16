import json
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = Path(__file__).parent / "skincare_rag_by_skin_type.json"

class RetrievalState:
    """
    管理資料、分塊、嵌入與模型的單例狀態
    """
    def __init__(self):
        self.embedder: Optional[SentenceTransformer] = None
        self.chunks: List[str] = []
        self.embeddings: Optional[np.ndarray] = None

STATE = RetrievalState()

def read_json_text(json_path: Path) -> List[Dict[str, Any]]:
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def flatten_json_entries(data: List[Dict[str, Any]]) -> List[str]:
    chunks: List[str] = []
    for entry in data:
        block = []
        block.append(f"膚質類型：{entry.get('skin_type', '')}")
        for c in entry.get("recommended_courses", []):
            goals = "、".join(c.get("goals", []))
            block.append(f"療程：{c.get('name','')}\n功效：{goals}")
        for p in entry.get("products", []):
            features = "；".join(p.get("features", []))
            block.append(f"產品：{p.get('name','')}（{p.get('step','')}）\n特色：{features}")
        block.append(f"推薦話術：{entry.get('reply_template', '')}")
        chunks.append("\n".join(block))
    return chunks

def embed_chunks(chunks: List[str], model: SentenceTransformer) -> np.ndarray:
    return model.encode(chunks)

def retrieve_top_k_chunks(query: str, chunks: List[str], embeddings: np.ndarray,
                          model: SentenceTransformer, k: int = 3) -> List[str]:
    query_vec = model.encode([query])
    sims = cosine_similarity(query_vec, embeddings)[0]
    top_idx = np.argsort(sims)[-k:][::-1]
    return [chunks[i] for i in top_idx]

def load_state() -> None:
    """
    在應用啟動時呼叫：載入資料、建立分塊與嵌入、初始化模型
    """
    data = read_json_text(DATA_PATH)
    STATE.chunks = flatten_json_entries(data)
    STATE.embedder = SentenceTransformer("all-MiniLM-L6-v2")
    STATE.embeddings = embed_chunks(STATE.chunks, STATE.embedder)
