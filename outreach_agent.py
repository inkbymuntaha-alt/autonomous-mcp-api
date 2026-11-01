import os
import requests
from typing import Dict, List

API_URL = "https://autonomous-mcp-api.vercel.app/mcp/tools/extract_commercial_leads"

def fetch_commercial_leads(target_region: str, payment_sig: str = None) -> List[Dict]:
    """Queries the x402-gated MCP endpoint for verified commercial leads."""
    headers = {"Content-Type": "application/json"}
    if payment_sig:
        headers["PAYMENT-SIGNATURE"] = payment_sig
        
    payload = {
        "target_region": target_region,
        "min_urgency_score": 0.5
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 402:
        print("[!] Payment Required (x402 Challenge Received):")
        print(response.json())
        return []
    elif response.status_code == 200:
        data = response.json()
        return data.get("data", [])
    else:
        print(f"[X] Error {response.status_code}: {response.text}")
        return []

def generate_cold_email(lead: Dict) -> str:
    """Generates a hyper-personalized cold outreach draft based on real-time signals."""
    entity = lead.get("entity")
    region = lead.get("region")
    signal = lead.get("signal")
    
    if "Mumbai" in region:
        # Template optimized for Dubai real estate / Mumbai cross-border expansion
        return f"""Subject: Scaling {entity}'s cross-border deal flow in Dubai
        
Hi Team at {entity},

Noticed your recent market signal ({signal}) in {region}. With high-net-worth capital shifting aggressively between Mumbai and Dubai real estate corridors, traditional lead pipelines often miss immediate buyer intent.

We run an automated pipeline that extracts verified commercial property movers before they hit public boards. Would you be open to a 5-minute data sample preview this week?

Best regards,
Autonomous Growth Operations
"""
    else:
        # Template optimized for US Marketing Firms
        return f"""Subject: Capturing intent for {entity}
        
Hi {entity} team,

Noted your latest commercial milestone ({signal}). Scaling outbound acquisition in competitive US markets requires zero-latency prospect enrichment. 

Our autonomous agents isolate high-intent accounts in real-time. Let me know if you'd like to test our verified data stream.

Best,
Growth Engineering
"""

if __name__ == "__main__":
    print("[*] Initiating autonomous lead extraction & outreach pipeline...")
    
    # Test with mock signature (or pass your real Base tx hash once funded)
    mock_tx_hash = "0x_mock_payment_proof"
    
    leads = fetch_commercial_leads(target_region="Mumbai", payment_sig=mock_tx_hash)
    
    if not leads:
        print("[*] Tip: Provide a valid Base USDC transaction hash in 'payment_sig' to bypass the 402 paywall.")
    else:
        for lead in leads:
            print(f"\n--- Generated Outreach for: {lead['entity']} ---")
            email_draft = generate_cold_email(lead)
            print(email_draft)
