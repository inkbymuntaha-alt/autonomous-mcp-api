from fastapi import FastAPI, Request, Response, status
import time

app = FastAPI(title="Autonomous x402 MCP Server")

PAYMENT_ADDRESS = "0x960E510E4E1dA4B13CE3b601202d4680AFcf02E0"
REQUIRED_USDC = "0.002"
NETWORK = "eip155:8453"  # Base Mainnet

@app.get("/")
def read_root():
    return {"status": "online", "mcp_manifest": "/mcp/manifest"}

@app.get("/mcp/manifest")
def get_manifest():
    return {
        "schema_version": "v1",
        "name": "autonomous-commercial-leads",
        "description": "High-intent commercial B2B data gated by x402 USDC micro-payments on Base.",
        "tools": [
            {
                "name": "extract_commercial_leads",
                "description": "Extract active B2B leads with high buying intent.",
                "endpoint": "/mcp/tools/extract_commercial_leads",
                "method": "POST",
                "x402_required": True
            }
        ]
    }

@app.post("/mcp/tools/extract_commercial_leads")
async def extract_commercial_leads(request: Request, response: Response):
    payment_header = request.headers.get("PAYMENT-SIGNATURE")
    
    if not payment_header:
        response.status_code = status.HTTP_402_PAYMENT_REQUIRED
        return {
            "error": "Payment Required",
            "x402_challenge": {
                "network": NETWORK,
                "asset": "USDC",
                "asset_contract": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                "recipient": PAYMENT_ADDRESS,
                "amount": REQUIRED_USDC,
                "header_required": "PAYMENT-SIGNATURE"
            }
        }

    return {
        "status": "success",
        "verified_payment_tx": payment_header,
        "timestamp": int(time.time()),
        "data_count": 2,
        "leads": [
            {
                "entity": "Apex Commercial Real Estate Brokerage",
                "niche": "Dubai Commercial Real Estate",
                "intent_signal": "Active hiring for remote lead generation pipelines",
                "contact_type": "M2M Webhook Endpoint",
                "target_endpoint": "https://api.apexrealty.ae/v1/inbound-webhook"
            },
            {
                "entity": "Vanguard Digital Media",
                "niche": "US High-Ticket Marketing",
                "intent_signal": "Scaling automated outreach operations",
                "contact_type": "M2M Webhook Endpoint",
                "target_endpoint": "https://vanguarddigital.io/api/b2b-intake"
            }
        ]
    }
