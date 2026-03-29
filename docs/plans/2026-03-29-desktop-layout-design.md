# Desktop Responsive Layout Design

## Decision Summary
- **Approach:** Desktop layout shell + adaptive page layouts (Approach 2)
- **Breakpoint:** 768px (single breakpoint, mobile below, desktop above)
- **Reference:** Hagglezon.com for wide content patterns
- **Navigation:** Bottom nav on mobile, top nav bar on desktop (DesktopNav)

## App Shell (≥768px)
- Remove 480px max-width cap → content max-width 1200px, centered
- DesktopNav: sticky top bar, white bg, subtle border-bottom
  - Left: Oma avatar + "Oma Zuinig"
  - Center: nav links (Home, Lijst, Vergelijk, Deals, Mijn Oma) with icons
  - Right: future slot (search/account)
  - Active page: orange underline
- Bottom nav hidden on desktop, DesktopNav hidden on mobile
- Mobile layout completely untouched

## Page Layouts (desktop)

### Home — Dashboard
- Hero: full width, more horizontal breathing room
- Below hero: 12-col CSS grid
  - Quick actions (8 cols) + Oma tip / savings (4 cols)
  - Deals: 4-col grid instead of carousel
  - Popular products (8 cols, 2-col grid) + shopping list preview widget (4 cols)

### Vergelijk — Two columns
- Left: search + category pills + product list (2-col grid)
- Products display in wider cards with more price info visible

### Deals
- Store tabs stay horizontal
- Oma's Toppers: 3 cards in a row (wider)
- All deals: 4-col grid instead of 2-col

### Lijst — Wide list + sidebar
- Center: search + shopping list (wider, more breathing room)
- Right sidebar: Oma advice panel (instead of sticky bottom overlay)

### Mijn Oma — Centered dashboard
- Max-width ~800px centered content
- Stats + chart side by side
- Settings list wider with more spacing
