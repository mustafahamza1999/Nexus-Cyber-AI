import re
from datetime import datetime

def parse_apache_nginx_log(log_line):
    """
    تحليل سطر سجل (Log Line) مستخرج من Apache أو Nginx أو PythonAnywhere Access Log
    نمط السطر المتوقع: IP - - [Date] "METHOD Path HTTP/x.x" Status Size "Referer" "User-Agent"
    """
    # تعبير نمطي (Regex) دقيق لتفكيك عناصر سطر الـ Log
    log_pattern = r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+-\s+-\s+\[(?P<date>[^\]]+)\]\s+"(?P<method>[A-Z]+)\s+(?P<path>[^\s]+)\s+(?P<http_version>[^"]+)"\s+(?P<status>\d+)\s+(?P<size>\d+|-)\s+"(?P<referer>[^"]*)"\s+"(?P<user_agent>[^"]*)"'
    
    match = re.match(log_pattern, log_line)
    if not match:
        return {"error": "فشل تحليل هذا السطر، الصيغة غير مطابقة للـ Standard Access Log."}
    
    data = match.groupdict()
    
    # فحص الأنماط المشبوهة لتحديد نوع الهجوم المحتمل
    ua = data['user_agent'].lower()
    path_query = data['path'].lower()
    
    attack_type = "طلب سليم (Normal Traffic)"
    severity = "منخفض (Low)"
    
    if any(tool in ua for tool in ['sqlmap', 'nikto', 'nmap', 'burpsuite', 'dirsearch', 'ffuf', 'python-requests']):
        attack_type = "أداة فحص / بوت أمني مشبوه (Automated Scanner)"
        severity = "عالي (High)"
    elif any(pat in path_query for pat in ['union', 'select', '<script>', 'drop', 'exec', '../', 'etc/passwd']):
        attack_type = "محاولة حقن بايلود خبيث (Exploit Payload Injection)"
        severity = "حرج (Critical)"

    return {
        "ip_address": data['ip'],
        "timestamp": data['date'],
        "http_method": data['method'],
        "target_path": data['path'],
        "status_code": data['status'],
        "user_agent": data['user_agent'],
        "detected_attack": attack_type,
        "severity_level": severity
    }

# --- تجربة عملية محلية على VS Code ---
if __name__ == "__main__":
    print("[*] جاري تشغيل وكيل التحليل الجنائي الرقمي (DFIR) محلياً...\n")
    
    # سطر Log تجريبي يحاكي هجوم سحري بـ sqlmap
    sample_log = '185.220.101.5 - - [02/Nov/2026:14:20:10 +0300] "GET /api/audit?id=1%27%20UNION%20SELECT%201,2,3-- HTTP/1.1" 403 232 "-" "sqlmap/1.6-beta"'
    
    print(f"[-] السطر الخام المرصود:\n{sample_log}\n")
    print("="*60)
    
    # تحليل السطر عبر الوكيل
    report = parse_apache_nginx_log(sample_log)
    
    print("📋 [التقرير الجنائي الرقمي المستخرج]:")
    for key, value in report.items():
        print(f"  • {key}: {value}")
    print("="*60)