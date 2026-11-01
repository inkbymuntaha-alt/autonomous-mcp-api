import os
import requests
from typing import Dict, List

# API Endpoints
MCP_API_URL = "https://autonomous-mcp-api.vercel.app/mcp/tools/extract_commercial_leads"
RESEND_API_URL = "https://api.resend.com/emails"

# Securely retrieve API Key from GitHub Secrets / Environment
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def fetch_commercial_leads(target_region: str, payment_sig: str = None) -> List[Dict]:
    """Queries the x402-gated MCP endpoint for verified commercial leads."""
    headers = {"Content-Type": "application/json"}
    if payment_sig:
        headers["PAYMENT-SIGNATURE"] = payment_sig
        
    payload = {"target_region": target_region, "min_urgency_score": 0.5}
    
    try:
        response = requests.post(MCP_API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            print(f"[!] Server returned status {response.status_code}")
            return []
    except Exception as e:
        print(f"[X] Error fetching leads: {e}")
        return []

def send_email_via_resend(to_email: str, subject: str, html_body: str):
    """Dispatches cold outreach emails using Resend REST API."""
    if not RESEND_API_KEY:
        print("[X] RESEND_API_KEY secret is missing from environment. Skipping email dispatch.")
        return

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Note: 'onboarding@resend.dev' sends to your verified account inbox
    payload = {
        "from": "onboarding@resend.dev",
        "to": [to_email],
        "subject": subject,
        "html": html_body
    }
    
    try:
        response = requests.post(RESEND_API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code in [200, 201]:
            print(f"[+] Resend Email sent successfully to {to_email}! ID: {response.json().get('id')}")
        else:
            print(f"[X] Resend API Error ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"[X] Failed to dispatch via Resend: {e}")

if __name__ == "__main__":
    print("[*] Initiating autonomous lead extraction & Resend email dispatch...")
    
    # Using mock signature to pass testing check
    mock_tx_hash = "0x_mock_payment_proof"
    leads = fetch_commercial_leads(target_region="Mumbai", payment_sig=mock_tx_hash)
    
    destination_inbox = "inkbymuntaha@gmail.com"
    
    if not leads:
        print("[*] Generating test dispatch directly to inbox...")
        subject = "Autonomous Pipeline: Real-Time Commercial Signal Alert"
        html_content = "<p>Congrats on sending your <strong>first automated email</strong> from your autonomous MCP agent!</p>"
        send_email_via_resend(destination_inbox, subject, html_content)
    else:
        for lead in leads:
            entity = lead.get("entity", "Target Company")
            signal = lead.get("signal", "Market Expansion")
            
            subject = f"Scaling {entity}'s cross-border deal flow"
            html_content = f"""
            <h3>Commercial Lead Dispatch</h3>
            <p>Hi Team at <strong>{entity}</strong>,</p>
            <p>We detected your recent market signal (<em>{signal}</em>). Our autonomous system has generated a high-intent profile for your review.</p>
            <p>Best regards,<br><strong>Autonomous Growth Operations</strong></p>
            """
            
            send_email_via_resend(destination_inbox, subject, html_content)
