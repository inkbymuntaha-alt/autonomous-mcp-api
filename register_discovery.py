import requests
import json

MANIFEST_URL = "https://autonomous-mcp-api.vercel.app/mcp/manifest"
REPO_URL = "https://github.com/inkbymuntaha-alt/autonomous-mcp-api"

# Directories, indexes, and ping aggregators for MCP servers
REGISTRY_ENDPOINTS = [
    # Official / Community Index Pings & Crawlers
    "https://registry.modelcontextprotocol.io/v1/ping",
    "https://api.smithery.ai/v1/servers/register",
    "https://mcp.so/api/register"
]

def register_server():
    payload = {
        "manifest_url": MANIFEST_URL,
        "repository": REPO_URL,
        "name": "autonomous-commercial-leads",
        "x402_enabled": True
    }
    
    headers = {"Content-Type": "application/json"}
    
    for endpoint in REGISTRY_ENDPOINTS:
        try:
            res = requests.post(endpoint, json=payload, headers=headers, timeout=10)
            print(f"Ping sent to {endpoint} -> Status: {res.status_code}")
        except Exception as e:
            print(f"Could not reach {endpoint}: {e}")

if __name__ == "__main__":
    register_server()
