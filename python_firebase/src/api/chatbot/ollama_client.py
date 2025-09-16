import logging
import requests

def query_ollama(context: str, question: str, model_name: str = "llama3.1:8b") -> str:
    """
    呼叫本機 Ollama 的 /api/chat，根據提供的 context 與 question 產生回覆
    """
    system_prompt = (
        "你是一位經驗豐富、溫柔且親切的皮膚護理顧問，擅長提供專業且易懂的建議。"
        "請嚴格根據【參考資料】和使用者最新的問題，來生成你的回答。"
        "規則："
        "1) 回答以條列式 1. 2. 3. 呈現；"
        "2) 僅能引用【參考資料】內容；"
        "3) 問類型→只列名稱；問特定項目→列出最多三點特色；"
        "4) 全程用繁體中文，不要多餘開場或結語。"
    )
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"【參考資料】\n{context}\n\n【使用者最新問題】\n{question}"}
        ],
        "stream": False
    }

    try:
        res = requests.post("http://localhost:11434/api/chat", json=payload, timeout=60)
        res.raise_for_status()
        j = res.json()
        return j.get("message", {}).get("content", "").strip() or "（沒有產生內容）"
    except Exception as e:
        logging.exception("Ollama 呼叫失敗")
        return f"⚠️ 發生錯誤：{e}"
