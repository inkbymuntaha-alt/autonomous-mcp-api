import os
import requests
from typing import Dict, List

MCP_API_URL = "https://autonomous-mcp-api.vercel.app/mcp/tools/extract_commercial_leads"
RESEND_API_URL = "https://api.resend.com/emails"

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

print(f"[*] DEBUG: RESEND_API_KEY present? {bool(RESEND_API_KEY)}")
if RESEND_API_KEY:
    print(f"[*] DEBUG: Key starts with: {RESEND_API_KEY[:5]}...")

def send_email_via_resend(to_email: str, subject: str, html_body: str):
    if not RESEND_API_KEY:
        print("[X] ERROR: RESEND_API_KEY is missing from environment variables!")
        return

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": "onboarding@resend.dev",
        "to": [to_email],
        "subject": subject,
        "html": html_body
    }
    
    print(f"[*] Sending request to Resend API for {to_email}...")
    try:
        response = requests.post(RESEND_API_URL, headers=headers, json=payload, timeout=10)
        print(f"[*] Resend API Response Status: {response.status_code}")
        print(f"[*] Resend API Response Body: {response.text}")
    except Exception as e:
        print(f"[X] Exception during Resend request: {e}")

if __name__ == "__main__":
    print("[*] Starting diagnostic outreach run...")
    destination_inbox = "inkbymuntaha@gmail.com"
    subject = "Autonomous Pipeline Diagnostic Test"
    html_content = "<p>Diagnostic test email from GitHub Actions runner.</p>"
    
    send_email_via_resend(destination_inbox, subject, html_content)
