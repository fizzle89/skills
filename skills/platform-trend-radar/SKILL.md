---
name: platform-trend-radar
description: Find what is trending or outperforming (HN, YouTube metadata, Reddit when reachable) and extract replicable format, hook and pacing patterns for Pillar/Tenda posts. Use before ideation. Never copy others' media or text.
---
# platform-trend-radar
1. Run scripts/radar.sh "<topic>" : HN Show HN top via Algolia, YouTube search metadata via yt-dlp (title, views, duration; no downloads), and optionally last30days (python 3.12 via uv; keyless sources only).
2. For each outlier, record ONLY: hook pattern, length, structure, format, why it worked. Paraphrase in our own words. Never reupload or copy media/text.
3. Feed patterns into content-ideation-engine and hook-architect; check platform rules in pillar-social-ops/references/platform-playbooks.md.
4. Do not use session-cookie extraction, proxies, paid keys, or logged-in scraping of any account (trending-scraper's IG/Reddit cookie paths are off limits). Reddit search returns 403 from our IP; skip it.
5. Run content-qa-gate on whatever ships.
Installed: yt-dlp (pip), uv + python 3.12, last30days v3.26 (cloned ~/res, runs keyless: HN only here; thin evidence).
