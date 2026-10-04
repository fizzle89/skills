#!/usr/bin/env python3
"""Computer-style plan runner (stdlib only, free). Executes a plan.json-style
graph in dependency waves, gates spend and external effects, verifies each
unit, writes a replayable JSONL trace. Handlers are pluggable by tool name."""
import json, time, uuid, sys
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

class PlanError(Exception): pass

def validate(plan):
    errs, units = [], plan.get("units")
    if not isinstance(units, list) or not units: return ["units must be a nonempty list"]
    ids = [u.get("id") for u in units]
    if len(set(ids)) != len(ids): errs.append("duplicate ids")
    for u in units:
        for d in u.get("needs", []):
            if d not in ids: errs.append(f"{u.get('id')}: unknown prerequisite {d}")
        if u.get("effect") not in ("read", "prep", "external"): errs.append(f"{u.get('id')}: bad effect")
        try:
            if Decimal(str(u.get("cost_usd", 0))) < 0: raise ValueError
        except Exception: errs.append(f"{u.get('id')}: bad cost_usd")
    try: waves(plan)
    except PlanError as e: errs.append(str(e))
    try:
        total = sum(Decimal(str(u.get("cost_usd", 0))) for u in units)
        if total > Decimal(str(plan.get("limit_usd", 0))): errs.append(f"declared ${total} exceeds limit")
    except Exception: errs.append("bad limit_usd")
    return errs

def waves(plan):
    need = {u["id"]: set(u.get("needs", [])) for u in plan["units"]}
    done, out = set(), []
    while need:
        ready = sorted(i for i, n in need.items() if n <= done)
        if not ready: raise PlanError("cycle or unresolved dependency")
        out.append(ready); done |= set(ready)
        for i in ready: del need[i]
    return out

class Runner:
    def __init__(self, handlers, trace_path=None, approvals=()):
        self.handlers, self.approvals, self.trace_path = handlers, set(approvals), trace_path
        self.trace, self.run_id = [], uuid.uuid4().hex[:12]
    def log(self, **e):
        e.update(ts=time.time(), run=self.run_id); self.trace.append(e)
        if self.trace_path:
            with open(self.trace_path, "a") as f: f.write(json.dumps(e) + "\n")
    def _unit(self, u, results, spent):
        uid = u["id"]
        if u.get("effect") == "external" and uid not in self.approvals:
            self.log(unit=uid, event="blocked", why="external effect needs approval"); return {"state": "blocked", "why": "approval"}
        if Decimal(str(u.get("cost_usd", 0))) > 0 and uid not in self.approvals:
            self.log(unit=uid, event="blocked", why="spend needs approval"); return {"state": "blocked", "why": "spend"}
        h = self.handlers.get(u.get("tool"))
        if not h: self.log(unit=uid, event="blocked", why="no handler"); return {"state": "blocked", "why": "no handler"}
        self.log(unit=uid, event="start", tool=u["tool"])
        try:
            out = h(u.get("args", {}), {n: results[n] for n in u.get("needs", [])})
        except Exception as e:
            self.log(unit=uid, event="error", err=str(e)); return {"state": "failed", "why": str(e)}
        chk = u.get("verify")
        if chk and not self.handlers["_verify"](chk, out):
            self.log(unit=uid, event="verify_failed"); return {"state": "failed", "why": "verification", "out": out}
        self.log(unit=uid, event="done", out=out); return {"state": "done", "out": out}
    def run(self, plan):
        errs = validate(plan)
        if errs: raise PlanError("; ".join(errs))
        by = {u["id"]: u for u in plan["units"]}; res = {}
        for w in waves(plan):
            runnable = []
            for i in w:
                bad = [d for d in by[i].get("needs", []) if res[d]["state"] != "done"]
                if bad: res[i] = {"state": "blocked", "why": f"upstream {bad}"}; self.log(unit=i, event="blocked", why="upstream")
                else: runnable.append(i)
            with ThreadPoolExecutor(max_workers=4) as ex:
                for i, r in zip(runnable, ex.map(lambda i: self._unit(by[i], {k: v.get("out") for k, v in res.items()}, 0), runnable)):
                    res[i] = r
        return {"run": self.run_id, "results": res, "complete": all(r["state"] == "done" for r in res.values())}

def replay(trace_path):
    """Reconstruct unit states from a trace without re-executing anything."""
    st = {}
    for line in open(trace_path):
        e = json.loads(line)
        if e["event"] in ("done", "blocked", "error", "verify_failed"): st[e["unit"]] = e["event"]
    return st

def default_handlers():
    import urllib.request
    def fetch(a, _):
        import ipaddress, socket, urllib.parse
        if not a["url"].startswith(("http://", "https://")): raise ValueError("http(s) only")
        host = urllib.parse.urlparse(a["url"]).hostname or ""
        for ai in socket.getaddrinfo(host, None):
            ip = ipaddress.ip_address(ai[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved: raise ValueError("private address blocked")
        with urllib.request.urlopen(a["url"], timeout=15) as r: return {"status": r.status, "bytes": len(r.read(200000))}
    def echo(a, up): return {"echo": a.get("text", ""), "upstream": list(up)}
    def verify(chk, out):
        k, v = chk.get("key"), chk.get("equals")
        return out.get(k) == v if "equals" in chk else (out.get(k) or 0) >= chk.get("min", 0)
    return {"fetch": fetch, "echo": echo, "_verify": verify}

if __name__ == "__main__":
    plan = json.load(open(sys.argv[1]))
    print(json.dumps(Runner(default_handlers(), "trace.jsonl").run(plan), indent=1))
