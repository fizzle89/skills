import time, pillar_router as pr
def boom(_): raise RuntimeError("x")
def t_degrade():
    r = pr.Router([("a", boom), ("b", lambda p: "B:" + p)]); n, v, at = r.call("q"); assert (n, v) == ("b", "B:q") and at[0] == ("a", "RuntimeError")
def t_breaker():
    now = [0.0]; r = pr.Router([("a", boom), ("b", lambda p: "ok")], fail_max=2, cool_s=10, clock=lambda: now[0])
    r.call(1); r.call(1); assert r.call(1)[2][0] == ("a", "circuit_open")
    now[0] = 11; assert r.call(1)[2][0][1] == "RuntimeError"  # half-open trial fails again
def t_timeout():
    r = pr.Router([("slow", lambda p: time.sleep(2)), ("b", lambda p: "ok")], timeout_s=0.1); assert r.call(1)[0] == "b"
def t_fallback(): assert pr.Router([("a", boom)], fallback="try later").call(1)[:2] == ("fallback", "try later")
def t_allfail():
    try: pr.Router([("a", boom)]).call(1); assert False
    except pr.AllFailed: pass
for k, v in list(globals().items()):
    if k.startswith("t_"): v(); print("ok", k)
