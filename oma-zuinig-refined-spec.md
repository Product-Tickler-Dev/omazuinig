# Oma Zuinig — Refined Product Specification

**Version 2.0 | March 2026**
**Status**: Research-validated, ready for design & implementation planning

---

## 1. What This Is (And What It Isn't)

**Oma Zuinig** is a Dutch grocery price comparison app that tells you which supermarket is cheapest for your shopping list. It covers Albert Heijn, Jumbo, Lidl, Aldi, Plus, Dirk, and more. It's wrapped in a warm, distinctly Dutch personality — a thrifty grandmother character — that makes the experience feel human instead of clinical.

**Core promise**: You type your groceries. Oma tells you where to buy them cheapest. You save money every week.

**What it is NOT**:
- Not a grocery delivery app
- Not a coupon/cashback platform (Scoupy already owns that)
- Not a recipe app or meal planner (that's a future layer, not the core)
- Not a general deals aggregator (Supermarktaanbiedingen.com does that)

**The gap we fill**: Existing Dutch tools (SmartKoop, Checkjebon, Btrkoop) offer price comparison but with zero emotional connection. They're spreadsheets with logos. No one tells their friends about a spreadsheet. Oma Zuinig is the first Dutch grocery app people will *recommend* because it has personality, not just function.

---

## 2. Market Reality (Validated)

### The Numbers

| Metric | Value | Source |
|--------|-------|--------|
| Dutch grocery market size | ~€47B/year | CBS 2025 |
| AH market share | 38.2% (and growing) | Distrifood 2025 |
| Jumbo market share | 19.9% (declining) | Distrifood 2025 |
| Lidl market share | ~11.5% (gaining) | Distrifood 2025 |
| Plus (post-Coop merger) | ~10% | Distrifood 2025 |
| Consumers concerned about grocery prices | 87% | GfK 2025 |
| Consumers who switched primary store | 33% | GfK 2025 |
| Private label share of sales | 42-47% | Euromonitor 2025 |
| Average store visits per week | ~3 | Consumer panel data |
| Online grocery share of total | 3-4% | Distrifood 2025 |
| Food inflation (NL, 2025) | 3.7% | CBS Sept 2025 |

### Competitive Landscape

| App | What It Does | Users | Weakness |
|-----|-------------|-------|----------|
| **Supermarktaanbiedingen** | Aggregates weekly deals/folders | Large | Not true price comparison — just promotions |
| **Scoupy** | Cashback on specific products | 1M+ | Not price comparison — pay-to-participate for brands |
| **SmartKoop** | True cross-store price comparison | Small | No personality, no mobile-first UX, no brand |
| **Checkjebon** | Open-source, browser-only comparison | Niche | Technical audience, no app, privacy-maximalist |
| **Btrkoop** | Comparison + receipt scanning | Small | No differentiation, limited visibility |

**Key insight**: No existing app combines true multi-supermarket price comparison with a consumer brand that people actually want to use. The functional gap is small (SmartKoop exists). The *emotional* gap is massive.

### Regulatory Tailwind

The ACM (Netherlands Authority for Consumers & Markets) launched a formal investigation into Dutch supermarket pricing in September 2025, with results expected summer 2026. The Consumentenbond found that 9 supermarket chains simultaneously claim to be "the cheapest." The Omnibus Directive now requires 30-day lowest-price disclosure for discounts. **Price transparency is becoming a regulatory priority.** Oma Zuinig rides this wave.

---

## 3. Brand Identity (Reworked)

### Heritage — Honest Version

The original spec tied Oma Zuinig to the "Old Dutch Cleanser" mascot (1903). **This connection is fabricated.** Old Dutch Cleanser is a North American brand that traded on American stereotypes of Dutch cleanliness. It has virtually zero recognition in the Netherlands. Claiming this heritage would feel forced and inauthentic to Dutch consumers.

**The real heritage**: Oma Zuinig draws from genuinely Dutch archetypes:

- **The zuinige huisvrouw**: A real, deeply-rooted Dutch cultural identity. The Netherlands has centuries of Calvinist-influenced frugality ("doe maar normaal, dan doe je al gek genoeg"). Thrift is not embarrassing in Dutch culture — it's a point of pride.
- **The Dutch oma**: Universally beloved figure. Warm, direct, opinionated, slightly sassy. Every Dutch person has (or wishes they had) an oma who told them not to waste money.
- **"Kijken kijken, niet kopen"**: The classic Dutch market browsing phrase. This is real cultural shorthand that every Dutch person knows.
- **Loeki de Leeuw & Dutch mascot tradition**: The Netherlands has a proven history of warm, unpretentious mascot characters in media and advertising.

### Personality

- **Warm but not saccharine**. Dutch *nuchterheid* (sobriety/directness) means she never tries too hard. She's your oma, not a cheerleader.
- **Dry humor, not wacky**. "Tja, alles is duur tegenwoordig. Maar niet als Oma meekijkt." Not "OMG SUPER DEALS!!!!"
- **Empowering, not patronizing**. She gives you information and celebrates when you save. She doesn't lecture or guilt-trip (important: this is NOT Duolingo — grocery shopping is a chore, not an aspiration).
- **Occasionally opinionated**. "Die is veel te duur, lieverd. Jumbo heeft 'm voor de helft."

### Voice Examples

| Context | Oma Says |
|---------|----------|
| Welcome | "Hoi lieverd, laten we kijken wat er goedkoop is vandaag." |
| Good deal found | "Kijk eens aan! Dat scheelt weer." |
| Scan result | "Slim gescand. Oma heeft even rondgekeken voor je." |
| Expensive item | "Hmm, die is wel pittig geprijsd. Zal ik even zoeken?" |
| Weekly savings | "€14,20 bespaard deze week. Goed bezig!" |
| Nothing cheaper | "Tja, soms is alles gewoon even duur." |
| Error | "Even geduld, lieverd. Oma's bril is beslagen." |

### What Oma Is NOT

- **Not "unhinged" like Duo.** The Duolingo strategy works because language learning is aspirational and streaks create loss aversion. Grocery shopping is utilitarian. An aggressive/meme-driven personality would irritate Dutch adults using a utility app.
- **Not ever-present.** Oma appears at key moments (savings found, scan results, milestones) but stays out of the way during task-focused interactions like list editing or browsing. Users can dial her down.
- **Not a children's character.** The visual design should feel warm and distinctive, not childish. Think illustrated, not Pixar 3D. More "Fiep Westendorp meets modern app" than "cartoon grandma."

---

## 4. Visual Design System

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| **Dutch Orange** | `#FF6200` | Primary brand, headers, logo |
| **Savings Green** | `#00C853` | Best-price badges, savings highlights |
| **Deep Blue** | `#0052CC` | Accents, secondary actions |
| **Warm Cream** | `#FFF9F0` | Backgrounds (warm paper feel) |
| **Alert Red** | `#E6392E` | "Duur" tags, price warnings |
| **Neutral Dark** | `#1C1C1C` | Body text |

### Typography

- **Headings**: Inter Bold (clean, readable, modern)
- **Body**: Inter Regular
- **Oma's speech**: A handwritten-style font for personality. Consider "Caveat" or a custom "Oma Script" — but used sparingly (speech bubbles only, never body text).

### Mascot Direction

**Illustration style**: Warm, flat illustration with subtle textures. Not 3D Pixar. Think along the lines of Dutch children's book illustration (Fiep Westendorp, Dick Bruna's warmth) but for adults. Clean lines, expressive but simple.

**Core elements**:
- Gray hair in a bun
- Round glasses (warm, not trendy)
- Apron (practical, not costume-y)
- A broom or shopping basket as signature prop
- Rosy cheeks, warm smile
- A handful of key poses: waving, pointing, thumbs-up, shrugging, sweeping

**Where Oma appears**:
- App icon (her face)
- Welcome/onboarding
- Search results (small avatar + speech bubble when savings found)
- Empty states and errors
- Weekly savings summary
- Push notifications (icon)

**Where Oma does NOT appear**:
- Every single screen
- Blocking the UI
- During list editing or other focused tasks
- In a way that slows down task completion

---

## 5. Core Features (MVP)

### 5.1 Smart Shopping List ("Mijn Lijst")

**This is the killer feature. Not barcode scanning. Not deals. The list.**

The user builds a shopping list. For each item, Oma shows the price at every supermarket. At the bottom: the cheapest total, and which store(s) to visit.

- Add items by typing (autocomplete from product database)
- Each item shows price across all chains with the cheapest highlighted
- "Oma's Advies" at the bottom: "Alles bij Lidl: €47,20. Of split: Lidl + AH = €43,80 (besparing: €3,40)"
- Option to optimize for one store vs. split across stores
- Check items off while shopping
- Lists persist offline (IndexedDB)
- Share lists with household members (future: real-time sync)

### 5.2 Search & Compare ("Vergelijk")

Search for any product, see prices across all supermarkets instantly.

- Search by product name
- Results show: product image, price per store, unit price (per kg/L), price history sparkline
- "Oma's Beste Keuze" badge on the cheapest option
- Filter by category, dietary needs, brand vs. private label

### 5.3 Barcode Scan ("Scan")

Point your camera at a product barcode, get instant comparison.

- Camera-based EAN-13 scanning
- Results identical to Search & Compare
- This is a *supplementary* feature, not the core UX. Most users will use Search & List.
- Degrade gracefully if camera access denied (show manual search)

### 5.4 Weekly Deals ("Aanbiedingen")

Curated view of this week's best promotions across all stores.

- Aggregated from all chains' weekly folders
- Filterable by category
- "Hamsteralert" badge for unusually deep discounts (>40% off)
- Oma's commentary on the best picks

### 5.5 Profile & Savings ("Mijn Besparingen")

Your savings dashboard.

- Lifetime savings counter
- Weekly/monthly savings graph
- Thrift level system (gentle gamification, not aggressive)
  - Levels: Beginner → Slimme Shopper → Koopjeskoning → Gouden Oma
- Preferred stores setting (filter results to stores near you)
- Notification preferences (daily deals, weekly summary, or off)

---

## 6. What We Defer (Post-MVP)

- Family/household sharing with real-time list sync
- Recipe integration ("add ingredients to list")
- "Direct bestellen" links to online delivery
- Receipt scanning for automatic price tracking
- Push notifications (requires PWA install or native app)
- Store locator / distance-based optimization
- Price alerts ("notify me when X drops below €Y")

---

## 7. Technical Architecture (Research-Validated)

### Why NOT Flutter

The original spec proposed Flutter. Research conclusively shows this is wrong for a price comparison app:

| Flutter Web Problem | Impact |
|---|---|
| Canvas rendering = invisible to search engines | No SEO. Users searching "goedkoopste melk" will never find you. |
| ~14x heavier bundles than standard web | Slow loads on mobile. Users bounce. |
| Accessibility is opt-in, broken by default | EU accessibility compliance risk |
| No standard DOM = no browser features (print, right-click, text select) | Feels alien, not native-web |

**Flutter is good for app-first products (games, complex UIs). Oma Zuinig is a content-first product where SEO, performance, and web-nativeness are critical.**

### Recommended Stack

```
┌─────────────────────────────────────────────────┐
│                    Frontend                      │
│  SvelteKit (SSR/SSG) → PWA → Capacitor (native) │
│  • Smallest bundles (~1.6 KB runtime)            │
│  • Full SSR = excellent SEO                      │
│  • PWA: offline lists, installable               │
│  • Capacitor: iOS/Android wrappers when ready    │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│                  Backend / BaaS                   │
│  Supabase (Frankfurt region)                     │
│  • PostgreSQL for products, prices, users         │
│  • Auth (anonymous + account)                     │
│  • Edge Functions for API logic                   │
│  • Realtime subscriptions for price updates       │
│  • GDPR-compliant EU hosting                      │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│               Price Data Pipeline                 │
│  Docker containers (one per supermarket chain)    │
│  → Redis message queue (Upstash)                  │
│  → Normalization service (product matching)       │
│  → PostgreSQL (source of truth)                   │
│  → Redis cache (hot data, 4hr TTL)               │
│                                                   │
│  Sources:                                         │
│  • SupermarktConnector (AH, Jumbo APIs)           │
│  • Apify "Dutch Supermarkets all 11"              │
│  • Pepesto API (commercial fallback)              │
│  • Custom scrapers where needed                   │
│                                                   │
│  Schedule: Daily full scrape + 4x/day promos      │
└─────────────────────────────────────────────────┘
```

### Barcode Scanning

- **MVP**: `html5-qrcode` library (free, supports EAN-13, easy setup)
- **Production upgrade**: STRICH SDK (commercial, WASM-based, reliable)
- **Fallback**: Manual search always available if camera fails

### Key Infrastructure Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Hosting | Vercel (SvelteKit) + Supabase (Frankfurt) | Fast deploys, EU data residency |
| Caching | Redis via Upstash (serverless) | Hot price data, search results |
| Offline | Service Workers + IndexedDB | Native PWA capability, no extra deps |
| Product matching | Custom normalization service | Hardest technical problem — EAN matching for brands, fuzzy matching for private labels |
| Image storage | Supabase Storage or Cloudflare R2 | Product images scraped from chains |

### The Hard Problem: Product Matching

Cross-chain product matching is the single hardest technical challenge. "AH Halfvolle Melk 1L" and "Jumbo Halfvolle Melk 1 Liter" are the same product but named differently.

**Approach**:
1. **EAN-13 barcode as primary key** — works for ~60% of branded products
2. **Unit-price normalization** — compare per kg/L across chains
3. **Fuzzy text matching** — Levenshtein distance + category + package size
4. **Manual curation layer** — crowdsourced corrections + editorial review
5. **Store brands treated separately** — AH Huismerk ≠ Jumbo Huismerk (different products)

### Data Scale Estimates

| Metric | Estimate |
|--------|----------|
| Products tracked | ~100,000-200,000 across 8+ chains |
| Price points | ~800,000 (products × chains) |
| Daily scrape data | ~500 MB |
| Database after Year 1 | ~10 GB (with price history) |
| Infrastructure cost (Year 1) | ~€50-150/month |

---

## 8. Monetization (Reality-Checked)

### What Doesn't Work

- **Grocery affiliate commissions**: Dutch supermarkets don't offer ongoing basket commissions. Only one-time CPA bounties (€2-5 for new online delivery customers) via Daisycon/TradeTracker. This depletes fast and yields ~€15-30K/year. **Not a primary revenue stream.**
- **Merch**: App mascot merchandise has never generated meaningful revenue for any utility app (even Duolingo's merch is negligible vs. subscriptions). **Marketing expense, not revenue.**

### What Does Work

#### 1. Premium Subscription — "Oma Plus" (Primary Revenue, ~45%)

| Feature | Free | Oma Plus (€2,99/mo or €29/yr) |
|---------|------|------|
| Price comparison (up to 10 items/list) | Yes | Yes |
| Unlimited list items | No | Yes |
| Price history graphs | No | Yes |
| Multi-store split optimization | No | Yes |
| Barcode scanning | 5/day | Unlimited |
| Ad-free | No | Yes |
| Household sharing (future) | No | Yes |
| "Oma's Geheime Deals" (exclusive finds) | No | Yes |

**Conversion target**: 3-5% of MAU at €2,99/month.

#### 2. FMCG Sponsored Placements (~30%)

Supermarkets won't pay you. **Brands will.** Unilever, Heineken, FrieslandCampina, Nestlé — they pay for visibility in the shopping context.

- Promoted products in search results ("Aanbevolen")
- Branded deal highlights ("Nieuw van Heineken")
- Category sponsorship
- CPC model: €0.15-0.50 per click

**This is the Instacart playbook** (Instacart's ad business does $1B+/year).

#### 3. Data Licensing (~15%)

Aggregated, anonymized shopping behavior → sold to FMCG companies and market researchers.

- Which products are most price-compared?
- What are switching patterns between brands?
- Regional price sensitivity data

**Requires**: GDPR-compliant anonymization, B2B sales capability. Slow to build but high-margin.

#### 4. Affiliate / Referral (~5%)

Supplementary: one-time CPA bounties for online grocery delivery sign-ups (AH, Jumbo, Picnic, Crisp).

### Revenue Projections (Conservative)

| | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| **MAU** | 50K | 200K | 400K |
| **Premium subscribers** | 1,500 (3%) | 8,000 (4%) | 20,000 (5%) |
| **Subscription revenue** | €54K | €287K | €718K |
| **FMCG sponsored placements** | €0 | €100K | €400K |
| **Data licensing** | €0 | €0 | €150K |
| **Affiliate/other** | €10K | €25K | €40K |
| **Total revenue** | **€64K** | **€412K** | **€1.3M** |

**Note**: The original spec claimed €2M by Year 3 with 500K MAU. That's optimistic. **€1-1.5M with 400K MAU** is more realistic and still an excellent business. Reaching 400K MAU (3% of Dutch smartphone users) requires strong organic growth via SEO, word-of-mouth, and social sharing.

---

## 9. Launch Strategy

### Phase 1: Foundation (Weeks 1-8)

**Goal**: PWA live on omazuinig.nl with core functionality.

- SvelteKit app with SSR (SEO from day one)
- Price data pipeline covering AH, Jumbo, Lidl, Aldi, Plus, Dirk
- Smart shopping list with multi-store comparison
- Search & compare
- Basic barcode scanning
- Oma personality layer (speech bubbles, savings celebrations)
- Installable PWA with offline lists

### Phase 2: Growth (Weeks 9-16)

**Goal**: Expand coverage, start monetization.

- Weekly deals aggregation
- Savings dashboard & thrift levels
- Oma Plus subscription launch
- Push notifications (for installed PWA users)
- Product matching refinement (ML-assisted fuzzy matching)
- Social sharing ("Ik heb €14 bespaard met Oma Zuinig!")

### Phase 3: Scale (Months 5-9)

**Goal**: Native apps, FMCG revenue.

- Capacitor-wrapped iOS + Android apps (same codebase)
- FMCG sponsored placements platform
- Household/family list sharing
- Price alerts
- Receipt scanning for automatic tracking

### Phase 4: Expand (Months 10-12+)

**Goal**: Full revenue engine.

- Data licensing partnerships
- Recipe integration (add recipe ingredients to list)
- Store locator with distance-based optimization
- API for third-party integrations
- Possible expansion to Belgium (overlapping chains: AH, Lidl, Aldi)

---

## 10. Animations & Interactions

Mascot-driven interactions should be **subtle, fast, and optional**. Every animation must serve a purpose: confirming an action, celebrating a save, or providing feedback.

| Interaction | Animation | Duration |
|-------------|-----------|----------|
| Savings found | Green badge slides in + subtle confetti | ≤250ms |
| Barcode scanned | Scan line animation → results card | ≤300ms |
| Item added to list | Item slides into list with soft bounce | ≤200ms |
| Weekly savings total | Number counts up with sparkle | ≤400ms |
| Loading state | Oma's broom gently sweeps | Loop |
| Error/empty state | Oma shrug illustration (static, no animation) | — |
| Achievement unlocked | Badge + Oma thumbs-up + speech bubble | ≤500ms |

**Rules**:
- All animations ≤300ms (400ms max for celebrations)
- 60fps minimum, no jank
- Every animation can be turned off in settings ("Rustige modus")
- Use CSS animations where possible, Lottie/Rive for complex mascot animations only
- No sound effects (unless user explicitly enables them)

---

## 11. Success Metrics

### North Star: Weekly Active Savings

How much money does the average user save per week by using Oma Zuinig?

**Target**: €8+ per active user per week.

### Supporting Metrics

| Metric | Target (Year 1) | Why It Matters |
|--------|-----------------|----------------|
| MAU | 50K | Growth |
| WAU/MAU ratio | >50% | Stickiness (grocery is weekly) |
| Lists created per user/week | >1.5 | Core engagement |
| Items per list | >8 | Depth of use |
| Premium conversion | 3% | Revenue |
| NPS | >50 | Word-of-mouth potential |
| Organic search traffic share | >40% | Sustainable acquisition |
| App store rating | 4.6+ | Trust & downloads |

---

## 12. Key Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Supermarkets block scraping | HIGH | Use commercial intermediaries (Pepesto, Apify). Diversify data sources. Build toward partnerships. ACM investigation creates political cover for price transparency tools. |
| Product matching quality | HIGH | Start with EAN-matched branded products (reliable). Add private labels gradually with human-in-the-loop QA. Be transparent about coverage gaps. |
| Low user acquisition | MEDIUM | SEO-first strategy (SSR, product pages indexed). Social sharing features. Dutch PR / media coverage of the ACM investigation angle. |
| Mascot feels cringe | MEDIUM | User testing with Dutch consumers before launch. "Rustige modus" setting. Oma is optional, never blocking. |
| Price data staleness | MEDIUM | 4x daily scrape for promos. Show "laatst bijgewerkt" timestamps. User-submitted corrections. |
| Subscription conversion too low | MEDIUM | Generous free tier to build habit. Clear ROI messaging ("Oma Plus betaalt zichzelf terug in 1 week"). |
| Legal challenge from supermarket | LOW | Non-personal data scraping is legally defensible. Use intermediary APIs. Build public goodwill (consumer advocacy angle). |

---

## 13. What Makes This a Real Business

1. **The demand is proven**: 87% of Dutch consumers worry about grocery prices. They already visit 3 stores/week hunting deals. We just make that easier.

2. **The gap is real**: SmartKoop proves the functional concept works. But it has no brand, no SEO, no mobile experience. We build the version people actually want to use and tell their friends about.

3. **The data moat deepens over time**: Price history, product matching quality, and user behavior data compound. Newcomers can't replicate years of data.

4. **SEO is a sustainable channel**: Every product page is indexable. "Goedkoopste melk" or "AH vs Jumbo prijs" searches bring free, high-intent traffic forever.

5. **The regulatory environment is turning in our favor**: ACM is investigating supermarket pricing. Omnibus Directive requires price disclosure. The political wind is behind transparency tools.

6. **The domain is secured**: omazuinig.nl is ours.

---

*This specification has been validated against current market research, competitive analysis, technical feasibility studies, and monetization benchmarks. It replaces the original grok.txt with corrected data, honest projections, and a technically sound architecture.*
