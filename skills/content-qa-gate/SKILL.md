---
name: content-qa-gate
description: Mandatory QA step before any post, script, carousel, or article is shown as ready. Scores against a 6-dimension rubric, fact-checks every claim against a ledger, edits in three passes, strips AI tells, and allows at most 2 rewrite rounds. Use after the format skill (script/carousel/long-form) and before packaging or posting.
---

# Content QA gate
Patterns folded in from vetted open-source content pipelines (PingPingE/ai-content-agents review+edit+fact-check, Ismail-2001 editor/fact-checker/SEO sequence, wilingna FLUX retry-capped review, content-king quality gate, fabric rate_content/analyze_claims/humanize/improve_writing). Patterns only, no code copied, no paid APIs.

Chain position: ... format skill -> **content-qa-gate** -> video-packaging-lab + visual-prompt-director -> content-repurposer.

## Steps
1. **Claims ledger.** List every claim, number, name, and "we did X" line. For each: source (live URL, product screen, his voice note, verified file) or mark UNVERIFIED. Any UNVERIFIED claim is cut or reworded. Demo wording check for Tenda (early demo, sample catalog, simulated MoMo, no live payments, no waitlist CTA).
2. **Score 1-10** on: truth, hook strength, clarity, voice match (against voice sheet), platform fit, originality (could another brand post this verbatim? then fail). Ship needs truth = 10 and all others >= 8.
3. **Edit three passes:** structure, clarity (target ~20% shorter), grammar. Keep wit; cut filler.
4. **Humanize:** remove AI tells (inflated words, "not just X but Y", lists of three by reflex, emdashes, curly quotes, hype).
5. **Rewrite loop:** max 2 rounds. If still failing, drop the piece and log why instead of shipping weak work.
6. **Viewer review:** read or watch the final asset end to end as a viewer (render, screenshot, play). Nothing is "done" before this.
7. Output a short QA report: ledger, scores, changes, verdict APPROVE / REVISE / REJECT. Save to /downloads/qa-<piece>.md.

Personal LinkedIn/X posts and uploads still wait for his yes after APPROVE.

## Lessons from first keyed run (Oct 2, Groq gpt-oss-120b)
- "VERIFIED (implied/subjective)" is not a verdict. A first-person founder story, a stat, or an outcome claim is UNVERIFIED unless the user's own words or a live source supplies it. Opinion questions are the only claims exempt.
- Verify against the live product (open the demo or use product screens), not only the input text.
- Do not say "file saved" unless a file was actually written. State only what was done.
- Any "I/we" experience claim must trace to a founder message; otherwise CUT.
- Outcome words ("zero", "never", "all") are cut or softened to what the demo shows.

## Plain-writing pass (STE-style, added Oct 2)
Add after the humanize step. Aim "80% of the way" to ASD-STE100, not a strict audit:
- One idea per sentence, about 20 words max. Active voice, present tense.
- Short common words ("use", not "utilize"). One word per meaning; do not swap synonyms.
- Commands start with a verb. No idioms. No stacked noun strings.
- Keep his wit and the product names; plain does not mean flat.
