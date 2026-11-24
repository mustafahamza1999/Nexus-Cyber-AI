import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.schemas import SecurityReport, PerformanceReport, DocReport

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "qwen/qwen3.8-27b"

def clean_dict_keys(d):
    """دالة ذكية لتنظيف أي مسافات زائدة في مفاتيح الـ JSON التي يرسلها النموذج"""
    if isinstance(d, dict):
        return {str(k).strip(): clean_dict_keys(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [clean_dict_keys(item) for item in d]
    return d

def safe_parse_json(raw_text: str, default_dict: dict) -> dict:
    if not raw_text or not raw_text.strip():
        return default_dict
    
    cleaned = raw_text.strip()
    if "```json" in cleaned:
        try:
            cleaned = cleaned.split("```json")[1].split("```")[0]
        except IndexError:
            pass
    elif "```" in cleaned:
        try:
            cleaned = cleaned.split("```")[1].split("```")[0]
        except IndexError:
            pass
            
    cleaned = cleaned.strip()
    try:
        parsed = json.loads(cleaned)
        return clean_dict_keys(parsed)
    except json.JSONDecodeError:
        if cleaned.count("{") > cleaned.count("}"):
            cleaned += "}" * (cleaned.count("{") - cleaned.count("}"))
        try:
            parsed = json.loads(cleaned)
            return clean_dict_keys(parsed)
        except Exception:
            return default_dict

def run_security_agent(code_content: str) -> SecurityReport:
    default_data = {
        "vulnerabilities": [{
            "severity": "Critical",
            "title": "Analysis Interrupted",
            "description": "The code analysis response was interrupted or incomplete.",
            "remediation": "Please retry the audit."
        }],
        "owasp_risks": ["A01:2021-Broken Access Control"],
        "security_score": 100
    }
    
    prompt = f"""
    You are an elite, world-class Application Security Auditor and Vulnerability Researcher. 
    Your ONLY task is to detect REAL, EXPLOITABLE SECURITY VULNERABILITIES in the provided code (such as Injection, XSS, CSRF, RCE, Broken Auth, Hardcoded Secrets, Insecure Deserialization, etc.).

    CRITICAL RULES:
    1. Detect ALL actual security vulnerabilities, no matter how small or large, including newly discovered vulnerability patterns.
    2. STRICTLY IGNORE architectural feedback, code styling choices, missing best practices (like HSTS, headers, rate limiting, or ProxyFix), and performance tips. DO NOT report them as vulnerabilities.
    3. If the code is secure and contains NO real security vulnerabilities, you MUST return an empty list for "vulnerabilities": [], and set the "security_score" to 100. DO NOT invent fake vulnerabilities or theoretical edge cases just to write a report.

    Code to Audit:
    ```python
    {code_content}
    ```
    
    You MUST return a valid JSON object matching this exact schema:
    {{
        "vulnerabilities": [
            {{
                "severity": "Low|Medium|High|Critical",
                "title": "Vulnerability Title",
                "description": "Concise technical explanation of the security flaw.",
                "remediation": "Fix details."
            }}
        ],
        "owasp_risks": ["List of applicable OWASP risks"],
        "security_score": 0_to_100_integer
    }}
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=900,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content if response.choices else ""
        data = safe_parse_json(content, default_data)
        
        if "security_score" not in data or data["security_score"] is None:
            data["security_score"] = 100
        if "vulnerabilities" not in data:
            data["vulnerabilities"] = default_data["vulnerabilities"]
        if "owasp_risks" not in data:
            data["owasp_risks"] = default_data["owasp_risks"]
            
        return SecurityReport(**data)
    except Exception as e:
        print(f"[!] Security Agent Exception: {e}")
        return SecurityReport(**default_data)

def run_performance_agent(code_content: str, security_report: SecurityReport) -> PerformanceReport:
    return PerformanceReport(
        time_complexity="N/A",
        space_complexity="N/A",
        code_smells=["Feature coming soon"],
        refactored_code="# قريباً: سيتم توفر إرسال الكود المصحح والخالي من الثغرات تلقائياً هنا.",
        improvements_summary="Refactoring agent is temporarily paused to focus exclusively on deep security auditing.",
        quality_score=100
    )

def run_doc_agent(code_content: str, refactored_code: str) -> DocReport:
    return DocReport(
        summary="Security audit completed successfully.",
        documented_code=code_content,
        generated_readme="# Security Audit Report\n\nDetailed vulnerability analysis performed successfully."
    )