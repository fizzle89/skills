"""Fuzz the public Pillar endpoints with malformed input. Expect: never 5xx, never a stack trace in the body.
Usage: python3 fuzz_live.py https://pillar-fabric.onrender.com/mcp https://pillar-computer-runner.onrender.com/run"""
import sys, json, urllib.request, urllib.error
CASES = [b"", b"{", b"null", b"[]", b"[1,2,3]", b'{"jsonrpc":"2.0"}', b'{"jsonrpc":"2.0","id":1}',
 b'{"jsonrpc":"2.0","id":1,"method":null}', b'{"jsonrpc":"2.0","id":1,"method":"tools/call","params":null}',
 b'{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":5}}',
 b'{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"pillar_mask_pii","arguments":null}}',
 b'{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"pillar_mask_pii","arguments":{"text":' + b'"A"' + b'}}}',
 b'{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"pillar_mask_pii","arguments":{"text":[1,{"a":2}]}}}',
 b'{"units":"x"}', b'{"units":[]}', b'{"units":[{"id":1}]}', b'\xff\xfe\x00', b'{"a":' * 200]
def post(u, body):
    r = urllib.request.Request(u, data=body, method="POST", headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=30) as x: return x.status, x.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e: return e.code, e.read().decode("utf-8", "replace")
bad = 0
for u in sys.argv[1:]:
    for c in CASES:
        s, b = post(u, c)
        if s >= 500 or "Traceback" in b: bad += 1; print("FAIL", u, s, c[:40], b[:80])
    print("done", u, len(CASES), "cases")
print("failures:", bad); sys.exit(1 if bad else 0)
