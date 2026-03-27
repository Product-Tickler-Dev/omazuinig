export interface Store {
  id: string;
  name: string;
  short: string;
  color: string;
}

export interface Product {
  id: number;
  name: string;
  brand: string;
  size: string;
  category: string;
  image: string;
  prices: Record<string, number>;
}

export interface Deal {
  productId: number;
  store: string;
  oldPrice: number;
  newPrice: number;
  discount: number;
}

export interface ShoppingListItem {
  productId: number;
  checked: boolean;
}
