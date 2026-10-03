# Reels / TikTok launch playbook (researched Oct 3 2026)
Sources: reelflood.com/blog/how-to-get-users-with-instagram-reels-2026 ; adsandscale.com/blog/instagram-reels-d2c-strategy ; linkedin.com post by KJS Creative (hook/demo/proof/action).

What successful product launches do:
1. Hook in the first 1.5-3s. Hook rate (viewers past 3s) is the gating signal: below 50% is a red flag, top Reels run 60-75%. Large on-screen text in frame 1, plus open loop or specific moment. Many watch muted, so always burn captions, but ship audio too.
2. Real product UI in motion, not stock footage. Show the transformation fast (screen recording or phone-native capture).
3. 80/20 value-to-ask: about 80% useful, 20% soft ask at the end. No hard CTA on cold viewers.
4. Length: demo 25-45s, social proof 20-35s, education 35-50s. Shorter is fine if completion is high. Watch-through of 75%+ and replays drive distribution.
5. Shares weigh more than saves. Write for "send this to a friend" moments (seller-to-seller).
6. Cadence 3-4/week once production is batched. Reply to every comment. Track hook rate, completion, shares/views >1.5%, saves/views >2%.
7. One tip or one claim per Reel. Specific claims beat vague praise. Open loops beat closed statements.
Our rules on top: honest early-demo wording, no invented stats or sellers, calm CC0 music at low level under the VO, audio on every reel.

Implementation in our stack: real mobile-native capture (scripts/capture_demo_mobile.py, 3x scale), Piper voice, CC0 music (FreePD mirror github.com/0lhi/FreePD, public domain), ffmpeg build (scripts/build_reel.py), QA gate before any post.
Known product bug found while capturing: the Tenda mobile header logo "tenda." renders as a blue underlined default link. Needs a CSS fix (a { color: inherit; text-decoration: none }). Never capture that header in assets until fixed.
