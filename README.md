# Autonomous x402-Gated MCP API

An autonomous, machine-to-machine Model Context Protocol (MCP) server built with **FastAPI** and secured by **x402 micropayments** on **Base Mainnet (eip155:8453)**. This service provides real-time commercial intent data and high-urgency B2B leads on demand.

## 🚀 Service Endpoints
* **Base URL:** `https://autonomous-mcp-api.vercel.app`
* **MCP Manifest:** `https://autonomous-mcp-api.vercel.app/mcp/manifest`
* **SSE Endpoint:** `https://autonomous-mcp-api.vercel.app/sse`
* **Lead Extraction Tool:** `https://autonomous-mcp-api.vercel.app/mcp/tools/extract_commercial_leads`

---

## 💰 x402 Micropayment Monetization
This API enforces a programmatic paywall. Requests submitted without a valid settlement hash receive an HTTP `402 Payment Required` challenge containing structured payment routing data:
* **Network:** Base Mainnet (`eip155:8453`)
* **Asset:** USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
* **Recipient:** `0x960E510E4E1dA4B13CE3b601202d4680AFcf02E0`
* **Required Amount:** 0.002 USDC (2,000 wei)

Once an AI agent or client settles the USDC transfer on-chain, passing the resulting transaction hash in the `PAYMENT-SIGNATURE` header instantly unlocks the data payload.

---

## 🛠️ Configuration for AI Agents (Claude / Cursor)

Add this entry to your local MCP client configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "autonomous-commercial-leads": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sse",
        "[https://autonomous-mcp-api.vercel.app/sse](https://autonomous-mcp-api.vercel.app/sse)"
      ]
    }
  }
}
