export const CATEGORY_COLORS: Record<string, string> = {
  zuivel: '#4FC3F7',
  brood: '#FFB74D',
  groente: '#81C784',
  dranken: '#BA68C8'
};

export const CATEGORY_FALLBACK = '#BDBDBD';

export function getCategoryColor(category: string): string {
  return CATEGORY_COLORS[category] ?? CATEGORY_FALLBACK;
}
