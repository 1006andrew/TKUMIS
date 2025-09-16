from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

templates = Jinja2Templates(directory="src/web/templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    index_path = Path("src/web/templates/index.html")
    template_name = "index.html" if index_path.exists() else None
    if template_name:
        return templates.TemplateResponse(template_name, {"request": request})
    # If no index.html, render the first available html file
    html_files = list(Path("src/web/templates").rglob("*.html"))
    if not html_files:
        raise HTTPException(status_code=404, detail="No templates found")
    rel = html_files[0].relative_to(Path("src/web/templates"))
    return templates.TemplateResponse(str(rel).replace("\\", "/"), {"request": request})

@router.get("/{page_path:path}", response_class=HTMLResponse)
async def any_page(request: Request, page_path: str):
    base = Path("src/web/templates")

    # 1️⃣ 直接找到完整路徑
    target = base / page_path
    if target.is_file():
        rel = target.relative_to(base)
        return templates.TemplateResponse(str(rel).replace("\\", "/"), {"request": request})

    # 2️⃣ 如果沒有副檔名，先補 .html
    if not page_path.endswith(".html"):
        candidate = base / f"{page_path}.html"
        if candidate.is_file():
            rel = candidate.relative_to(base)
            return templates.TemplateResponse(str(rel).replace("\\", "/"), {"request": request})

    # 3️⃣ 嘗試當資料夾，找資料夾下的 index.html
    folder_index = base / page_path / "index.html"
    if folder_index.is_file():
        rel = folder_index.relative_to(base)
        return templates.TemplateResponse(str(rel).replace("\\", "/"), {"request": request})

    raise HTTPException(status_code=404, detail=f"Template {page_path} not found")

