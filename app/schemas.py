from pydantic import BaseModel, Field
from typing import List, Optional

class VulnerabilityItem(BaseModel):
    title: str = Field(description="اسم الثغرة الأمنية")
    severity: str = Field(description="مستوى الخطورة: High, Medium, Low")
    line_number: Optional[int] = Field(None, description="رقم السطر إن وجد")
    description: str = Field(description="شرح للثغرة وما قد تسببه")
    remediation: str = Field(description="كيفية الإصلاح أو الكود المصحح")

class SecurityReport(BaseModel):
    security_score: int = Field(description="تقييم الأمان الإجمالي من 0 إلى 100")
    vulnerabilities: List[VulnerabilityItem] = Field(default_factory=list, description="قائمة الثغرات المكتشفة")

class ImprovementSuggestion(BaseModel):
    category: str = Field(description="فئة التحسين: Time Complexity, Memory, Clean Code, Redundancy")
    suggestion: str = Field(description="اقتراح التحسين والتطوير")
    code_before: Optional[str] = Field(None, description="الجزء القديم من الكود")
    code_after: Optional[str] = Field(None, description="الجزء المعدل بعد التحسين")

class PerformanceReport(BaseModel):
    quality_score: int = Field(description="تقييم جودة الأداء ونظافة الكود من 0 إلى 100")
    time_complexity: str = Field(description="التعقيد الزمني الإجمالي مثل O(N), O(N^2)")
    space_complexity: str = Field(description="التعقيد المكاني الإجمالي مثل O(1), O(N)")
    refactored_code: str = Field(description="النسخة المحسنة الكاملة من الكود Clean Code")
    suggestions: List[ImprovementSuggestion] = Field(default_factory=list, description="تفاصيل التوصيات")

class DocReport(BaseModel):
    summary: str = Field(description="ملخص سريع لما يفعله الكود ووظيفته الأساسية")
    documented_code: str = Field(description="الكود كاملاً مع إضافة Docstrings والتعليقات التوضيحية لكل دالة")
    generated_readme: str = Field(description="محتوى ملف README.md بلغة Markdown لشرح الملف في GitHub")