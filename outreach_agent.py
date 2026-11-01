import os
import requests
import sys

# Force immediate log flushing to GitHub terminal
sys.stdout.reconfigure(line_buffering=True)

MCP_API_URL = "https://autonomous-mcp-api.vercel.app/mcp/tools/extract_commercial_leads"
RESEND_API_URL = "https://api.resend.com/emails"

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

print(f"[*] Autonomous pipeline executing...")
print(f"[*] RESEND_API_KEY detected: {bool(RESEND_API_KEY)}")

def send_email_via_resend(to_email: str, subject: str, html_body: str):
    if not RESEND_API_KEY:
        print("[X] ERROR: RESEND_API_KEY secret is missing from environment variables!")
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
    
    print(f"[*] Dispatching test email via Resend to {to_email}...")
    try:
        response = requests.post(RESEND_API_URL, headers=headers, json=payload, timeout=10)
        print(f"[*] Resend API Response Status: {response.status_code}")
        print(f"[*] Resend API Response Body: {response.text}")
        if response.status_code in [200, 201]:
            print(f"[+] Resend Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"[X] Exception during Resend request: {e}")

if __name__ == "__main__":
    destination_inbox = "inkbymuntaha@gmail.com"
    subject = "Autonomous Pipeline: Live Test Dispatch"
    html_content = "<p>Congrats! Your autonomous GitHub Actions agent successfully delivered this email via Resend.</p>"
    
    send_email_via_resend(destination_inbox, subject, html_content)
    print("[*] Autonomous execution cycle complete.")
