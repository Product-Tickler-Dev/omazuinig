import type { Product, ShoppingListItem } from '$lib/data/types';

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
  const products = unchecked.map(i => getProduct(i.productId)).filter(Boolean) as Product[];

  if (products.length === 0) return [];

  // Find all stores that appear in at least one product
  const allStores = new Set<string>();
  products.forEach(p => Object.keys(p.prices).forEach(s => allStores.add(s)));

  // Calculate total per store — only count stores that have a price for the product
  // If a store doesn't carry a product, use the cheapest available price as fallback
  const storeTotals: Record<string, number> = {};
  allStores.forEach(storeId => {
    let total = 0;
    for (const product of products) {
      if (product.prices[storeId] != null) {
        total += product.prices[storeId];
      } else {
        // Store doesn't carry this product — use cheapest available
        const cheapest = getCheapestStore(product);
        total += cheapest[1];
      }
    }
    storeTotals[storeId] = total;
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
    savings: Math.max(0, singleTotal - splitTotal)
  };
}
