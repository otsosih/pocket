# Roblox Game Business — Market Research & First-Game Recommendation

Research date: **22 October 2026**. Owner: project founder + Claude (AI partner).

## How to read this document

Every factual claim carries a label:

| Label | Meaning |
|---|---|
| **[Official]** | Roblox documentation, DevForum announcement, SEC filing or Roblox newsroom (seen via search-indexed text) |
| **[Reported]** | Press, trackers, wikis or industry reports. Plausible but not independently checked |
| **[Estimate]** | My own calculation from stated assumptions |
| **[Opinion]** | My judgement. Challenge it |

**Research limitations (important):**
- This session's network policy blocked direct page fetches (roblox.com, trackers, news sites all refused). All evidence came through a web-search tool that returns summaries of indexed pages. I could not open Roblox's Creator Dashboard, RoMonitor/Rolimons history charts, TikTok or YouTube directly.
- Live player counts change hourly, and trackers disagree with each other. Treat every CCU figure below as a snapshot, not a fact about today.
- No reliable public revenue data exists for individual Roblox games. I don't estimate competitor revenue anywhere in this document.
- Roblox reports Q3 2026 earnings on **29 October 2026**, a week after this research. Re-check the platform numbers after that date.

---

## STEP 1 — The Roblox market right now: the trends that matter

### 1.1 Platform health: big but cooling, and monetization is under pressure
- **DAU 123M in Q2 2026**, +10% YoY, but down from a **152M peak in Q3 2025** (144M Q4'25 → 132M Q1'26 → 123M Q2'26). Hours engaged were 29B (peak 40B). **[Reported, from Q2 2026 earnings coverage]**
- Bookings grew only **+8% YoY to ~$1.6B**. Q3 2026 guidance implies a **14–18% YoY decline**. The CFO said **bookings per hour were below forecast, especially in under-13 cohorts**, as play moved from high-monetizing 2025 viral hits to lower-monetizing new and evergreen games. **[Reported]**
- Growth is concentrated in older users and new regions: U.S. **18+ DAU and hours +40% YoY** (Q1 2026 letter) **[Official]**. Japan DAU +67%, India +64% **[Reported]**.
- Age mix among age-checked users (Q4 2025): **35% under 13, 38% aged 13–17, 27% aged 18+** **[Official, SEC 8-K]**.

**Implication [Opinion]:** Roblox now has a strong incentive to send traffic to games that **retain players and monetize**, particularly with teens and adults. That's the audience to build for.

### 1.2 Safety overhaul changes who you can reach on day one
- **Mandatory age checks for chat** worldwide since January 2026 **[Official]**.
- **Roblox Kids (5–8) and Roblox Select (9–15) accounts** launched April 2026. Kids accounts only see games labelled Minimal or Mild **[Official/Reported]**.
- From **19 May 2026**, social hangouts and free-form roleplay games are restricted to **ID-verified 16+** users **[Reported]**. Roleplay is effectively off the table for a new developer targeting kids.
- **New publishing requirements (May 2026) [Official, DevForum]:**
  - *Personal use:* anyone can publish.
  - *Reach 16+ users:* age check, account in good standing, account at least 2 days old.
  - *Reach all ages (Kids/Select):* also **ID verification, 2-step verification, and an active Roblox Plus/Premium subscription**, **or a one-time 1,000 Robux fee per game**, refunded 3 months after the game becomes eligible.
  - The game must then pass an **evaluation**. Reported thresholds vary: the help article says **250 unique plays by highly engaged, age-checked 16+ users within 60 days**, and the DevForum thread says 500 in 30 days. Players under 16 can't see the game until it passes.
- **Content maturity labels [Official]:** Minimal/Mild reach Kids + Select. **Moderate** reaches Select (9–15) + 16+. **Restricted** is 18+ only. Unrated experiences have been unplayable since 30 Sept 2025.

**Implication [Opinion]:** A brand-new game first lives or dies with **16+ players**. Design something teens and young adults genuinely enjoy and that produces engaged sessions. Only after evaluation does it unlock the younger audience. That rules out designs that only appeal to 7-year-olds.

### 1.3 Discovery now rewards long-term retention, not spikes
- The official DevForum post "How we are improving Home this year" describes a new **"deep play-through rate"** signal, a **"Standout Games"** curated sort for novel games, and video previews (hover-to-autoplay, July 2026). The new signals are visible in **Creator Analytics → Acquisition → Home Recommendations**. **[Official]**
- A June 2026 change reportedly widened the evaluation window **from 7 to 28 days**, scoring returns on Day 1, Days 2–7 and Days 8–28 **[Reported, single secondary source, needs verifying]**.
- Benchmark scorecards (D1/D7 vs similar games) appear once a game has **100+ DAU** **[Official]**.

**Implication [Opinion]:** Cheap viral spikes without a reason to return get punished. The MVP needs a **reason to come back on Day 2, Day 7 and Day 28** from launch.

### 1.4 What's hot (snapshots, Aug–Oct 2026)
| Game | What it is | Evidence |
|---|---|---|
| **Steal an Egg** (launched 25 Jul 2026) | Steal-and-defend collection tycoon | 6B visits, 14.2M peak CCU in Q3, the most-visited game of Q3 **[Reported, Aream & Co Q3 report via press]**. It used an in-game short-video "Reels" feed that Roblox then banned for all-ages games **[Reported, Kotaku]** |
| **Steal a Brainrot** (2025) | Meme steal-and-defend tycoon | Only Roblox game past **25M CCU** **[Reported, Wikipedia]** |
| **Grow a Garden** (2025) | Farming / collection live-ops | Peak 22.3M CCU (Aug 2025), no longer in the top lists **[Reported]** |
| **99 Nights in the Forest** | Co-op survival horror | Peak ~14.2M CCU, 26B visits, film deal, Fortnite collab **[Reported]** |
| **Animal Hospital (Anomaly)** (launched 10 May 2026) | Co-op observation / anomaly horror | ~1.27M peak CCU on 10 Jul. Won 4 Innovation Awards including Best New Game. 30-day peak since fell to roughly ¼ of the record **[Reported]** |
| **Scary Shawarma Kiosk: the ANOMALY** | Night-shift anomaly horror | ~1.3B visits, 2 game passes, 27 dev products **[Reported, Rotrends]** |
| **+1 Speed Keyboard Escape** | Incremental speed obby | Top-3 live in Aug 2026 snapshots **[Reported]** |
| **Murder Mystery 2** (evergreen) | Social deduction PvP | ~540K–700K concurrent at peaks **[Reported]** |
| **Brookhaven RP** (evergreen) | Social roleplay | ~87B all-time visits, now hit by the 16+ roleplay rule **[Reported]** |

### 1.5 Monetization tools available in 2026
- Game passes, developer products, private servers, avatar items **[Official]**.
- **Creator Rewards** replaced Premium Payouts on 24 July 2025. It pays for daily engagement by "active spender" players and for bringing new or returning players onto Roblox (audience expansion). There's a 60-day hold **[Official, DevForum]**. Exact rates (e.g. "5 Robux per qualifying player per day", "35% of first $100") are **[Reported, third-party]**.
- **Rewarded video ads** are open to all ads-eligible creators (Feb 2026). A Studio drag-and-drop ad plug-in is expected Q4 2026 **[Official/Reported]**.
- **Roblox Plus** ($4.99/mo) replaced Premium for new subscribers on 30 April 2026 **[Reported]**.
- **Paid random items** (loot boxes, paid eggs) are strict since May 2026: exact % odds for every outcome before purchase, every outcome must have value, luck-boost effects must be disclosed, and players in some regions must be blocked via `PolicyService` (`ArePaidRandomItemsRestricted`) **[Official, DevForum]**.
- **RDC 2026 (Sept)** announced standalone apps for Roblox games, Chrome browser play by end of 2026, a "Roblox Wallet" paying eligible **U.S. 18+** creators in USD daily, and AI tools (Build, Scene Generator). Creators earned ~$1.7B in the last 12 months **[Official/Reported]**.

---

## STEP 2 — Why the successful games work (patterns)

| Pattern | Seen in | Why it works |
|---|---|---|
| **A premise you get from one thumbnail or 5-second clip** | Steal a Brainrot, Steal an Egg, +1 Speed, Shawarma Kiosk | Roblox Home and TikTok both reward instant comprehension |
| **Social conflict or co-op tension** | Steal-and-defend (stealing from friends), MM2, 99 Nights, Animal Hospital | Players invite friends, and friend groups retain far better than solo players |
| **Clip-able moments** | Anomaly jump-scares, someone stealing your best item, ragdoll chaos | Free short-form marketing made by players and YouTubers |
| **Collection + rarity** | Grow a Garden, Steal an Egg, anomaly "journals" | A long-term goal that drives Day-7+ returns and spending |
| **Frequent, scheduled updates** | Animal Hospital (named updates every ~2 weeks), Grow a Garden weekly events | Each update re-triggers recommendations and creator videos |
| **Low technical ceiling, high polish of the core feel** | Anomaly games are one small map | Small teams ship fast and iterate weekly |

**Recent breakouts weren't technically complex.** Roblox's own GDC 2026 pitch says teams under 10 people reach 25M+ CCU with social-first design **[Official claim, marketing]**. Most breakout hits re-skin a proven loop with a fresh fantasy and great clip potential.

**Common weaknesses in competitors that we can exploit [Opinion, from player-facing coverage]:**
- Anomaly games run out of content. Once you've seen every anomaly, there's no reason to return, which is visible in Animal Hospital's decline from peak.
- Steal-and-defend clones are hostile to newcomers (griefing, pay-to-defend) and copy each other's memes.
- Big survival games are long and heavy on low-end phones.

---

## STEP 3 — Niches that are realistic for a solo developer using AI

**Filters applied:** (1) MVP in ≤8 weeks part-time; (2) appeals to 16+ first; (3) Mild/Moderate maturity so it can later reach Select 9–15; (4) produces clips; (5) has a reason to return on Day 7 and Day 28; (6) monetizes without loot-box regulatory pain; (7) not roleplay or social hangout (16+ ID-verified only).

| Niche | Verdict |
|---|---|
| Co-op **anomaly / observation horror** with replayable meta | ✅ Proven demand, tiny map, scripted content is easy to produce with AI help, very clip-able. Risk: trend may be maturing |
| Physics / ragdoll "launch" incremental | ✅ Cheap to build, very clip-able, weaker retention |
| Co-op chaotic job sim (Overcooked-style) | ✅ Less crowded, needs good netcode feel |
| Steal-and-defend meme tycoon | ⚠️ Biggest demand but most copycats. Success depends on meme timing and live-ops speed |
| Co-op open-world survival (99 Nights-like) | ❌ Too big for a solo MVP |
| Roleplay / hangout | ❌ Now 16+ ID-verified only |
| Plain simulator / obby / tycoon | ❌ Saturated, low differentiation |

---

## STEP 4 — 12 concepts compared

Scores are 1–10 (for **Competition**, 10 = least crowded). They are **[Opinion]** informed by the evidence above. The weighted score multiplies **Feasibility ×1.5**, **Competition ×1.25** and **Expansion ×0.75**, and keeps the rest at ×1, because for a solo dev "can we actually finish and stand out" matters most.

| # | Concept | Demand | Compet. | Feasib. | Retention | Monet. | Viral | Expansion | **Raw /70** | **Weighted** |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Co-op anomaly night-shift + upgrade meta** | 8 | 5 | 9 | 5 | 5 | 9 | 7 | 48 | **52.0** |
| 2 | Steal-and-defend meme collection tycoon | 9 | 2 | 6 | 7 | 9 | 8 | 6 | 47 | **49.0** |
| 3 | Ragdoll "launch yourself" physics incremental | 6 | 6 | 8 | 5 | 6 | 8 | 5 | 44 | **48.3** |
| 4 | Co-op chaotic job sim (kitchen / delivery rush) | 6 | 7 | 6 | 6 | 5 | 7 | 6 | 43 | **46.3** |
| 5 | Fishing / digging collection sim | 7 | 4 | 6 | 8 | 7 | 5 | 7 | 44 | **46.3** |
| 6 | Asymmetric 1-vs-many horror PvP | 8 | 4 | 4 | 7 | 7 | 8 | 7 | 45 | **46.3** |
| 7 | Co-op forest / zombie survival (99 Nights-like) | 9 | 3 | 3 | 8 | 7 | 7 | 8 | 45 | **45.3** |
| 8 | "+1 per second" escape incremental | 8 | 3 | 9 | 4 | 6 | 6 | 4 | 40 | **44.3** |
| 9 | Cozy farming / garden live-ops | 7 | 2 | 5 | 8 | 8 | 5 | 7 | 42 | **43.3** |
| 10 | Daily-seed procedural tower (competitive obby) | 6 | 4 | 8 | 6 | 4 | 5 | 5 | 38 | **41.8** |
| 11 | Party mini-games / social deduction | 6 | 5 | 6 | 5 | 4 | 6 | 6 | 38 | **40.8** |
| 12 | Linear story horror run ("Doors-lite") | 7 | 4 | 5 | 4 | 5 | 7 | 5 | 37 | **39.3** |

### Concept briefs

Each brief covers: loop · audience · why try · why stay · competitors · differentiation · difficulty / MVP time · systems · monetization · viral angle · biggest risk. MVP times assume **~15–20 h/week** of your time with me writing most of the code.

1. **Co-op Anomaly Night Shift** *(full design in Step 6)*
   - **Loop:** work a night shift, spot anomalies, report or handle them, survive the night, upgrade the workplace.
   - **Audience:** 12–20, friend groups. **Why try:** a creepy, funny premise that's instantly clear. **Why stay:** procedural anomaly combos, an anomaly journal collection, upgrades, endless mode, daily anomaly.
   - **Competitors:** Scary Shawarma Kiosk, Animal Hospital, Home Alone (Anomaly). **Differentiation:** 4-player **role split** (desk / CCTV / runner) + procedural mixing + persistent upgrades.
   - **Difficulty:** low–medium. **MVP:** 6–8 weeks.
   - **Systems:** anomaly director, 1 map, role tools, lobby/teleport, DataStore, shop.
   - **Monetization:** revive / second-chance products, passes, cosmetics, private servers, rewarded ads.
   - **Viral:** reaction clips, "spot the anomaly" Shorts.
   - **Risk:** the trend is maturing, and content gets consumed fast.
2. **Steal-and-defend meme tycoon**
   - **Loop:** buy or hatch units, place them in your base, earn cash, steal from others, defend your own.
   - **Audience:** 8–15. **Why try / stay:** meme units and friend rivalry; collection completion.
   - **Competitors:** Steal a Brainrot, Steal an Egg + dozens of clones. **Differentiation:** needs an original mascot universe.
   - **Difficulty:** medium. **MVP:** 6–8 weeks. **Monetization:** strong (base locks, boosts, units). Unit sales are paid random items if eggs are used, so odds rules apply.
   - **Risk:** extreme saturation. Success relies on meme timing and daily live-ops, and Roblox is actively policing manipulative mechanics (Reels ban).
3. **Ragdoll launch incremental**
   - **Loop:** launch yourself, earn by distance, buy a stronger launcher, launch again.
   - **Audience:** 8–16. **Why stay:** big numbers and new zones.
   - **Competitors:** generic "+1" sims. **Differentiation:** hilarious physics and multiplayer cannon duels.
   - **MVP:** 3–4 weeks. **Monetization:** boosts, cosmetics, x2 passes. **Viral:** fail compilations.
   - **Risk:** shallow; weak Day-28 retention.
4. **Co-op chaotic job sim**
   - **Loop:** fulfil orders under time pressure with friends, earn stars, unlock new locations.
   - **Audience:** 10–18, friend groups. **Competitors:** fewer direct ones on Roblox. **Differentiation:** Overcooked-style chaos on mobile.
   - **MVP:** 7–9 weeks (network "feel" is tricky). **Monetization:** cosmetics, kitchens.
   - **Risk:** fun depends on precise netcode and level design.
5. **Fishing / digging collection sim**
   - **Loop:** cast or dig, run a timing minigame, catch, sell, upgrade gear, reach new zones.
   - **Competitors:** Fisch and others. **Differentiation:** needs a twist (co-op boats, creatures).
   - **MVP:** 8–10 weeks (lots of content). **Monetization:** strong.
   - **Risk:** content-hungry; dominated by established titles.
6. **Asymmetric horror PvP**
   - **Loop:** one killer vs survivors, completing objectives, escape.
   - **Competitors:** Forsaken-likes. **Difficulty:** high (balancing needs live CCU).
   - **Risk:** dead servers kill it at launch (cold start).
7. **Co-op survival 99 Nights-like**
   - **Difficulty:** high (AI enemies, crafting, large map, day/night). **MVP:** 12+ weeks.
   - **Risk:** scope, and direct comparison with a giant.
8. **"+1 per second" escape**
   - **MVP:** 2–3 weeks. **Risk:** the most-copied template on the platform (templates are even sold on BuiltByBit); poor retention.
9. **Cozy farm live-ops**
   - **Risk:** requires weekly content and events forever; the Grow a Garden comparison hurts.
10. **Daily-seed tower**
    - **Feasibility:** easy. **Risk:** weak monetization; Tower of Hell-likes already dominate.
11. **Party / social deduction**
    - **Risk:** needs many simultaneous players; low monetization; MM2 dominance.
12. **Story horror run**
    - **Risk:** content is consumed once; heavy art and level work per minute of play.

---

## STEP 5 — Top three

1. **Co-op Anomaly Night Shift with a persistent meta (weighted 52.0).** Best ratio of proven demand to solo build cost. Small map, content is "data" (anomaly definitions) that AI can help produce quickly, and the strongest organic clip engine. Our main improvement is fixing the genre's big weakness, running out of content, with procedural combos, roles, a collection journal and upgrades.
2. **Steal-and-defend meme tycoon (49.0).** The highest demand and monetization on the platform, but the most saturated, and it rewards studios that can update daily. Keep it as a **second-game candidate** once our pipeline is proven, not as game #1.
3. **Ragdoll launch incremental (48.3).** The cheapest viable game, at 3–4 weeks. A good **"second shot"** to test the marketing pipeline, or a fallback if game #1 tests poorly.

## STEP 6 — Recommendation: build the Co-op Anomaly Night Shift game

**Why this one, for our circumstances [Opinion, evidence-based]:**
- **Proven demand right now:** the anomaly genre produced a 1.27M-CCU game (Animal Hospital) and a 1.3B-visit game (Shawarma Kiosk) within the past 11 months.
- **It fits the 16+ gate:** creepy co-op horror appeals to teens and young adults, the audience a new game must win first. Moderate fear, no gore, keeps the Select (9–15) audience reachable later.
- **Solo-feasible:** one small map. The "content" is anomaly definitions (swap a painting, a guest with wrong eyes, a hallway that loops) that are cheap to add each week. Updates every 1–2 weeks are realistic.
- **Built-in marketing:** reactions to anomalies are exactly the kind of clips that spread on TikTok and Shorts, and the gameplay is spectator-friendly for YouTubers.
- **Reusable engine:** the anomaly director, role tools, save system and shop can be reskinned into a second and third setting (hospital → motel → ferry → ski lodge). That's the "repeatable process" you asked for.

**Honest counter-evidence:** Animal Hospital is down to ~¼ of its peak, so the genre may be past its top. We are **not** betting on another 1M-CCU hit. We're betting that a well-made, replayable entry can hold a profitable niche of thousands of DAU, and on building a reusable engine. The kill/pivot gates in Step 8 handle the downside.

### Working concept: **"Last Stop Motel"** (working title — check name availability)
- **Premise:** you and up to 3 friends work the night shift at a roadside motel where some guests… are not guests. Follow the rulebook, check guests in, watch the cameras, and report anomalies before dawn.
- **USP:** the first anomaly game built around **co-op roles + procedural anomaly mixing + a motel you upgrade between shifts**, so no two nights are the same and there's always a next goal.
- **Core loop (8–10 min per night):** shift starts → **Desk** checks guests against the night's rules (ID, room number, behaviour), **CCTV** watches hallway cameras for environmental anomalies, **Runner** physically inspects and fixes things → correct reports earn cash and stars, mistakes escalate threat (lights fail, a chase) → survive until 6 AM → spend cash on motel upgrades and tools → next night has new rules and combos.
- **Progression:** 5-night "week" story → Endless Night mode (score attack) → anomaly journal (collect all 60+, with rarity tiers) → motel upgrades (cosmetic rooms, functional tools: UV torch, master key, better cameras) → employee rank and titles.
- **Retention hooks:** a daily featured anomaly, weekly new anomalies, a journal-completion goal, rank, friend co-op streak bonus.
- **Maturity target:** Moderate fear, no blood, cartoon-creepy style.

### MVP scope (launch-essential vs later)
| Launch-essential (MVP) | Later (only if metrics justify) |
|---|---|
| 1 map: lobby, 2 hallways, parking lot, office | 2nd location / reskin |
| 1–4 players per server, solo playable | Matchmaking queue, trading |
| 20 anomalies (12 environment, 8 guest) with a procedural mixer | 60+ anomalies, rare "legend" anomalies |
| 3 roles with simple tools | Role skill trees |
| 5-night week + Endless mode | Daily challenge leaderboards, seasonal events |
| Save: cash, journal, upgrades, cosmetics (DataStore with session locking) | Badges, cross-game rewards |
| Shop: 2 game passes, 3 dev products, rewarded-ad revive | Battle pass, subscriptions |
| Mobile UI, tutorial night, settings | Voice-line localisation |
| Analytics funnel + economy events | A/B testing infrastructure |

### Development scope estimate **[Estimate]**
- **Time:** 6–8 weeks to MVP at 15–20 h/week. I write most Luau (server-authoritative anomaly director, data layer, receipts, UI logic); you do Studio placement, playtests, publishing and account tasks.
- **Tooling:** Roblox Studio's **built-in MCP server lets Claude Code read the open place, edit scripts and run playtests** **[Reported, community guides; Roblox lists Claude Code as a quick-connect client]**. Alternative: **Rojo** or Studio **Script Sync** to keep Luau in this git repo. Decide once we confirm your setup.
- **Assets:** Roblox Creator Store free models (check licence and scripts), plus simple low-poly modelling. Sound from licensed libraries (Roblox audio library, CC0 sources). No copying of competitors' assets or branding.

### Monetization model (fair, no pay-to-win over other players)
| Item | Type | Indicative price (R$) |
|---|---|---|
| Second Chance (revive self/teammate once this night) | Dev product | 25 |
| Revive via rewarded video ad | Ads | free |
| Night Manager Pass (+1 tool slot, manager uniform, 1.5× shift pay) | Game pass | 199 |
| Motel Radio (music + cosmetic jukebox) | Game pass | 79 |
| Cash bundles (for cosmetic upgrades) | Dev product | 49 / 149 / 399 |
| Uniform & room cosmetic sets | Dev product (later) | 50–150 |
| Private server | Private server | 50 / month |

No paid random items at launch, which avoids the odds and regional rules. Prices get tuned with Roblox price optimization tools after launch.

### Biggest risks
1. **Trend timing:** the genre may already be declining (see counter-evidence).
2. **The evaluation gate:** we must reach the engaged-16+ play threshold before younger players can even see the game.
3. **Content treadmill:** anomaly games need fresh content, so the anomaly pipeline must be fast.
4. **Monetization ceiling:** horror co-op typically monetizes below collection tycoons.
5. **Your own eligibility** for publishing to all ages and for DevEx (see Step 9).

### Marketing strategy (summary — details go in the 90-day plan)
- **Pre-launch (from week 3):** post 3–5 short clips per week on TikTok + YouTube Shorts: "spot the anomaly" puzzles (viewers comment the answer), dev-log "I'm building a horror game with AI", jump-scare reactions from playtests.
- **Launch:** an icon and thumbnail that show **one anomaly + a frightened clerk**, tested in Creator Hub thumbnail experiments. A small Sponsored Experiences test (about $30–50) **only after** D1 retention looks healthy. Agency-sourced benchmarks put the cost at roughly $0.10–$1 per player, an order-of-magnitude spread **[Reported, vendor data]**.
- **Creators:** contact 10–30 small Roblox horror YouTubers/TikTokers (10K–500K followers) with early access. No payment until the game proves retention.
- **Update rhythm:** a named update every 2 weeks ("The Night Auditor Arrives"), each with 3–5 new anomalies and a clip.
- **Measure:** use a separate custom link and code per channel, and compare **D1/D7 by acquisition source** in Creator Analytics (official feature). Views mean nothing unless those players come back.

---

## Revenue model & scenarios (STEP 4/7 of the brief: business model)

### How the money actually flows **[Official unless marked]**
1. A player buys Robux with real money. Roblox and app stores take their share before any Robux reaches you.
2. The player spends X Robux on your game pass or dev product → you receive **~70%** of the price as **Earned Robux** (the platform keeps ~30%).
3. **Creator Rewards** may add Robux for engagement and new-user acquisition, after a **60-day hold**.
4. **DevEx** converts Earned Robux to USD at **$0.0038 per Robux** (standard). The rate is **$0.0054** for qualifying spend by **age-verified U.S. 18+ players** (since 8 June 2026), and $0.0035 for balances earned before 5 Sept 2025.
5. **DevEx requirements:** **at least 30,000 Earned Robux** (= $114 at the standard rate), age 13+, account in good standing, verified email, a valid W-8/W-9 tax form, and DevEx terms acceptance. Only *earned* Robux count. Taxes in your own country still apply to what you receive.

> 100 R$ spent by a player in your game ≈ 70 Earned R$ ≈ **$0.27** at the standard DevEx rate. The player paid roughly **$1.00–$1.25** for those 100 Robux.

### Visits ≠ revenue
1M visits from players who leave after 2 minutes produces almost nothing: no purchases, poor recommendation signals, and no Creator Rewards. Revenue comes from **DAU × payer conversion × spend per payer**. DAU in turn depends on **retention**, because each day's DAU is mostly returning players.

### Three illustrative scenarios **[Estimate — illustrations, not predictions]**
Assumptions: monthly = 30 days; 70% creator share; DevEx $0.0038; Creator Rewards and ad revenue excluded (treated as upside); averages over a stable month.

| | Conservative | Moderate | Optimistic |
|---|---|---|---|
| Average DAU | 300 | 3,000 | 25,000 |
| Rough peak CCU equivalent (DAU÷10–20, rule of thumb) | 15–30 | 150–300 | 1,250–2,500 |
| Avg session length | 12 min | 18 min | 22 min |
| Payer conversion (daily) | 1.0% | 2.0% | 3.0% |
| Avg spend per payer per day (gross R$) | 150 | 200 | 250 |
| Daily gross R$ spent | 300×0.01×150 = **450** | 3,000×0.02×200 = **12,000** | 25,000×0.03×250 = **187,500** |
| Daily Earned R$ (×0.70) | 315 | 8,400 | 131,250 |
| **Monthly Earned R$** | **9,450** | **252,000** | **3,937,500** |
| Monthly USD via DevEx ($0.0038) | **~$36** | **~$958** | **~$14,960** |
| Months to reach the 30k-R$ DevEx minimum | ~3.2 | <1 | <1 |

**Sanity check:** the moderate case implies ~$0.011 of USD revenue per DAU per day. That's inside the $0.003–$0.025 range one 2026 analysis gives for conservative-to-well-monetized games **[Reported]**. Forum reports of ARPDAU vary 50× between similar games, mostly by audience geography **[Reported]**.

**Costs to subtract [Estimate]:** Roblox Plus $5/mo, or the refundable 1,000 R$ publishing fee; optional ads budget $50–300 per test; assets mostly free. Your time is the main cost.

**What would make this meaningful income [Opinion]:** sustaining **~3,000+ DAU** with **D1 ≥ 25%, D7 ≥ 8%**, **≥ 2% daily payer conversion** and an engaged 15+ min average session. Below ~1,000 DAU it's a learning project, not a business. One game rarely makes a business; a **portfolio built on a reusable engine** does.

---

## STEP 8 — 90-day plan (13 weeks, ~15–20 h/week)

Week 1 = week of 26 Oct 2026. Launch is targeted at **week 9 (~21 Dec)**, aligned with winter holiday traffic.

| Wk | Objective | Concrete tasks | Deliverable | Hours | Success criteria | Main risk |
|---|---|---|---|---|---|---|
| 1 | Verify & set up | Confirm Step 9 items (eligibility, country, DevEx); install Studio + MCP or Rojo; spend 2 h playing each of 3 competitors; write notes on what bores you | Verification checklist done; repo + Studio connected | 12 | Can publish a private test place; Claude Code can edit scripts | Eligibility blocker |
| 2 | Paper prototype + greybox | Greybox motel; 5 hard-coded anomalies; report button; night timer | Playable 1-player night | 18 | A friend understands it without explanation in < 60 s | Core not scary or fun |
| 3 | Anomaly director v1 | Data-driven anomaly definitions; server-side director spawns & validates; procedural combos | 10 anomalies, random each night | 18 | Two nights feel different | Over-engineering |
| 4 | Co-op roles | Desk / CCTV / Runner tools; 1–4 players; role select; server-validated reports | Co-op night | 20 | 3-friend playtest: they laugh/scream and want "one more night" | Netcode bugs |
| 5 | **Validation playtest #1** | 10+ external testers (16+); record sessions; quick survey | Playtest report | 15 | ≥ 60% want to play again; avg session ≥ 12 min. **If not: rework the core or pivot to concept #3** | Biased friend testers |
| 6 | Progression & save | DataStore (session lock, retries, autosave, BindToClose); cash, journal, upgrades; 5-night week + Endless | Persistent progression | 20 | No data loss across 50 test joins/leaves | Data corruption |
| 7 | Art, sound, UI, mobile | Lighting pass, low-poly props, ambience/stingers, mobile controls, tutorial night | Content-complete MVP (20 anomalies) | 20 | Stable 30+ FPS on a low-end phone (MicroProfiler) | Performance |
| 8 | Monetization + analytics + closed beta | Passes / products / ProcessReceipt (idempotent), rewarded-ad revive, AnalyticsService funnel + economy events, maturity questionnaire, icon + 3 thumbnails | Closed beta with 30–50 players | 18 | 0 purchase bugs; funnel shows where players drop | Receipt bugs |
| 9 | **Public launch (16+)** | Publish; pick 1,000 R$ fee or Plus; daily Shorts/TikTok; message 20 creators | Live game | 18 | D1 ≥ 20%, avg session ≥ 12 min in first 7 days | No traffic |
| 10 | Fix & first update | Fix top bugs from error report; Update #1 (+5 anomalies); thumbnail experiment | Update #1 | 16 | D1 improves vs week 9 | Fixing the wrong thing |
| 11 | Growth test | Sponsored ads test ($30–50) only if D1 ≥ 20%; creator outreach round 2 | Ad report (cost per *retained* player) | 14 | Ad-sourced D1 ≥ 15% | Burning money |
| 12 | Update #2 + economy tuning | +5 anomalies, daily featured anomaly, price tweaks; check Kids/Select evaluation status | Update #2 | 16 | Payer conversion ≥ 1%; evaluation passed or on track | Evaluation threshold not met |
| 13 | **Day-90 decision** | Review 30-day D1/D7/D28, ARPDAU, DAU trend vs the gates below | Go/iterate/pivot memo | 10 | See gates | Sunk-cost bias |

**Day-90 gates [Opinion]:**
- **Scale:** DAU ≥ 1,000 & D7 ≥ 8% → double down (2-week updates, ads, second location).
- **Iterate:** DAU 200–1,000 or D7 5–8% → one more 4-week iteration cycle on the weakest metric.
- **Pivot:** DAU < 200 & D7 < 5% → keep the engine (data, monetization, analytics modules) and ship concept #3 (ragdoll incremental, 3–4 weeks) or a reskinned anomaly setting.

### Weekly optimization loop (from launch)
Monday: read the dashboard (retention by source, session length, funnel drop-off, conversion, errors). Pick **one** metric to move → change one thing → ship by Friday → post a clip of the change → next Monday compare.

| Metric weak | Likely cause | First action |
|---|---|---|
| Low CTR (impressions → plays) | Icon/thumbnail/title | Thumbnail experiment, clearer anomaly in icon |
| Low D1 | First 5 minutes confusing or not scary | Shorten tutorial, guaranteed great anomaly in night 1 |
| Low D7/D28 | Nothing left to chase | More anomalies, journal rewards, daily anomaly, upgrades |
| Short sessions | Waiting / downtime | Faster lobby, shorter nights, instant replay |
| Low conversion | Offers not visible or not valued | Offer revive at the emotional moment; better pass value |
| Errors | Bugs | Error report in Creator Hub; fix before content |

---

## STEP 9 — What we must verify before committing

1. **Your eligibility (blocking):** your age (ID verification and DevEx require 13+; the higher U.S. 18+ rate and Roblox Wallet are U.S. 18+ only), country, and ability to complete **ID verification + 2FA**.
2. **Country restrictions:** whether Roblox and **DevEx payouts** work in your country of residence and with your tax status. Example: Roblox was blocked in Russia from Dec 2025 and its status in 2026 is reported inconsistently **[Reported]**. I note it only because this repository contains Russian-language code; ignore it if it doesn't apply to you. If payouts aren't possible, the business model changes completely.
3. **Current publishing rules:** read the live Creator Hub page for the evaluation threshold (250/60 days vs 500/30 days) and the 1,000 R$ fee.
4. **Live competitor data:** open RoMonitor/Rolimons history charts for Animal Hospital, Shawarma Kiosk and Home Alone (Anomaly) to confirm whether the genre's 90-day trend is flat, rising or falling. I couldn't access these.
5. **Creator Rewards current rules** (the per-player rate and audience-expansion terms are third-party claims).
6. **Retention claims:** confirm the 28-day algorithm window in an official Roblox source.
7. **Name and IP check:** "Last Stop Motel" isn't infringing, and no assets copy competitors.
8. **Your time budget:** confirm 15–20 h/week is realistic; the plan scales linearly with it.
9. **Q3 2026 earnings (29 Oct):** re-check platform trends and any monetization policy changes.

## STEP 10 — Recommendation and exact next actions

**Recommendation:** build **"Last Stop Motel"**, a co-op anomaly night-shift game with procedural anomalies, roles and a persistent upgrade/journal meta. Use a **6–8 week MVP**, launch around **21 Dec 2026**, and make a data-driven go / iterate / pivot decision at **day 90**. Build the code as a **reusable anomaly-game engine** so a second setting or game costs weeks, not months.

**Next actions (you):**
1. Answer the Step 9 eligibility questions: age bracket, country, Studio installed, weekly hours.
2. Play Scary Shawarma Kiosk and Animal Hospital for ~1 hour each and write 5 lines on what bored you.
3. Approve or challenge the concept (or pick #2/#3 instead).

**Next actions (me, after approval):**
1. Set up the project structure (Rojo or Script Sync + Claude Code via Studio MCP) and a `CLAUDE.md` with Roblox conventions.
2. Build week-2 deliverables: greybox-friendly scripts, the anomaly definition format, the server-side director and the report flow.
3. Draft the first 20 anomaly definitions and the pre-launch clip calendar.

---

## Sources
Accessed via search on 22 Oct 2026; I couldn't open the pages directly.

**Official (Roblox / SEC)**
- [Developer Exchange Program](https://create.roblox.com/docs/production/monetization/developer-exchange) · [U.S. 18+ exchange rate](https://create.roblox.com/docs/production/monetization/18-plus-devex-rate) · [Developer Products](https://create.roblox.com/docs/production/monetization/developer-products)
- [New Publishing Requirements & Evaluation Process](https://devforum.roblox.com/t/new-publishing-requirements-evaluation-process-for-games/4573166) · [Alternate Publishing Requirements for Kids and Select](https://devforum.roblox.com/t/alternate-publishing-requirements-for-roblox-kids-and-select/4630944) · [Roblox Kids and Select docs](https://create.roblox.com/docs/production/publishing/kids-and-select) · [AMA](https://devforum.roblox.com/t/ama-publishing-requirements-roblox-kids-select/4580953)
- [Content Maturity docs](https://create.roblox.com/docs/production/promotion/content-maturity)
- [How we are improving Home this year](https://devforum.roblox.com/t/how-we-are-improving-home-this-year/4502571) · [Improved Recommended For You algorithm](https://devforum.roblox.com/t/boost-your-discovery-with-the-improved-recommended-for-you-algorithm-and-analytics-for-creators/3587441)
- [Introducing Creator Rewards](https://devforum.roblox.com/t/introducing-creator-rewards-earn-more-by-growing-the-community/3777628)
- [Rewarded Video ads for all ads-eligible creators](https://devforum.roblox.com/t/rewarded-video-ads-are-now-available-to-all-ads-eligible-creators/4063278) · [Rewarded Video enhancements](https://devforum.roblox.com/t/boost-your-game-earnings-with-rewarded-video-enhancements/4645335)
- [Clarifying Requirements for Paid Random Items](https://devforum.roblox.com/t/clarifying-requirements-for-paid-random-items/4654622)
- [Analytics retention docs](https://create.roblox.com/docs/production/analytics/retention) · [Retention by acquisition source & benchmark set](https://devforum.roblox.com/t/analytics-view-retention-by-acquisition-source-and-select-your-benchmark-set/4010157) · [Monetization analytics (GitHub docs)](https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/monetization.md)
- [Studio MCP Server updates](https://devforum.roblox.com/t/studio-mcp-server-updates-and-external-llm-support-for-assistant/4415631)
- [Age checks for chat (IR)](https://ir.roblox.com/news/news-details/2026/Roblox-Requires-Users-Worldwide-to-Age-Check-to-Access-Chat/default.aspx) · [Kids and Select accounts (newsroom)](https://about.roblox.com/newsroom/2026/04/introducing-roblox-kids-and-select-accounts)
- [RDC 2026 newsroom](https://about.roblox.com/newsroom/2026/09/rdc-2026-the-world-needs-more-play) · [RDC press release](https://ir.roblox.com/news/news-details/2026/Roblox-Unveils-New-Ways-to-Play-Build-and-Grow-at-the-Roblox-Developers-Conference-RDC/default.aspx) · [Roblox at GDC 2026](https://about.roblox.com/newsroom/2026/03/roblox-gdc-2026)
- [Q4 2025 shareholder letter (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/1315098/000131509826000009/ex991-q42025shareholder.htm) · [Q1 2026 shareholder letter](https://s27.q4cdn.com/984876518/files/doc_financials/2026/q1/Q1-2026-Earnings-Shareholder-Letter.pdf) · [Q2 2026 8-K](https://www.sec.gov/Archives/edgar/data/0001315098/000162828026051059/ex991-robloxq22026earnin.htm) · [Q3 2026 results date](https://ir.roblox.com/news/news-details/2026/Roblox-to-Report-Third-Quarter-2026-Financial-Results-on-October-29-2026/default.aspx)

**Reported (press, trackers, industry)**
- [Investing.com — Q2 2026 slides](https://www.investing.com/news/company-news/roblox-q2-2026-slides-bookings-growth-slows-to-8-amid-user-decline-93CH-4826401) · [Q2 2026 call transcript](https://www.investing.com/news/transcripts/earnings-call-transcript-roblox-q2-2026-beats-eps-but-shares-sink-on-bookings-93CH-4826338)
- [Yahoo Finance / TIKR — Steal an Egg & Q3](https://www.tikr.com/blog/roblox-stock-is-down-37-in-2026-heres-what-its-new-viral-hit-has-to-prove-on-october-29) · [Aream & Co Q3 2026 report](https://investgame.net/wp-content/uploads/2026/10/aream_co._video_game_market_report_q3_2026.pdf) · [Otakukart — Steal an Egg](https://otakukart.com/robloxs-steal-an-egg-reaches-6-billion-visits-and-14-2-million-peak-concurrent-players)
- [Kotaku — Roblox bans doomscrolling mechanic](https://kotaku.com/roblox-cracks-down-on-doomscrolling-games-like-steal-an-egg-that-forces-players-to-watch-reels-while-running-on-a-treadmill-2000727952)
- [Wikipedia — Steal a Brainrot](https://en.wikipedia.org/wiki/Steal_a_Brainrot) · [Grow a Garden](https://en.wikipedia.org/wiki/Grow_a_Garden) · [List of Roblox games](https://en.wikipedia.org/wiki/List_of_Roblox_games)
- [Livecounts Roblox charts](https://livecounts.nl/roblox-charts/) · [RBLXSTAT records](https://rblxstat.com/lists/record-breaking-roblox-games) · [Rotrends — Scary Shawarma Kiosk](https://rotrends.com/game/8539298853/Scary-Shawarma-Kiosk-the-ANOMALY-horror)
- [ComicBook — anomaly horror trend](https://comicbook.com/gaming/news/robloxs-next-big-horror-trend-has-players-searching-for-anomalies-and-some-are-seriously-scary/) · [GosuGamers — Animal Hospital](https://www.gosugamers.net/entertainment/news/78741-animal-hospital-becomes-roblox-s-latest-horror-sensation-here-s-everything-you-need-to-know) · [spottheanomaly.wiki — genre timeline](https://spottheanomaly.wiki/anomaly-games)
- [Naavik — State of UGC Games 2026](https://naavik.co/deep-dives/the-state-of-ugc-games-2026/)
- [Lensblox — June 2026 algorithm change](https://lensblox.com/blog/roblox-algorithm-change-2026-explained/) · [PCGamesN — publishing eligibility](https://www.pcgamesn.com/roblox/eligibility-to-upload-games) · [PiunikaWeb — Roblox Plus & DevEx rate](https://piunikaweb.com/2026/05/01/roblox-raises-devex-by-42-us-18-above-players/)
- [RoWatcher — DevEx math 2026](https://rowatcher.com/news/devex-math-in-2026-what-you-actually-take-home-per-1-000-players) · [BLOXG ad benchmarks (vendor)](https://bloxg.com/statistics/roblox-advertising-benchmarks) · [BloxClips — TikTok promotion (vendor)](https://www.bloxclips.com/articles/how-to-promote-a-roblox-game-on-tiktok)
- [Meduza — Russia Roblox ban status](https://meduza.io/en/news/2026/06/09/russia-s-digital-ministry-seeks-to-lift-roblox-ban-saying-the-platform-has-agreed-to-meet-government-requirements)
