import type { Product, ShoppingListItem } from '$lib/data/types';
import { STORES } from '$lib/data/stores';

export function formatPrice(n: number): string {
  return '\u20AC' + n.toFixed(2).replace('.', ',');
}

export function getCheapestStore(product: Product): [string, number] {
  return Object.entries(product.prices).sort((a, b) => a[1] - b[1])[0];
}

export function getMostExpensiveStore(product: Product): [string, number] {
  return Object.entries(product.prices).sort((a, b) => b[1] - a[1])[0];
}

export function calculateBestSingleStore(
  items: ShoppingListItem[],
  getProduct: (id: number) => Product | undefined
): [string, number][] {
  const unchecked = items.filter(i => !i.checked);
  const storeTotals: Record<string, number> = {};
  STORES.forEach(s => { storeTotals[s.id] = 0; });
  unchecked.forEach(item => {
    const product = getProduct(item.productId);
    if (!product) return;
    STORES.forEach(s => { storeTotals[s.id] += product.prices[s.id] ?? 0; });
  });
  return Object.entries(storeTotals).sort((a, b) => a[1] - b[1]);
}

export function calculateSplitSavings(
  items: ShoppingListItem[],
  getProduct: (id: number) => Product | undefined
) {
  const unchecked = items.filter(i => !i.checked);
  let splitTotal = 0;
  const storesUsed = new Set<string>();
  unchecked.forEach(item => {
    const product = getProduct(item.productId);
    if (!product) return;
    const [cheapestId, cheapestPrice] = getCheapestStore(product);
    splitTotal += cheapestPrice;
    storesUsed.add(cheapestId);
  });
  const bestStoreResult = calculateBestSingleStore(items, getProduct);
  const [singleStore, singleTotal] = bestStoreResult[0] ?? ['', 0];
  return {
    splitTotal,
    storesUsed: [...storesUsed],
    singleStore,
    singleTotal,
    savings: singleTotal - splitTotal
  };
}
