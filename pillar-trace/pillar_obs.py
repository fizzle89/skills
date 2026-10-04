"""Pillar Trace client: stdlib only. Spans and logs are batched and sent to the hub.
Never raises into the app, never blocks a request. Env: OBS_URL, OBS_TOKEN, OBS_PROJECT."""
import os, time, json, uuid, threading, queue, contextvars, urllib.request, atexit

URL = os.environ.get("OBS_URL", "https://pillar-fabric.onrender.com").rstrip("/")
TOKEN = os.environ.get("OBS_TOKEN", "")
PROJECT = os.environ.get("OBS_PROJECT", "unknown")
_q = queue.Queue(maxsize=2000)
_cur = contextvars.ContextVar("pillar_obs_span", default=None)
_budget = {"t": 0.0, "over": False}

def _id(n): return uuid.uuid4().hex[:n]

def _worker():
    while True:
        items = [_q.get()]
        t0 = time.time()
        while len(items) < 200 and time.time() - t0 < 2.0:
            try: items.append(_q.get(timeout=0.5))
            except queue.Empty: break
        _send(items)

def _send(items):
    if not TOKEN: return
    body = json.dumps({"spans": [i[1] for i in items if i[0] == "s"], "logs": [i[1] for i in items if i[0] == "l"]}).encode()
    req = urllib.request.Request(URL + "/api/obs/ingest", body, {"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN})
    for wait in (0, 5, 20):
        try:
            time.sleep(wait)
            urllib.request.urlopen(req, timeout=15).read(); return
        except Exception: continue

_started = False
def _start():
    global _started
    if not _started and TOKEN:
        _started = True
        threading.Thread(target=_worker, daemon=True).start()

class span:
    """with span('retrieval', kind='retrieval', cost_usd=0.0, k=3) as s: s.set(hit=True)"""
    def __init__(self, name, kind="", cost_usd=0.0, **attrs):
        self.name, self.kind, self.cost, self.attrs = name, kind, cost_usd, attrs
        self.status = "ok"
    def set(self, **kw):
        if "cost_usd" in kw: self.cost = kw.pop("cost_usd")
        self.attrs.update(kw)
    def __enter__(self):
        parent = _cur.get()
        self.trace_id = parent["trace"] if parent else _id(16)
        self.parent_id = parent["span"] if parent else None
        self.span_id = _id(8); self.start = time.time()
        self._tok = _cur.set({"trace": self.trace_id, "span": self.span_id})
        return self
    def __exit__(self, et, ev, tb):
        _cur.reset(self._tok)
        if et: self.status = "error"; self.attrs["error"] = f"{et.__name__}: {str(ev)[:200]}"
        try:
            _start()
            _q.put_nowait(("s", {"trace_id": self.trace_id, "span_id": self.span_id, "parent_id": self.parent_id, "name": self.name, "kind": self.kind,
                "start": self.start, "duration_ms": (time.time() - self.start) * 1000, "status": self.status, "cost_usd": self.cost, "attrs": self.attrs}))
        except Exception: pass
        return False

def log(message, level="info", **attrs):
    try:
        cur = _cur.get(); _start()
        _q.put_nowait(("l", {"ts": time.time(), "level": level, "message": message, "trace_id": cur["trace"] if cur else None, "attrs": attrs}))
    except Exception: pass

def budget_over():
    """Cost kill-switch: True when today's spend has reached the project's daily budget. Cached 60s; fails open."""
    if time.time() - _budget["t"] < 60: return _budget["over"]
    _budget["t"] = time.time()
    try:
        req = urllib.request.Request(f"{URL}/api/obs/budget/{PROJECT}", headers={"Authorization": "Bearer " + TOKEN})
        _budget["over"] = bool(json.loads(urllib.request.urlopen(req, timeout=3).read()).get("over"))
    except Exception: pass
    return _budget["over"]

def install(app, skip=("/health", "/api/health", "/api/v1/health", "/api/obs", "/obs", "/static", "/favicon.ico")):
    """FastAPI: one root span per request."""
    @app.middleware("http")
    async def _obs_mw(request, call_next):
        if request.url.path.startswith(skip): return await call_next(request)
        with span(f"{request.method} {request.url.path}", kind="http", method=request.method, path=request.url.path) as s:
            resp = await call_next(request)
            s.set(status_code=resp.status_code)
            if resp.status_code >= 500: s.status = "error"
            return resp
