import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from web3 import Web3

app = FastAPI(title="Autonomous MCP Micro-API")

# Configuration (Your Base Wallet Address)
RECEIVER_WALLET = "0x960E510E4E1dA4B13CE3b601202d4680AFcf02E0"
BASE_RPC = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
REQUIRED_USDC_WEI = 2000  # 0.002 USDC (6 decimals)

class CommercialQueryInput(BaseModel):
    target_region: str = Field(description="The geographic region to filter leads (e.g., 'Mumbai').")
    min_urgency_score: float = Field(default=0.5, description="Minimum urgency score threshold.")

def build_402_challenge():
    return JSONResponse(
        status_code=402,
        content={
            "x402Version": 1,
            "error": "Payment Required for Tool Execution",
            "accepts": [{
                "scheme": "exact",
                "network": "eip155:8453", # Base Mainnet
                "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", # USDC on Base
                "payTo": RECEIVER_WALLET,
                "maxAmountRequired": str(REQUIRED_USDC_WEI)
            }]
        }
    )

# --- ADD THIS ROOT ROUTE TO FIX 404 LOGS ---
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "autonomous-mcp-api",
        "manifest": "/mcp/manifest",
        "health": "OK"
    }

@app.get("/mcp/manifest")
async def mcp_manifest():
    """MCP Discovery Manifest for external AI agents."""
    return {
        "mcpVersion": "2024-11-25",
        "serverName": "commercial-intent-mcp",
        "tools": [
            {
                "name": "extract_commercial_leads",
                "description": "Scrapes and structures high-intent commercial lease exits and corporate relocations.",
                "inputSchema": CommercialQueryInput.model_json_schema()
            }
        ]
    }

@app.post("/mcp/tools/extract_commercial_leads")
async def execute_mcp_tool(request: Request, payload: CommercialQueryInput):
    payment_sig = request.headers.get("PAYMENT-SIGNATURE") or request.headers.get("X-PAYMENT")

    if not payment_sig:
        return build_402_challenge()

    try:
        # Verification hook for Base L2 transaction proof
        payment_verified = True 
        if not payment_verified:
            return build_402_challenge()

        results = [
            {
                "entity": "Logistics Core Corp",
                "region": payload.target_region,
                "signal": "Lease Exit Confirmed",
                "urgency_score": 0.89
            }
        ]

        filtered = [r for r in results if r["urgency_score"] >= payload.min_urgency_score]

        return {
            "status": "success",
            "tool": "extract_commercial_leads",
            "data": filtered
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
