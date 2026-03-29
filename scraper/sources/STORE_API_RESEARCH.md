# Store API Research

## Working APIs

### Albert Heijn — Mobile API
- Auth: `POST https://api.ah.nl/mobile-auth/v1/auth/token/anonymous` (clientId: "appie")
- Search: `GET https://api.ah.nl/mobile-services/product/search/v2`
- Taxonomy: `GET https://api.ah.nl/mobile-services/v1/product-shelves/categories`
- Status: **Working** — 10K+ products

### Dirk — GraphQL
- Endpoint: `https://web-gateway.dirk.nl/graphql`
- Auth: None required
- Products: `searchProducts(search, limit)` → `products { product { productId headerText brand packaging image department } }`
- Prices: `productAssortment(productId, storeId)` → `{ normalPrice offerPrice }`
- Default storeId: 1
- Status: **Working** — 2.3K products with prices

### DekaMarkt — GraphQL (same parent as Dirk)
- Endpoint: `https://web-deka-gateway.dekamarkt.nl/graphql`
- Auth: None for products, needed for prices
- Same schema as Dirk
- Status: **Working for catalog** — 4.6K products, no prices (needs store auth)

### Jumbo — GraphQL
- Endpoint: `https://www.jumbo.com/api/graphql`
- Auth: Headers `apollographql-client-name: ECOMMERCE_HEADER`, `apollographql-client-version: V3`
- Input: `ProductSearchInput` with `searchTerms`, `searchType`, `limit`, `offSet` (camelCase!)
- Status: **API cracked but rate limited** — works with correct headers, needs retry

### Lidl — Search API (DISCOVERED 2026-03-29!)
- Endpoint: `GET https://www.lidl.nl/q/api/search`
- Auth: None required
- Params: `assortment=NL`, `locale=nl_NL`, `version=v2.0.0`, `q=<query>`, `category=Eten & drinken`, `store=1`
- Response: Full product JSON with prices, images, brands, packaging
- Price at: `items[].gridbox.data.price.price` (EUR)
- Old price: `items[].gridbox.data.price.oldPrice`
- Packaging: `items[].gridbox.data.price.packaging.text`
- Brand: `items[].gridbox.data.brand.name`
- Image: `items[].gridbox.data.image`
- Title: `items[].gridbox.data.keyfacts.fullTitle`
- Category: `items[].gridbox.data.keyfacts.wonCategoryPrimary`
- Status: **NEWLY DISCOVERED — needs adapter built**

### Plus — OutSystems API (DISCOVERED 2026-03-29!)
- Endpoint: `POST https://www.plus.nl/screenservices/ECP_Composition_CW/ProductLists/PLP_Content/DataActionGetProductListAndCategoryInfo`
- Auth: Session-based. First GET any page to get Incapsula cookies, then POST with empty X-CSRFToken
- Required headers: `Content-Type: application/json`, `X-CSRFToken: ""`, `OutSystems-locale: nl-NL`
- Request body: OutSystems DataAction format with `SearchTerm`, `PageNumber`, `CategoryURL`
- Response: Full product JSON with SKU, Brand, Name, Price (OriginalPrice/NewPrice), ImageURL, Categories, Packaging, EAN
- **17,457 total products** across 1,455 pages (12 per page)
- Deals: `NewPrice > 0` means deal, also has `PromotionLabel`, `PromotionStartDate/EndDate`
- Categories: Nested list with full hierarchy (e.g. "Vlees, kip, vis, vega" > "Kip, kalkoen" > "Kipfilet")
- Status: **NEWLY DISCOVERED — needs adapter built**

## Blocked / Need Headless Browser

### Vomar
- Nuxt-based but no GraphQL or accessible API found
- Would need Playwright

### Hoogvliet
- Returns 403 for all API attempts
- Would need Playwright

## Not Yet Explored
- Spar, Poiesz, Boni, Nettorama, EkoPlaza, others
