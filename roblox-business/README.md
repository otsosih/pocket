# Roblox Game Business — Project Log

The project's running record. Update it at the end of every work session.

- Full research report: [`01-market-research-and-recommendation.md`](01-market-research-and-recommendation.md)

## Status (22 Oct 2026)
- **Stage:** Research complete → **waiting for founder approval** of the recommended concept.
- **Recommended first game:** "Last Stop Motel" (working title), a co-op anomaly night-shift horror game with procedural anomalies, 3 roles and a persistent upgrade/journal meta.
- **Target:** MVP in 6–8 weeks, public launch around 21 Dec 2026, go/iterate/pivot decision at day 90.

## Key findings
- Roblox DAU fell from 152M (Q3'25) to 123M (Q2'26), and bookings per hour are under pressure. Discovery now rewards retention and monetization.
- Since May 2026, a new game first reaches only **16+ players**. Under-16 access (Kids/Select) requires ID verification + 2FA + Roblox Plus or a refundable 1,000 R$ fee, plus passing an engaged-play evaluation.
- Roleplay and social hangouts are 16+ ID-verified only. Paid random items need exact odds disclosure and regional gating.
- Anomaly / observation horror has been a 2026 breakout genre (Shawarma Kiosk, Animal Hospital), but it may be past its peak.
- DevEx: $0.0038 per Earned Robux (standard), $0.0054 for qualifying U.S. 18+ spend, 30,000 R$ minimum.

## Decisions
| Date | Decision | Why | Status |
|---|---|---|---|
| 22 Oct 2026 | Recommend co-op anomaly game as game #1 | Best demand × solo-feasibility × virality; reusable engine | Proposed |
| 22 Oct 2026 | No paid random items at launch | Avoid odds/region compliance load | Proposed |
| 22 Oct 2026 | Research docs live in `roblox-business/`, separate from the existing `app.py` | Keep the unrelated trading app untouched | Done |

## Business assumptions (to validate)
- Founder can give 15–20 h/week.
- Founder is eligible for ID verification, publishing and DevEx in their country.
- Meaningful income threshold ≈ 3,000+ DAU, D1 ≥ 25%, D7 ≥ 8%, payer conversion ≥ 2%.

## Open questions for the founder
1. Age bracket (under 13 / 13–17 / 18+) and country of residence (DevEx eligibility)?
2. Roblox Studio installed? Windows or Mac?
3. Realistic weekly hours?
4. Approve "Last Stop Motel", or choose concept #2/#3?

## Current metrics
None yet (no game published).

## Known bugs
None yet.

## Next actions
- [ ] Founder: answer the open questions above
- [ ] Founder: play Scary Shawarma Kiosk + Animal Hospital for ~1 h each and note what's boring
- [ ] Claude: after approval, set up the Studio ↔ Claude Code workflow (Studio MCP or Rojo) and `CLAUDE.md`
- [ ] Claude: week-2 greybox scripts, anomaly definition format, server-side director
