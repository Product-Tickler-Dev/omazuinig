-- Oma Zuinig — Initial Schema
-- Run this in the Supabase SQL Editor to set up all tables.

-- ============================================================
-- EXTENSIONS
-- ============================================================

create extension if not exists "uuid-ossp";
create extension if not exists "pg_trgm"; -- fuzzy text matching for product search

-- ============================================================
-- TABLES
-- ============================================================

-- All Dutch supermarket chains
create table stores (
  id text primary key,               -- 'ah', 'jumbo', 'lidl', etc.
  name text not null,                -- 'Albert Heijn'
  color text,                        -- brand color for UI (#00A0E2)
  logo_url text,
  website text,
  store_count int,                   -- approximate # of physical locations
  is_online_only boolean default false,
  is_active boolean default true,    -- can disable without deleting
  created_at timestamptz default now()
);

-- Product categories
create table categories (
  id text primary key,               -- 'zuivel', 'brood', 'groente'
  name text not null,                -- 'Zuivel'
  sort_order int default 0
);

-- Canonical products (store-agnostic)
-- One row = one real-world product, regardless of how many stores sell it
create table products (
  id uuid primary key default uuid_generate_v4(),
  name text not null,                -- canonical display name
  brand text,                        -- 'Calvé', 'De Ruijter', null for private label
  category_id text references categories(id),
  ean text,                          -- EAN-13 barcode (nullable)
  unit_size text,                    -- '1L', '500g', 'per stuk' (display string)
  weight_grams int,                  -- parsed weight for unit price calc
  volume_ml int,                     -- for liquids
  image_url text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- A product as listed by a specific store
-- One canonical product can have many store_products (one per store)
create table store_products (
  id uuid primary key default uuid_generate_v4(),
  product_id uuid not null references products(id) on delete cascade,
  store_id text not null references stores(id) on delete cascade,
  external_id text,                  -- store's own ID (webshopId, SKU, etc.)
  store_name text,                   -- the store's name for this (may differ from canonical)
  current_price numeric(8,2) not null,
  original_price numeric(8,2),       -- pre-discount price (null if no deal)
  unit_price numeric(8,2),           -- EUR per kg or per L
  is_deal boolean default false,
  deal_description text,             -- 'BONUS', '2 voor €3.00', '25% korting'
  deal_start date,
  deal_end date,
  url text,                          -- product page on store's website
  image_url text,                    -- store-specific image
  in_stock boolean default true,
  last_seen_at timestamptz default now(),
  created_at timestamptz default now(),
  updated_at timestamptz default now(),

  unique (store_id, external_id)
);

-- Price snapshots over time
-- One row per store_product per fetch — enables price history charts
create table price_history (
  id uuid primary key default uuid_generate_v4(),
  store_product_id uuid not null references store_products(id) on delete cascade,
  price numeric(8,2) not null,
  original_price numeric(8,2),
  unit_price numeric(8,2),
  is_deal boolean default false,
  recorded_at timestamptz default now()
);

-- Pipeline health tracking
-- One row per store per fetch run
create table fetch_logs (
  id uuid primary key default uuid_generate_v4(),
  store_id text not null references stores(id),
  started_at timestamptz default now(),
  completed_at timestamptz,
  products_fetched int default 0,
  products_updated int default 0,
  products_new int default 0,
  status text default 'running' check (status in ('running', 'success', 'error')),
  error_message text
);

-- ============================================================
-- INDEXES
-- ============================================================

-- === Product lookups (app reads) ===
create index idx_products_ean on products(ean) where ean is not null;
create index idx_products_category on products(category_id);
create index idx_products_name_trgm on products using gin (name gin_trgm_ops);
create index idx_products_brand on products(brand) where brand is not null;

-- === Scraper: find existing product to match against ===
-- "Does this EAN already exist?" — fastest match path
-- Already covered by idx_products_ean above
-- "Does this brand+name combo exist?" — fallback matching
create index idx_products_brand_name on products(brand, name);

-- === Store product lookups (app reads) ===
create index idx_store_products_product on store_products(product_id);
create index idx_store_products_store on store_products(store_id);
create index idx_store_products_deal on store_products(is_deal) where is_deal = true;
create index idx_store_products_last_seen on store_products(last_seen_at);
-- Composite: "all store_products for this product, cheapest first" (comparison view)
create index idx_store_products_product_price on store_products(product_id, current_price) where in_stock = true;
-- Composite: "all products in this store" (store-filtered browsing)
create index idx_store_products_store_product on store_products(store_id, product_id);

-- === Scraper: upsert by store + external_id ===
-- The UNIQUE constraint already creates an index on (store_id, external_id)
-- But we also need to find stale products (not seen in latest fetch)
create index idx_store_products_store_lastseen on store_products(store_id, last_seen_at);

-- === Price history (time-series queries) ===
create index idx_price_history_store_product on price_history(store_product_id);
create index idx_price_history_recorded on price_history(recorded_at desc);
-- Composite: "price history for one product over time" (chart queries)
create index idx_price_history_product_time on price_history(store_product_id, recorded_at desc);
-- Prevent duplicate snapshots in same fetch run
create index idx_price_history_dedup on price_history(store_product_id, recorded_at);

-- === Fetch logs ===
create index idx_fetch_logs_store on fetch_logs(store_id);
create index idx_fetch_logs_status on fetch_logs(status) where status = 'running';
create index idx_fetch_logs_store_time on fetch_logs(store_id, started_at desc);

-- ============================================================
-- MATERIALIZED VIEWS
-- ============================================================

-- For each product: cheapest store, price, and how many stores carry it
-- Powers: Vergelijk page, Lijst advice, ProductCard badges
create materialized view product_price_summary as
select
  p.id as product_id,
  p.name,
  p.brand,
  p.category_id,
  p.unit_size,
  p.weight_grams,
  p.image_url,
  count(sp.id) as store_count,
  min(sp.current_price) as min_price,
  max(sp.current_price) as max_price,
  round(avg(sp.current_price), 2) as avg_price,
  round(max(sp.current_price) - min(sp.current_price), 2) as price_spread,
  (
    select sp2.store_id from store_products sp2
    where sp2.product_id = p.id and sp2.in_stock = true
    order by sp2.current_price asc limit 1
  ) as cheapest_store_id,
  (
    select sp2.current_price from store_products sp2
    where sp2.product_id = p.id and sp2.in_stock = true
    order by sp2.current_price asc limit 1
  ) as cheapest_price,
  (
    select sp2.unit_price from store_products sp2
    where sp2.product_id = p.id and sp2.in_stock = true
    order by sp2.current_price asc limit 1
  ) as cheapest_unit_price
from products p
left join store_products sp on sp.product_id = p.id and sp.in_stock = true
group by p.id
with data;

create unique index idx_pps_product on product_price_summary(product_id);

-- Active deals across all stores, filtered to current date
-- Powers: Deals page, Home page deals section
create materialized view active_deals as
select
  sp.id as store_product_id,
  sp.product_id,
  sp.store_id,
  s.name as store_name,
  s.color as store_color,
  p.name as product_name,
  p.brand,
  p.category_id,
  p.unit_size,
  sp.current_price,
  sp.original_price,
  sp.unit_price,
  sp.deal_description,
  sp.deal_end,
  sp.image_url,
  case
    when sp.original_price > 0
    then round((1 - sp.current_price / sp.original_price) * 100, 0)
    else 0
  end as discount_pct
from store_products sp
join products p on p.id = sp.product_id
join stores s on s.id = sp.store_id
where sp.is_deal = true
  and sp.in_stock = true
  and (sp.deal_end is null or sp.deal_end >= current_date)
order by discount_pct desc
with data;

create index idx_active_deals_store on active_deals(store_id);
create index idx_active_deals_discount on active_deals(discount_pct desc);

-- ============================================================
-- FUNCTIONS
-- ============================================================

-- Refresh all materialized views
-- Call this after each store fetch completes: select refresh_views();
-- CONCURRENTLY allows reads during refresh (requires unique index on each MV)
create or replace function refresh_views()
returns void as $$
begin
  refresh materialized view concurrently product_price_summary;
  -- active_deals has no unique column, so refresh non-concurrently
  refresh materialized view active_deals;
end;
$$ language plpgsql;

-- ============================================================
-- SCRAPER HELPER FUNCTIONS
-- ============================================================

-- Upsert a store_product and record price history in one call
-- Returns the store_product id
create or replace function upsert_store_product(
  p_product_id uuid,
  p_store_id text,
  p_external_id text,
  p_store_name text,
  p_current_price numeric,
  p_original_price numeric,
  p_unit_price numeric,
  p_is_deal boolean,
  p_deal_description text,
  p_deal_start date,
  p_deal_end date,
  p_url text,
  p_image_url text
)
returns uuid as $$
declare
  v_sp_id uuid;
  v_old_price numeric;
begin
  -- Check if store_product exists
  select id, current_price into v_sp_id, v_old_price
  from store_products
  where store_id = p_store_id and external_id = p_external_id;

  if v_sp_id is null then
    -- Insert new
    insert into store_products (
      product_id, store_id, external_id, store_name,
      current_price, original_price, unit_price,
      is_deal, deal_description, deal_start, deal_end,
      url, image_url, last_seen_at
    ) values (
      p_product_id, p_store_id, p_external_id, p_store_name,
      p_current_price, p_original_price, p_unit_price,
      p_is_deal, p_deal_description, p_deal_start, p_deal_end,
      p_url, p_image_url, now()
    ) returning id into v_sp_id;

    -- First sighting — always record history
    insert into price_history (store_product_id, price, original_price, unit_price, is_deal)
    values (v_sp_id, p_current_price, p_original_price, p_unit_price, p_is_deal);
  else
    -- Update existing
    update store_products set
      store_name = p_store_name,
      current_price = p_current_price,
      original_price = p_original_price,
      unit_price = p_unit_price,
      is_deal = p_is_deal,
      deal_description = p_deal_description,
      deal_start = p_deal_start,
      deal_end = p_deal_end,
      url = p_url,
      image_url = coalesce(p_image_url, image_url),
      in_stock = true,
      last_seen_at = now()
    where id = v_sp_id;

    -- Only record history if price changed
    if v_old_price is distinct from p_current_price then
      insert into price_history (store_product_id, price, original_price, unit_price, is_deal)
      values (v_sp_id, p_current_price, p_original_price, p_unit_price, p_is_deal);
    end if;
  end if;

  return v_sp_id;
end;
$$ language plpgsql;

-- Mark products not seen in latest fetch as out of stock
create or replace function mark_stale_products(
  p_store_id text,
  p_fetch_started_at timestamptz
)
returns int as $$
declare
  v_count int;
begin
  update store_products
  set in_stock = false
  where store_id = p_store_id
    and last_seen_at < p_fetch_started_at
    and in_stock = true;

  get diagnostics v_count = row_count;
  return v_count;
end;
$$ language plpgsql;

-- Auto-update updated_at timestamp
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger trg_products_updated
  before update on products
  for each row execute function update_updated_at();

create trigger trg_store_products_updated
  before update on store_products
  for each row execute function update_updated_at();

-- ============================================================
-- SEED DATA: STORES
-- ============================================================

insert into stores (id, name, color, store_count, is_online_only) values
  ('ah',         'Albert Heijn',    '#00A0E2', 1048, false),
  ('jumbo',      'Jumbo',           '#FFC600', 705,  false),
  ('lidl',       'Lidl',            '#0050AA', 440,  false),
  ('aldi',       'Aldi',            '#00205C', 500,  false),
  ('plus',       'PLUS',            '#E30613', 550,  false),
  ('dirk',       'Dirk',            '#ED7100', 131,  false),
  ('spar',       'Spar',            '#00843D', 453,  false),
  ('dekamarkt',  'DekaMarkt',       '#E30613', 102,  false),
  ('vomar',      'Vomar',           '#003DA5', 94,   false),
  ('poiesz',     'Poiesz',          '#0066B3', 80,   false),
  ('dagwinkel',  'Dagwinkel',       '#FF6600', 74,   false),
  ('hoogvliet',  'Hoogvliet',       '#E30613', 71,   false),
  ('boni',       'Boni',            '#009640', 43,   false),
  ('nettorama',  'Nettorama',       '#0072BC', 32,   false),
  ('ekoplaza',   'EkoPlaza',        '#7AB648', 143,  false),
  ('mcd',        'MCD',             '#003399', 29,   false),
  ('makro',      'Makro',           '#003DA5', 17,   false),
  ('boons',      'Boon''s Markt',   '#E30613', 15,   false),
  ('marqt',      'Marqt',           '#1A1A1A', 10,   false),
  ('picnic',     'Picnic',          '#E7243A', null, true),
  ('crisp',      'Crisp',           '#FF5A00', null, true);

-- ============================================================
-- SEED DATA: CATEGORIES
-- ============================================================

insert into categories (id, name, sort_order) values
  ('zuivel',    'Zuivel',           1),
  ('brood',     'Brood & Bakkerij', 2),
  ('groente',   'Groente & Fruit',  3),
  ('vlees',     'Vlees',            4),
  ('vis',       'Vis',              5),
  ('dranken',   'Dranken',          6),
  ('pasta',     'Pasta & Rijst',    7),
  ('conserven', 'Conserven & Sauzen', 8),
  ('snacks',    'Snacks & Snoep',   9),
  ('diepvries', 'Diepvries',        10),
  ('huishouden','Huishouden',        11),
  ('verzorging','Verzorging',        12),
  ('drogist',   'Drogist',           13),
  ('overig',    'Overig',            99);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================

-- Enable RLS on all tables (Supabase requirement)
alter table stores enable row level security;
alter table categories enable row level security;
alter table products enable row level security;
alter table store_products enable row level security;
alter table price_history enable row level security;
alter table fetch_logs enable row level security;

-- Public read access for product data (no auth required)
create policy "Public read stores" on stores for select using (true);
create policy "Public read categories" on categories for select using (true);
create policy "Public read products" on products for select using (true);
create policy "Public read store_products" on store_products for select using (true);
create policy "Public read price_history" on price_history for select using (true);

-- Fetch logs: only service role can read/write (pipeline only)
create policy "Service role fetch_logs" on fetch_logs
  for all using (auth.role() = 'service_role');
