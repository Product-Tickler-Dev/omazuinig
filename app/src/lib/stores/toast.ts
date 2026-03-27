import { writable } from 'svelte/store';

interface ToastMessage {
  id: number;
  text: string;
  type: 'success' | 'info';
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
    }
  };
}

export const toasts = createToastStore();
