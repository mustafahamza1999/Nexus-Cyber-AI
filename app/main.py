from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.workflow import app_workflow

app = FastAPI(
    title="Multi-Agent Code Auditor API",
    description="API for auditing, refactoring, and documenting code using autonomous agents.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط مجلد الملفات الثابتة (static) لتخديم صفحة الواجهة index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

class CodeRequest(BaseModel):
    code: str

@app.get("/")
def read_root():
    # توجيه تلقائي للواجهة التفاعلية عند فتح الرابط الرئيسي http://127.0.0.1:8000
    return RedirectResponse(url="/static/index.html")

@app.get("/api/health")
def health_check():
    return {"status": "AI Code Auditor Agent is running successfully!"}

@app.post("/api/audit")
def audit_code(request: CodeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code content cannot be empty.")
    
    initial_state = {
        "code_content": request.code,
        "security_report": None,
        "performance_report": None,
        "doc_report": None,
        "error": None
    }

    try:
        # تشغيل سير العمل عبر LangGraph workflow
        final_state = app_workflow.invoke(initial_state)
        
        if final_state.get("error"):
            raise HTTPException(status_code=500, detail=final_state["error"])

        return {
            "success": True,
            "security": final_state.get("security_report"),
            "performance": final_state.get("performance_report"),
            "documentation": final_state.get("doc_report")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))