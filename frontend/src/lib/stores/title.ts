import { writable } from 'svelte/store';

function createTitleStore() {
	const { subscribe, set } = writable<string>('Home');

	return {
		subscribe,
		setTitle: (title: string) => set(title),
		reset: () => set('Home')
	};
}

export const title = createTitleStore();
