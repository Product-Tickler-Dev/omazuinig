import type { Product } from './types';

export const PRODUCTS: Product[] = [
  { id: 1, name: 'Halfvolle melk', brand: 'Huismerk', size: '1L', category: 'zuivel', image: '\u{1F95B}', prices: { ah: 1.29, jumbo: 1.25, lidl: 0.99, aldi: 0.95, plus: 1.19, dirk: 1.09 } },
  { id: 2, name: 'Gouda kaas jong belegen', brand: 'Huismerk', size: '500g', category: 'zuivel', image: '\u{1F9C0}', prices: { ah: 4.99, jumbo: 4.79, lidl: 3.99, aldi: 3.89, plus: 4.49, dirk: 4.29 } },
  { id: 3, name: 'Volkoren brood', brand: 'Huismerk', size: '800g', category: 'brood', image: '\u{1F35E}', prices: { ah: 1.89, jumbo: 1.79, lidl: 1.49, aldi: 1.39, plus: 1.69, dirk: 1.59 } },
  { id: 4, name: 'Scharreleieren', brand: 'Huismerk', size: '10 stuks', category: 'zuivel', image: '\u{1F95A}', prices: { ah: 3.29, jumbo: 2.99, lidl: 2.69, aldi: 2.59, plus: 2.89, dirk: 2.79 } },
  { id: 5, name: 'Heineken Pilsener', brand: 'Heineken', size: '6-pack', category: 'dranken', image: '\u{1F37A}', prices: { ah: 5.99, jumbo: 5.49, lidl: 5.29, aldi: 5.19, plus: 5.69, dirk: 5.39 } },
  { id: 6, name: 'Aroma Rood koffie', brand: 'Douwe Egberts', size: '500g', category: 'dranken', image: '\u2615', prices: { ah: 6.99, jumbo: 6.49, lidl: 5.99, aldi: 5.79, plus: 6.29, dirk: 6.19 } },
  { id: 7, name: 'Pindakaas', brand: 'Calv\u00e9', size: '650g', category: 'brood', image: '\u{1F95C}', prices: { ah: 4.49, jumbo: 3.99, lidl: 3.79, aldi: 3.69, plus: 4.19, dirk: 3.89 } },
  { id: 8, name: 'Paprika rood', brand: '', size: 'per stuk', category: 'groente', image: '\u{1FAD1}', prices: { ah: 1.19, jumbo: 0.99, lidl: 0.89, aldi: 0.85, plus: 0.99, dirk: 0.95 } },
  { id: 9, name: 'Melkchocolade hagelslag', brand: 'De Ruijter', size: '400g', category: 'brood', image: '\u{1F36B}', prices: { ah: 2.99, jumbo: 2.79, lidl: 2.49, aldi: 2.39, plus: 2.69, dirk: 2.59 } },
  { id: 10, name: 'Karnemelk', brand: 'Huismerk', size: '1L', category: 'zuivel', image: '\u{1F95B}', prices: { ah: 1.09, jumbo: 0.99, lidl: 0.89, aldi: 0.85, plus: 0.99, dirk: 0.95 } }
];

export function getProduct(id: number): Product | undefined {
  return PRODUCTS.find(p => p.id === id);
}
