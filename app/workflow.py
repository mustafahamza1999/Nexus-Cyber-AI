from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from app.schemas import SecurityReport, PerformanceReport, DocReport
from app.agents import run_security_agent, run_performance_agent, run_doc_agent

class AuditorState(TypedDict):
    code_content: str
    security_report: Optional[SecurityReport]
    performance_report: Optional[PerformanceReport]
    doc_report: Optional[DocReport]
    error: Optional[str]

def security_node(state: AuditorState):
    print("--- [Agent 1] Running Security Auditor ---")
    try:
        report = run_security_agent(state["code_content"])
        return {"security_report": report}
    except Exception as e:
        return {"error": str(e)}

def performance_node(state: AuditorState):
    print("--- [Agent 2] Running Performance & Quality Agent ---")
    try:
        # جلب تقرير الأمان وتمريره مع الكود لوكيل الأداء والتحسين
        security_report = state.get("security_report")
        report = run_performance_agent(state["code_content"], security_report)
        return {"performance_report": report}
    except Exception as e:
        return {"error": str(e)}

def documentation_node(state: AuditorState):
    print("--- [Agent 3] Running Documentation & Readme Agent ---")
    try:
        refactored = state["performance_report"].refactored_code if state["performance_report"] else state["code_content"]
        report = run_doc_agent(state["code_content"], refactored)
        return {"doc_report": report}
    except Exception as e:
        return {"error": str(e)}

workflow = StateGraph(AuditorState)

workflow.add_node("security_node", security_node)
workflow.add_node("performance_node", performance_node)
workflow.add_node("documentation_node", documentation_node)

workflow.set_entry_point("security_node")
workflow.add_edge("security_node", "performance_node")
workflow.add_edge("performance_node", "documentation_node")
workflow.add_edge("documentation_node", END)

app_workflow = workflow.compile()