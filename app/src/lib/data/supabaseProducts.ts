/**
 * Data layer that reads from Supabase when configured, falls back to mock data.
 *
 * When VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY are set, this module
 * fetches real product data from the database. Otherwise, it re-exports
 * the existing mock data — zero changes needed in components.
 */
import { supabase, isSupabaseConfigured } from '$lib/supabase';
import { PRODUCTS as MOCK_PRODUCTS } from './products';
import { DEALS as MOCK_DEALS } from './deals';
import { STORES as MOCK_STORES } from './stores';
import type { Product, Deal, Store } from './types';

export async function fetchProducts(): Promise<Product[]> {
  if (!isSupabaseConfigured) return MOCK_PRODUCTS;

  const { data, error } = await supabase!
    .from('product_price_summary')
    .select('*')
    .order('name');

  if (error || !data) return MOCK_PRODUCTS;

  // Transform DB rows to match our Product type
  return data.map((row: any) => ({
    id: row.product_id,
    name: row.name,
    brand: row.brand || 'Huismerk',
    category: row.category_id || 'overig',
    size: row.unit_size || '',
    prices: {}, // Will need a separate query for per-store prices
    image: row.image_url,
  }));
}

export async function fetchDeals(): Promise<Deal[]> {
  if (!isSupabaseConfigured) return MOCK_DEALS;

  const { data, error } = await supabase!
    .from('active_deals')
    .select('*')
    .order('discount_pct', { ascending: false });

  if (error || !data) return MOCK_DEALS;

  return data.map((row: any) => ({
    id: row.store_product_id,
    productId: row.product_id,
    store: row.store_id,
    oldPrice: row.original_price,
    newPrice: row.current_price,
    discount: row.discount_pct,
    description: row.deal_description,
  }));
}

export async function fetchStores(): Promise<Store[]> {
  if (!isSupabaseConfigured) return MOCK_STORES;

  const { data, error } = await supabase!
    .from('stores')
    .select('*')
    .eq('is_active', true)
    .order('name');

  if (error || !data) return MOCK_STORES;

  return data.map((row: any) => ({
    id: row.id,
    name: row.name,
    color: row.color || '#666',
  }));
}

export async function fetchProductPrices(productId: string): Promise<Record<string, number>> {
  if (!isSupabaseConfigured) return {};

  const { data, error } = await supabase!
    .from('store_products')
    .select('store_id, current_price')
    .eq('product_id', productId)
    .eq('in_stock', true)
    .order('current_price');

  if (error || !data) return {};

  const prices: Record<string, number> = {};
  for (const row of data) {
    prices[row.store_id] = row.current_price;
  }
  return prices;
}
