import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List

API_URL = "https://autonomous-mcp-api.vercel.app/mcp/tools/extract_commercial_leads"

# Configuration for Automated Sending (Set these in your environment or replace placeholders)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your-app-password")

def fetch_commercial_leads(target_region: str, payment_sig: str = None) -> List[Dict]:
    headers = {"Content-Type": "application/json"}
    if payment_sig:
        headers["PAYMENT-SIGNATURE"] = payment_sig
        
    payload = {"target_region": target_region, "min_urgency_score": 0.5}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

def send_email_notification(to_email: str, subject: str, body: str):
    """Automatically sends the generated cold email via SMTP relay."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"[+] Autonomous email successfully dispatched to {to_email}")
    except Exception as e:
        print(f"[X] SMTP Dispatch Error: {e}")

if __name__ == "__main__":
    print("[*] Autonomous pipeline executing...")
    
    # In production, pass your verified Base tx hash or integrate an automated eth-account signer here
    mock_tx_hash = "0x_mock_payment_proof"
    leads = fetch_commercial_leads(target_region="Mumbai", payment_sig=mock_tx_hash)
    
    for lead in leads:
        entity = lead.get("entity")
        signal = lead.get("signal")
        
        subject = f"Scaling {entity}'s cross-border deal flow in Dubai"
        body = f"""Hi Team at {entity},\n\nNoticed your recent market signal ({signal}) in Mumbai. We run an automated pipeline that extracts verified commercial property movers. Would you be open to a 5-minute data preview?\n\nBest,\nAutonomous Growth Operations"""
        
        # Target recipient destination (can be dynamically fetched or set to a test inbox)
        target_inbox = "test-client@targetdomain.com"
        
        # Uncomment below to enable live automated sending once SMTP details are configured
        # send_email_notification(target_inbox, subject, body)
        print(f"[Simulated Dispatch] Ready to email {entity} regarding signal: {signal}")
