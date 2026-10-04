import unittest, tempfile, os
from runner import *
H = default_handlers()
def P(units, limit=0): return {"outcome": "t", "limit_usd": limit, "units": units}
class T(unittest.TestCase):
    def test_waves_and_run(self):
        p = P([{"id": "a", "effect": "read", "tool": "echo", "args": {"text": "x"}, "verify": {"key": "echo", "equals": "x"}},
               {"id": "b", "effect": "read", "tool": "echo", "needs": ["a"]}])
        self.assertEqual(waves(p), [["a"], ["b"]])
        self.assertTrue(Runner(H).run(p)["complete"])
    def test_cycle(self):
        self.assertTrue(validate(P([{"id": "a", "effect": "read", "needs": ["b"]}, {"id": "b", "effect": "read", "needs": ["a"]}])))
    def test_external_gate_and_upstream_block(self):
        p = P([{"id": "s", "effect": "external", "tool": "echo"}, {"id": "n", "effect": "read", "tool": "echo", "needs": ["s"]}])
        r = Runner(H).run(p); self.assertFalse(r["complete"]); self.assertEqual(r["results"]["n"]["state"], "blocked")
        self.assertTrue(Runner(H, approvals=["s"]).run(p)["complete"])
    def test_spend_gate_and_limit(self):
        self.assertTrue(validate(P([{"id": "a", "effect": "read", "cost_usd": 5}], limit=1)))
        p = P([{"id": "a", "effect": "read", "tool": "echo", "cost_usd": 1}], limit=2)
        self.assertEqual(Runner(H).run(p)["results"]["a"]["why"], "spend")
    def test_verify_fail(self):
        p = P([{"id": "a", "effect": "read", "tool": "echo", "args": {"text": "y"}, "verify": {"key": "echo", "equals": "x"}}])
        self.assertEqual(Runner(H).run(p)["results"]["a"]["why"], "verification")
    def test_trace_replay(self):
        f = tempfile.mktemp(); Runner(H, f).run(P([{"id": "a", "effect": "read", "tool": "echo"}]))
        self.assertEqual(replay(f), {"a": "done"}); os.remove(f)
unittest.main()
