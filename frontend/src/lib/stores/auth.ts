import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import api from '$lib/api';

export interface User {
	id: number;
	username: string;
}

export interface LoginData {
	username: string;
	password: string;
}

export interface RegisterData {
	username: string;
	password: string;
}

export interface TokenResponse {
	access_token: string;
	token_type: string;
}

interface AuthState {
	user: User | null;
	isAuthenticated: boolean;
	loading: boolean;
}

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>({
		user: null,
		isAuthenticated: false,
		loading: true
	});

	return {
		subscribe,
		async login(data: LoginData): Promise<void> {
			try {
				const response = await api.post<TokenResponse>('/auth/login', data);
				if (browser) {
					localStorage.setItem('token', response.data.access_token);
				}
				update((state) => ({
					...state,
					isAuthenticated: true,
					loading: false
				}));
			} catch (error) {
				console.error('Login failed:', error);
				throw error;
			}
		},
		async register(data: RegisterData): Promise<void> {
			try {
				await api.post('/auth/register', data);
			} catch (error) {
				console.error('Registration failed:', error);
				throw error;
			}
		},
		async logout(): Promise<void> {
			if (browser) {
				localStorage.removeItem('token');
			}
			set({
				user: null,
				isAuthenticated: false,
				loading: false
			});
		},
		checkAuth() {
			if (browser) {
				const token = localStorage.getItem('token');
				update((state) => ({
					...state,
					isAuthenticated: !!token,
					loading: false
				}));
			} else {
				update((state) => ({ ...state, loading: false }));
			}
		}
	};
}

export const authStore = createAuthStore();
