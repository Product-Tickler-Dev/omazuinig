import type { Store } from './types';

export const STORES: Store[] = [
  { id: 'ah', name: 'Albert Heijn', short: 'AH', color: '#00A0E2' },
  { id: 'jumbo', name: 'Jumbo', short: 'Jumbo', color: '#FFD700' },
  { id: 'lidl', name: 'Lidl', short: 'Lidl', color: '#0050AA' },
  { id: 'aldi', name: 'Aldi', short: 'Aldi', color: '#00599C' },
  { id: 'plus', name: 'Plus', short: 'Plus', color: '#E3000B' },
  { id: 'dirk', name: 'Dirk', short: 'Dirk', color: '#E31937' }
];

export function getStore(id: string): Store | undefined {
  return STORES.find(s => s.id === id);
}
