import { writable } from 'svelte/store';

interface ToastMessage {
  id: number;
  text: string;
  type: 'success' | 'info' | 'celebrate';
  amount?: number;
}

function createToastStore() {
  const { subscribe, update } = writable<ToastMessage[]>([]);
  let nextId = 0;

  return {
    subscribe,
    show: (text: string, type: 'success' | 'info' = 'success') => {
      const id = nextId++;
      update(toasts => [...toasts, { id, text, type }]);
      setTimeout(() => {
        update(toasts => toasts.filter(t => t.id !== id));
      }, 2500);
    },
    celebrate: (text: string, amount: number) => {
      const id = nextId++;
      update(toasts => [...toasts, { id, text, type: 'celebrate' as const, amount }]);
      setTimeout(() => {
        update(toasts => toasts.filter(t => t.id !== id));
      }, 2000);
    }
  };
}

export const toasts = createToastStore();
