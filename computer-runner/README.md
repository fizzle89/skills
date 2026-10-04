# computer-runner

Stdlib-only (no deps, free) runner for Computer-style outcomes. Extends /skills/personal/computer-workflow/scripts/plan.py from a checker into an executor.

- Dependency waves, parallel within a wave (4 workers)
- Gates: `external` effect and any `cost_usd > 0` unit are blocked unless the unit id is in `approvals` (approvals must come from the user's channel, never from the plan itself)
- Per-unit `verify` ({key, equals} or {key, min}); failure marks the unit failed and blocks dependents
- JSONL trace + `replay()` reconstructs unit states without re-executing
- HTTP: GET /health, POST /run

Run tests: `python3 test_runner.py` (6 pass locally). Serve: `PORT=8080 python3 server.py`. Deploy: Dockerfile included (Render free web service).

Honest limits: handlers shipped are `echo` and `fetch` only. Connectors, MCP tools, and model routing plug in via the handlers dict. No auth on /run yet: add a bearer check before public exposure, and keep `approvals` ignored from public callers (currently the body can supply them; builder must remove that in the deployed version). Not the proprietary Perplexity fleet.

Deployed version: `/run` needs `Authorization: Bearer $RUNNER_TOKEN` (401 otherwise); approvals come only from the `RUNNER_APPROVALS` env var (the request body cannot grant them); `fetch` blocks private/loopback addresses.
