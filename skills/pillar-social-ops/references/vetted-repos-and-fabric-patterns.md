# Vetted open-source patterns (Oct 2 2026)
Used as patterns only. Nothing installed, no API keys, no paid services, no auto-publish.

Social-manager vertical loop: discover (platform mechanics + trends) -> voice sheet -> ideation -> hook -> format -> content-qa-gate -> packaging/visuals -> post (Buffer / owned channels) -> content-performance-loop -> back into voice sheet and ideation.

Fabric-style prompt patterns to emulate inside our skills (MIT, danielmiessler/fabric, patterns folder): extract_wisdom / extract_insights (pull key ideas from his voice notes and source material), analyze_claims (claims ledger in QA), rate_content / label_and_rate (scoring), improve_writing + clean_text (edit passes), humanize (strip AI tells), create_micro_summary / create_5_sentence_summary (captions, repurposing), analyze_prose (voice check), write_essay (long-form skeleton).

deepagents content-builder-agent pattern: keep a persistent brand/voice memory file, separate research from writing, small skills loaded on demand. Already matches our chain; the voice sheet is the memory file.

## Installed locally (Oct 2 2026, ~/tools, may be wiped)
- fabric v1.4.505 binary + 260 patterns, Ollama backend via ~/.config/fabric/.env. Run: `cat file | ~/tools/fb/fabric -p <pattern>`. Needs `ollama serve` (~/tools/ol/bin/ollama) with gemma3:1b.
- Box is ~2GB RAM / 2 CPU: only <=1B models run; 1.5B is OOM-killed. Quality is weak (hallucinated sources in analyze_claims). Use for mechanics, not final judgement.
- deepagents + langchain-ollama venv at ~/tools/deepagents/examples/content-builder-agent/.venv (python 3.12). Graph runs; 0.5B model returns empty. Needs a stronger free model.
- PingPingE/ai-content-agents cloned (Claude Code agents, needs Anthropic/Claude Code). Easel cloned only (needs OpenClaw + Anthropic key, browser publishing).
