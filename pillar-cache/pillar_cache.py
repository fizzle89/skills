"""pillar_cache: small in-memory semantic cache. Stdlib only, free.
Keys are word sets; a lookup hits when Jaccard similarity >= threshold (and the stored entry is fresh).
LRU eviction, TTL. Lexical similarity, not embeddings: cheap and predictable. Lost on restart by design."""
import re, time
from collections import OrderedDict

def _w(t): return frozenset(re.findall(r"[a-z0-9]+", t.lower()))

class SemanticCache:
    def __init__(self, max_items=100, ttl_s=3600, threshold=0.85, clock=time.time):
        self.max, self.ttl, self.th, self.clock = max_items, ttl_s, threshold, clock
        self.d = OrderedDict()  # key(frozenset) -> (ts, value, text)
    def get(self, text):
        k = _w(text); now = self.clock()
        for key in list(self.d):
            ts, v, _ = self.d[key]
            if now - ts > self.ttl: del self.d[key]; continue
            u = len(k | key)
            if u and len(k & key) / u >= self.th: self.d.move_to_end(key); return v
        return None
    def put(self, text, value):
        self.d[_w(text)] = (self.clock(), value, text)
        while len(self.d) > self.max: self.d.popitem(last=False)
