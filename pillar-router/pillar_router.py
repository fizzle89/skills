"""pillar_router: degradation chain for model/provider calls. Stdlib only.
Chain = ordered providers (callables). Per-provider circuit breaker: opens after `fail_max` consecutive failures,
stays open `cool_s` seconds, then half-open (one trial). A call tries providers in order, skips open breakers,
enforces a per-call timeout via a worker thread, and returns (provider_name, result, attempts). If all fail,
returns the last-resort `fallback` value (e.g. a canned 'try later' answer) when given, else raises AllFailed."""
import time, threading

class AllFailed(Exception): pass

class Breaker:
    def __init__(self, fail_max=3, cool_s=30, clock=time.monotonic):
        self.fail_max, self.cool_s, self.clock = fail_max, cool_s, clock
        self.fails, self.opened_at = 0, None
    def allow(self):
        if self.opened_at is None: return True
        if self.clock() - self.opened_at >= self.cool_s: return True  # half-open trial
        return False
    def ok(self): self.fails, self.opened_at = 0, None
    def bad(self):
        self.fails += 1
        if self.fails >= self.fail_max: self.opened_at = self.clock()

class Router:
    def __init__(self, chain, fail_max=3, cool_s=30, timeout_s=20, fallback=None, clock=time.monotonic):
        self.chain = list(chain)  # [(name, callable(prompt)->str)]
        self.br = {n: Breaker(fail_max, cool_s, clock) for n, _ in self.chain}
        self.timeout_s, self.fallback = timeout_s, fallback
    def _run(self, fn, arg):
        box = {}
        def w():
            try: box["r"] = fn(arg)
            except Exception as e: box["e"] = e
        t = threading.Thread(target=w, daemon=True); t.start(); t.join(self.timeout_s)
        if t.is_alive(): raise TimeoutError("provider timeout")
        if "e" in box: raise box["e"]
        return box["r"]
    def call(self, arg):
        attempts = []
        for name, fn in self.chain:
            b = self.br[name]
            if not b.allow(): attempts.append((name, "circuit_open")); continue
            try:
                r = self._run(fn, arg); b.ok(); attempts.append((name, "ok")); return name, r, attempts
            except Exception as e:
                b.bad(); attempts.append((name, type(e).__name__))
        if self.fallback is not None: return "fallback", self.fallback, attempts
        raise AllFailed(attempts)
