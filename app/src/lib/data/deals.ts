import type { Deal } from './types';

export const DEALS: Deal[] = [
  { productId: 5, store: 'ah', oldPrice: 5.99, newPrice: 3.99, discount: 33 },
  { productId: 6, store: 'jumbo', oldPrice: 6.49, newPrice: 4.49, discount: 31 },
  { productId: 7, store: 'lidl', oldPrice: 3.79, newPrice: 1.99, discount: 47 },
  { productId: 2, store: 'aldi', oldPrice: 3.89, newPrice: 2.49, discount: 36 },
  { productId: 9, store: 'dirk', oldPrice: 2.59, newPrice: 1.49, discount: 42 },
  { productId: 4, store: 'plus', oldPrice: 2.89, newPrice: 1.79, discount: 38 },
  { productId: 3, store: 'ah', oldPrice: 1.89, newPrice: 0.99, discount: 48 },
  { productId: 8, store: 'jumbo', oldPrice: 0.99, newPrice: 0.59, discount: 40 }
];
