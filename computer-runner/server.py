import json, os, hmac
from http.server import BaseHTTPRequestHandler, HTTPServer
from runner import Runner, default_handlers, PlanError
class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code)
        self.send_header("content-type", "application/json"); self.send_header("content-length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        self._send(200, {"ok": True, "service": "computer-runner"}) if self.path in ("/", "/health") else self._send(404, {"error": "not found"})
    def do_POST(self):
        if self.path != "/run": return self._send(404, {"error": "not found"})
        tok = os.environ.get("RUNNER_TOKEN", "")
        got = self.headers.get("authorization", "").removeprefix("Bearer ").strip()
        if not tok or not hmac.compare_digest(got, tok): return self._send(401, {"error": "unauthorized"})
        try:
            plan = json.loads(self.rfile.read(int(self.headers.get("content-length", 0))))
            self._send(200, Runner(default_handlers(), approvals=[a for a in os.environ.get("RUNNER_APPROVALS", "").split(",") if a]).run(plan))
        except (PlanError, ValueError, KeyError) as e: self._send(400, {"error": str(e)})
HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080))), H).serve_forever()
