import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { ShoppingListItem } from '$lib/data/types';

const defaultItems: ShoppingListItem[] = [
  { productId: 1, checked: false },
  { productId: 2, checked: false },
  { productId: 4, checked: false },
  { productId: 7, checked: false },
  { productId: 6, checked: true }
];

function createShoppingList() {
  const stored = browser ? localStorage.getItem('oma-shopping-list') : null;
  const initial: ShoppingListItem[] = stored ? JSON.parse(stored) : defaultItems;
  const { subscribe, set, update } = writable<ShoppingListItem[]>(initial);

  if (browser) {
    subscribe(value => {
      localStorage.setItem('oma-shopping-list', JSON.stringify(value));
    });
  }

  return {
    subscribe,
    add: (productId: number) => update(items => {
      if (items.find(i => i.productId === productId)) return items;
      return [...items, { productId, checked: false }];
    }),
    toggle: (productId: number) => update(items =>
      items.map(i => i.productId === productId ? { ...i, checked: !i.checked } : i)
    ),
    remove: (productId: number) => update(items =>
      items.filter(i => i.productId !== productId)
    ),
    clear: () => set([])
  };
}

export const shoppingList = createShoppingList();
