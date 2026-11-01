import os
import requests
import json

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
VERCEL_ENDPOINT = "https://autonomous-mcp-api.vercel.app/mcp/tools/extract_commercial_leads"
# 66-character valid EVM hash string for internal testing loop
TEST_TX_HASH = "0x" + "a" * 64

def run_autonomous_outreach():
    headers = {
        "Content-Type": "application/json",
        "PAYMENT-SIGNATURE": TEST_TX_HASH
    }
    payload = {
        "target_region": "Global",
        "min_urgency_score": 0.5
    }

    response = requests.post(VERCEL_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        lead_count = data.get("data_count", 0)
        timestamp = data.get("timestamp")
        
        print(f"[{timestamp}] Successfully retrieved {lead_count} leads.")
        
        # Dispatch execution receipt notification via Resend API
        if RESEND_API_KEY:
            resend_url = "https://api.resend.com/emails"
            resend_headers = {
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            }
            resend_payload = {
                "from": "onboarding@resend.dev",
                "to": "inkbymuntaha@gmail.com",
                "subject": f"Autonomous Pipeline Execution: {lead_count} Leads Processed",
                "text": f"Pipeline execution verified at timestamp {timestamp}.\nLeads processed: {lead_count}\nTx Signature: {TEST_TX_HASH}"
            }
            res = requests.post(resend_url, headers=resend_headers, json=resend_payload)
            print(f"Resend status: {res.status_code}")
    else:
        print(f"Pipeline failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    run_autonomous_outreach()
