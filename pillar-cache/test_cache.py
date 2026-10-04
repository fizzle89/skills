import pillar_cache as c
def t_hit():
    x = c.SemanticCache(); x.put("AI agents for a dental clinic with bookings", 1); assert x.get("ai agents for a dental clinic with bookings!") == 1
def t_miss(): x = c.SemanticCache(); x.put("dental clinic", 1); assert x.get("freight forwarding company") is None
def t_ttl():
    n = [0]; x = c.SemanticCache(ttl_s=10, clock=lambda: n[0]); x.put("a b c", 1); n[0] = 11; assert x.get("a b c") is None
def t_lru(): x = c.SemanticCache(max_items=1); x.put("a b", 1); x.put("c d", 2); assert x.get("a b") is None and x.get("c d") == 2
for k, v in list(globals().items()):
    if k.startswith("t_"): v(); print("ok", k)
