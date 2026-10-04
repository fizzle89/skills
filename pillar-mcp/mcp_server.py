"""Pillar Fabric MCP server: public, read-only, stdlib + FastAPI. Streamable HTTP, JSON responses only.
Tools: pillar_products, pillar_brand_facts. No secrets, no writes, no outbound calls."""
from __future__ import annotations
import os, re, json
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response

router = APIRouter()
PROTOCOL = "2025-03-26"
PRODUCTS = [
    {"name": "Pillar Fabric", "role": "parent company and hub", "url": "https://pillar-fabric.onrender.com/"},
    {"name": "Security Desk", "role": "security questionnaire drafting with human approval", "url": "https://pillar-agent-fabric.onrender.com/"},
    {"name": "AI Visibility Audit", "role": "audit of how AI engines describe a brand", "url": "https://pillar-agent-fabric.onrender.com/ai-visibility"},
    {"name": "AI Monitoring", "role": "ongoing AI-engine visibility tracking", "url": "https://pillar-ai-monitoring.onrender.com/"},
    {"name": "Tenda", "role": "seller worker app", "url": "https://tendaapp.onrender.com/"},
    {"name": "Pillar Real Estate", "role": "real-estate vertical worker", "url": "https://strata-real-estate.onrender.com/"},
    {"name": "Clips", "role": "podcast clipping", "url": "https://pillar-clips.onrender.com/"},
    {"name": "Campaign Manager", "role": "campaign planning", "url": "https://pillar-fabric.onrender.com/campaign-manager"},
]
TOOLS = [
    {"name": "pillar_products", "description": "List Pillar Fabric products with what each does and its public URL.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "pillar_brand_facts", "description": "Return the public entity facts page for Pillar Fabric as plain text.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
]

def _facts() -> str:
    p = os.path.join(os.path.dirname(__file__), "static", "brand-facts.html")
    try: h = open(p, encoding="utf-8").read()
    except OSError: return "brand facts page not available"
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()[:8000]

def _call(name: str):
    if name == "pillar_products": return json.dumps(PRODUCTS, indent=1)
    if name == "pillar_brand_facts": return _facts()
    return None

def handle(msg: dict):
    mid, method = msg.get("id"), msg.get("method")
    def ok(r): return {"jsonrpc": "2.0", "id": mid, "result": r}
    def err(c, m): return {"jsonrpc": "2.0", "id": mid, "error": {"code": c, "message": m}}
    if mid is None: return None  # notification
    if method == "initialize":
        return ok({"protocolVersion": PROTOCOL, "capabilities": {"tools": {}}, "serverInfo": {"name": "pillar-fabric", "version": "0.1.0"}})
    if method == "ping": return ok({})
    if method == "tools/list": return ok({"tools": TOOLS})
    if method == "tools/call":
        p = msg.get("params") or {}
        out = _call(p.get("name", ""))
        if out is None: return err(-32602, "unknown tool")
        return ok({"content": [{"type": "text", "text": out}], "isError": False})
    return err(-32601, "method not found")

@router.post("/mcp", include_in_schema=False)
async def mcp(request: Request):
    try: body = await request.json()
    except Exception: return JSONResponse({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}, status_code=400)
    if isinstance(body, list):
        out = [r for r in (handle(m) for m in body if isinstance(m, dict)) if r]
        return JSONResponse(out) if out else Response(status_code=202)
    r = handle(body if isinstance(body, dict) else {})
    return JSONResponse(r) if r else Response(status_code=202)

@router.get("/mcp", include_in_schema=False)
def mcp_get(): return Response(status_code=405, headers={"Allow": "POST"})
