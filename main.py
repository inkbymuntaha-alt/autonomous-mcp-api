import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from web3 import Web3

app = FastAPI(title="Autonomous MCP Micro-API")

# Configuration
RECEIVER_WALLET = "0x960E510E4E1dA4B13CE3b601202d4680AFcf02E0"
BASE_RPC = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
REQUIRED_USDC_WEI = 2000  # 0.002 USDC (6 decimals)

w3 = Web3(Web3.HTTPProvider(BASE_RPC))

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
                "network": "eip155:8453",
                "asset": USDC_CONTRACT,
                "payTo": RECEIVER_WALLET,
                "maxAmountRequired": str(REQUIRED_USDC_WEI)
            }]
        }
    )

def verify_onchain_payment(tx_hash: str) -> bool:
    """Verifies if the given transaction hash is a successful USDC transfer to RECEIVER_WALLET on Base."""
    try:
        # Fetch transaction receipt from Base network
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        if not receipt or receipt.get("status") != 1:
            return False
            
        # ERC-20 Transfer Event Signature Topic
        transfer_topic = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
        padded_receiver = "0x000000000000000000000000" + RECEIVER_WALLET[2:].lower()
        
        # Scan transaction logs for a valid USDC transfer to your wallet
        for log in receipt.get("logs", []):
            if log["address"].lower() == USDC_CONTRACT.lower():
                topics = log.get("topics", [])
                if len(topics) >= 3 and topics[0].hex() == transfer_topic:
                    to_address = topics[2].hex()
                    if to_address.lower() == padded_receiver.lower():
                        amount = int(log["data"], 16)
                        if amount >= REQUIRED_USDC_WEI:
                            return True
        return False
    except Exception:
        return False

@app.get("/")
def read_root():
    return {"status": "online", "service": "autonomous-mcp-api"}

@app.post("/mcp/tools/extract_commercial_leads")
async def execute_mcp_tool(request: Request, payload: CommercialQueryInput):
    payment_sig = request.headers.get("PAYMENT-SIGNATURE") or request.headers.get("X-PAYMENT")

    if not payment_sig:
        return build_402_challenge()

    # Verify transaction hash on Base mainnet
    if not verify_onchain_payment(payment_sig):
        return JSONResponse(
            status_code=402,
            content={"error": "Invalid or unverified payment transaction hash."}
        )

    # Payment confirmed! Release data.
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
