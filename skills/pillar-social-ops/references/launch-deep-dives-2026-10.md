# Launch deep dives (Oct 3 2026). Formats and structure only. Nothing copied.
Sources read in full: damianplayer.com/typesafe-ai-case-study ; neatprompts.com/p/heyclicky-15m-views-arguing-against-itself ; stackstarts.com/postiz-agentic-social-launch-system/ ; code: github.com/xai-org/x-algorithm (cloned, read README + home-mixer/params/param.rs + visibility-filtering) ; github.com/farzaa/clicky (cloned, README read; macOS app, needs Mac + paid keys, NOT run).
Also seen, not used: marketingideas.com piece about Instinct (not read; unrelated to our task).

## A. X ranking, from the source (what the feed actually rewards)
Final score = sum(weight x predicted probability of action). Published weights (param.rs, Aug-Sep 2026 release; weights multiply predictions, not raw counts, per the repo's own caveat):
- reply 5.0 (plus +15 boost on mutual follows), quote 5.0, follow-author 4.0, share 2.0, share via DM 5.0, share via copy-link 20.0, repost 1.0, like 0.5, link click 0.3 and open-link 0.2, video open 0.07, dwell 0.05.
- Negative: report -234, mute -58.8, not interested -47.52, block -31.2, not dwelled -0.02.
Takeaways: write for replies, quotes and sends-to-friends, not likes. A copy-link share is worth 40 likes of predicted probability. One link in the post body lowers value (link weights are small and the external-link penalty is reported). Anything that makes people hide, mute or report costs far more than likes earn. Candidate posts older than 48h are dropped (AgeFilter): day-one reach is all of it. Out-of-network posts are discounted, and a new-author boost exists for low-impression authors (README, values not located in params). Posts can be dropped before scoring by safety labels (visibility-filtering: SPAM, SPAM_HIGH_RECALL, low-quality rules for non-followers). Our @usepillar_ai reach label is probably this layer; the repo cannot say which rule hit us, and the Under the Hood tool in the README reports label stats per account (we have not opened it; X login is off limits).
## B. TypeSafe/Jev launch (X, Sep 15 2026; Doomers case study)
Founder had ~1,500 followers; launch post 40M impressions, 150k waitlist in 24h (their numbers). Sequence: seed the first hour to 80-100 relevant accounts (we cannot buy this; our free version is replying where the buyers already talk) > post opens with a checkable credential, then the question the product answers, then 3 testable claims > 2:56 demo video (long videos did 2x videos under 30s on X in their data) > founder answers every question all day > 5 follow-up posts (benchmarks, demos, pricing) added 4M+. For us: credential = what is real and checkable (live demo link); claims = only ones a viewer can test in the demo.
## C. HeyClicky (IG/X/LinkedIn, Apr 2026)
One demo clip where nobody needs the product explained (cursor buddy points at the exact button), shipped as "I built this" first person, open-sourced next morning, honest self-assessment ("not a 10/10 idea"), metrics video that argues against itself, no testimonials, one-line "something new, see you tomorrow, link below" teasers, same story cut for IG, X, LinkedIn, YouTube. For us: first-person founder voice, honest limits as a feature, one self-explaining demo moment per post.
## D. Postiz (X, 2026)
Made the product usable inside a trending agent workflow, then wrote an explainer on how to use it with the trend. A 200-follower account reached ~500k views because X distributes by interest. Reliability over features. For us: write practical how-to posts about the problem our demo solves (seller DM replies), not announcements.

## Applied rules (also in the platform-trend-radar and launch-sequence-reverse-engineer skills)
1. Every post opens with a claim a viewer can test in the demo.
2. Ask for replies/DMs/sends ("send this to a seller who answers DMs at midnight"), not likes.
3. No link in the body of X posts; link goes in a reply only after the label is cleared.
4. Day-one reply discipline: answer every comment in the first hour.
5. One demo moment per post that needs no explanation.
6. Same story, cut per platform (Reel, carousel, slideshow, X thread).
Limits: case-study numbers are the authors' claims; the weights are the published config, not proof of live production values.
