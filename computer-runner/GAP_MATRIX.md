# Capability gap matrix (free/OSS only, no spend). Provenance: builder todo notes (oss-capability-map.md, Sep 27-Oct 4); not re-verified externally by me.

| Gap | Free/OSS route | Status | Next step / owner |
|---|---|---|---|
| Computer-style orchestration | computer-runner (this folder) | built, 6 unit tests + local HTTP smoke pass | builder: commit to fizzle89/skills/computer-runner, deploy on Render free, test /health and /run on live URL |
| MCP server | FastMCP / python-sdk | routed to builder earlier | builder |
| Action traces + replay tests | runner.py JSONL + replay() | built (basic) | wire into Trace product |
| Bounded parallel reads | ThreadPoolExecutor wave exec in runner | built | none |
| FFmpeg compositor for proof videos | FFmpeg | routed to builder earlier, status unknown | builder to report |
| CAPTCHA/residential proxies | none free | BLOCKED: needs spend | stays gated; Ghana route via his iPhone covers Upwork |
| Virtual card rail at $0 | none | BLOCKED: no free rail | stays gated |
| Voice / heavy media gen | not on Render Free | BLOCKED: hardware | needs paid compute or his machine |
| Browser extension | spec only | BLOCKED: no desktop | needs his machine |
| Oracle Always Free host | n/a | NOT DONE: needs new account + card; not approved by user per today's rules | only if he says so directly |
