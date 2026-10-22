# Roblox Game Business — Project Log

The project's running record. Update it at the end of every work session.

- Full research report: [`01-market-research-and-recommendation.md`](01-market-research-and-recommendation.md)

## Status (22 Oct 2026)
- **Stage:** **Concept definition.** The founder asked to pause development until the concept is clear. The prototype in `last-stop-motel/` is parked (kept, not extended).
- **Founder profile:** 18+, lives in Germany, Windows laptop (Lenovo IdeaPad 5), Roblox Studio installed, time limited mainly by Claude usage limits.
- **Recommended first game:** "Last Stop Motel" (working title), a co-op anomaly night-shift horror game with procedural anomalies, 3 roles and a persistent upgrade/journal meta.
- **Target:** MVP in 6–8 weeks, public launch around 21 Dec 2026, go/iterate/pivot decision at day 90.

## Key findings
- Roblox DAU fell from 152M (Q3'25) to 123M (Q2'26), and bookings per hour are under pressure. Discovery now rewards retention and monetization.
- Since May 2026, a new game first reaches only **16+ players**. Under-16 access (Kids/Select) requires ID verification + 2FA + Roblox Plus or a refundable 1,000 R$ fee, plus passing an engaged-play evaluation.
- Roleplay and social hangouts are 16+ ID-verified only. Paid random items need exact odds disclosure and regional gating.
- Anomaly / observation horror has been a 2026 breakout genre (Shawarma Kiosk, Animal Hospital), but it may be past its peak.
- DevEx: $0.0038 per Earned Robux (standard), $0.0054 for qualifying U.S. 18+ spend, 30,000 R$ minimum.

- **Avatar items (UGC) as an alternative, checked 22 Oct 2026:** the creator gets only **30%** of each sale, or ~33% when priced above the floor on the Marketplace (official). An in-experience sale gives the experience owner another 40%, so items sold inside **our own game** earn 70%. Upfront costs: 80 R$ upload fee per item (official) plus a publishing advance of ~1,000–2,500 R$ for 3D items (reported). Requires ID verification, and reportedly Plus/Premium to keep items on sale. Reported: ~120k active sellers; median creator earns < 5,000 R$/month; median item ≈ $20 lifetime. Verdict: weaker than games as a main business; good as an add-on inside our own game.

## Decisions
| Date | Decision | Why | Status |
|---|---|---|---|
| 22 Oct 2026 | Recommend co-op anomaly game as game #1 | Best demand × solo-feasibility × virality; reusable engine | Proposed |
| 22 Oct 2026 | No paid random items at launch | Avoid odds/region compliance load | Proposed |
| 22 Oct 2026 | Research docs live in `roblox-business/`, separate from the existing `app.py` | Keep the unrelated trading app untouched | Done |
| 22 Oct 2026 | Workflow: Rojo project in git, Claude writes Luau in the cloud session, founder opens the built `.rbxlx` or syncs with Rojo | Works without Claude Code on the founder's PC; Studio MCP can be added later | Done |
| 22 Oct 2026 | Prototype first, concept approval after the playtest | A prototype is cheap and answers "is it fun?" better than discussion | Reversed by founder: define the concept first |

## Technical decisions
- Greybox map built from code (`MapBuilder`) so the prototype runs in an empty place. A hand-built map can replace it by reusing the `AnomalyProp` tags and `PropId`s.
- Anomalies are data (`AnomalyDefinitions`) built from reusable effects (`AnomalyEffects`). This is the reusable engine for future settings.
- Reporting uses server-side `ProximityPrompt.Triggered`, so no client remote is trusted.
- DataStore: `UpdateAsync` only, session lock with 30-min expiry, 5 load retries, data that failed to load is never saved, autosave every 120 s, `BindToClose` flush.

## Completed features
- Prototype v0.1: greybox motel, 22 anomalies, night loop, strikes, Cash rewards, anomaly journal, saves, analytics events, HUD. Passes `luau-compile` and `luau-lsp` strict type checks. **Not yet run in Studio.**

## Business assumptions (to validate)
- Founder is eligible for ID verification, publishing and DevEx from Germany (18+). DevEx supports international creators with a W-8BEN form. The higher $0.0054 rate depends on *U.S. 18+ buyers*, and Roblox Wallet is U.S.-only. Neither changes our base model.
- **Germany, taxes (not legal advice):** DevEx payouts are taxable income in Germany. Regular game income likely requires registering a business (Gewerbeanmeldung); the Kleinunternehmer scheme may apply. Check with a Steuerberater before the first payout.
- Meaningful income threshold ≈ 3,000+ DAU, D1 ≥ 25%, D7 ≥ 8%, payer conversion ≥ 2%.

## Open questions for the founder
1. Playtest results (see `last-stop-motel/README.md` checklist).
2. Final approval of "Last Stop Motel" after playing the prototype.

## Current metrics
None yet (no game published).

## Known bugs
None known; awaiting the first Studio run.

## Next actions
- [ ] Founder: fix GitHub access for Claude (so work is pushed and you can `git pull`)
- [ ] Founder: open `LastStopMotel.rbxlx`, play 2–3 nights, send Output errors + impressions
- [ ] Founder: play Scary Shawarma Kiosk + Animal Hospital for ~1 h each and note what's boring
- [ ] Claude: fix playtest issues, then week 3–4: co-op roles (Desk / CCTV / Runner), procedural anomaly combos, more anomalies
