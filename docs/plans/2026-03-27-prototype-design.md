# Oma Zuinig Interactive Prototype — Design Document

**Date**: 2026-03-27
**Type**: High-fidelity interactive HTML/CSS/JS prototype
**Scope**: 5 screens with navigation, mock data, Oma personality, full design system

---

## Tech

Single HTML file (or small set of files) with inline CSS + vanilla JS. No framework needed for a prototype. Mobile-first (375px), responsive up to desktop.

## Design System

### Colors
- Primary Orange: `#FF6200`
- Savings Green: `#00C853`
- Deep Blue: `#0052CC`
- Warm Cream: `#FFF9F0`
- Alert Red: `#E6392E`
- Neutral Dark: `#1C1C1C`

### Typography
- Headings: Inter Bold
- Body: Inter Regular
- Oma speech: Caveat (handwritten feel)

### Components
- Bottom nav: 5 tabs (Home, Lijst, Vergelijk, Deals, Mijn Oma)
- Store badges: Small colored pills with store logo/name + price
- Deal cards: Image, price, discount badge, store logo
- Oma speech bubble: Rounded, cream background, Caveat font, small Oma avatar
- Green "Beste Keuze" stamp
- Orange "Hamsteralert" badge
- Red "DUUR" tag (struck through)

---

## Screens

### 1. Home
- Top: Logo + winking Oma icon
- Hero banner (orange gradient): "Hoi lieverd! Oma heeft vandaag €14,20 voor je bespaard!"
- 3 quick-action cards: Mijn Lijst, Vergelijk, Scan
- Horizontal scrolling top deals (4-5 cards)
- Bottom nav

### 2. Mijn Lijst
- Header: "Mijn Boodschappenlijst" + item count
- Search input: "Voeg product toe..."
- List items: product name, image, price badges per store (cheapest = green)
- Checkbox to complete items
- Sticky footer: "Oma's Advies" with total + savings + optimization toggle (1 winkel / Slim splitsen)
- Oma speech bubble on add: "Slim bezig!"

### 3. Vergelijk
- Large search bar: "Zoek een product..."
- Category filter pills (Zuivel, Brood, Vlees, Groente, Dranken)
- Result cards: product image, price per store, unit price, "Oma's Beste Keuze" badge
- "Voeg toe aan lijst" button per result
- Loading state: "Oma kijkt even rond..."

### 4. Aanbiedingen
- Store filter tabs (All, AH, Jumbo, Lidl, Aldi, Plus, Dirk)
- "Oma's Toppers" featured section (3 picks + speech bubble)
- Deal card grid: image, store logo, original price struck through, deal price green, discount %, "Hamsteralert!" badge on >40%
- Tap → detail with "Voeg toe aan lijst"

### 5. Mijn Oma
- Large Oma illustration with speech bubble: "Goed bezig, lieverd!"
- Lifetime savings counter (big number, green)
- Weekly/monthly savings bar graph
- Thrift level: progress bar + level name (Beginner → Slimme Shopper → Koopjeskoning → Gouden Oma)
- Preferred stores setting
- Notification preferences

---

## Mock Data

Dutch grocery products with realistic prices across AH, Jumbo, Lidl, Aldi, Plus, Dirk:
- Halfvolle melk 1L
- Gouda kaas jong belegen 500g
- Brood volkoren
- Eieren 10 stuks
- Heineken pils 6-pack
- Douwe Egberts koffie 500g
- Calvé pindakaas 650g
- Paprika rood per stuk
- Hagelslag melk 400g
- Karnemelk 1L

## Interactions

- Bottom nav switches screens (no page reload)
- Add item to list → slide animation + Oma speech bubble
- Search → brief loading state → results
- Store filter tabs → filter deals
- Checkboxes → strike through items
- Optimization toggle → recalculates Oma's Advies

## Oma Moments

- Home: greeting in hero banner
- List: speech bubble when adding item, advies in footer
- Search: loading message, Beste Keuze badge
- Deals: Oma's Toppers picks
- Profile: celebration message based on savings level
- Error/empty: "Tja, soms is alles gewoon even duur."
