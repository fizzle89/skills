---
name: explainer-video-lab
description: Makes 30-60s explainer videos in a clean "3Blue1Brown-style" look with Manim (or an HTML/SVG-to-video fallback) and free local TTS. Free tools only, no paid voice or video keys, real facts only. Use for how-it-works and launch explainers after the script is approved.
---

# Explainer video lab
Chain: short-form-scriptwriter (script) -> content-qa-gate -> **this** -> video-packaging-lab.
1. Script first: beats of 5-8s, one idea each, plain STE-style VO, real facts, honest demo wording. No numbers without a source.
2. Voice: free local TTS only (Piper, espeak-ng, or Coqui if the box allows). Never ElevenLabs or other paid keys. Keep VO calm, ~150 wpm.
3. Visuals: Manim Community (MIT) scenes for diagrams, text reveals, arrows. If Manim does not fit the box, render the explainer-diagram-html frames in headless Chrome and stitch with ffmpeg.
4. Real product screens (live Tenda demo captures) beat generated art. Calm music: royalty-free only, low under VO.
5. Mux with ffmpeg, burn captions, 1080x1350 or 1080x1920 as the platform needs.
6. Watch the whole file as a viewer (frames + audio sync) before reporting done. Uploads need reviewed files and, for personal channels, his yes.
7. Sandbox limit: ~2GB RAM, 2 CPUs. Render at 720p preview first; long scenes may need the Render runner.

## Proven route in this sandbox (Oct 2 2026)
Manim does NOT install here (manimpango needs system pango/cairo dev libs, no root). Working free route: PIL scene cards (real demo screenshot, flow diagram, honest limits) + Piper TTS (en_US-lessac-medium, pip piper-tts, voice via `python -m piper.download_voices`) + ffmpeg concat with fades. Reference script: scripts/build_explainer.py (37s, 1080x1350). Manim needs a box with libpango/libcairo dev packages or the Render runner.
