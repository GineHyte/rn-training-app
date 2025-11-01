<script lang="ts">
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';

	let username = $state('');
	let password = $state('');
	let loading = $state(false);
	let error = $state('');

	async function handleLogin() {
		if (!username || !password) {
			error = 'Please fill in all fields';
			return;
		}

		loading = true;
		error = '';
		
		try {
			await authStore.login({ username, password });
			goto('/home');
		} catch (err: any) {
			error = err.response?.data?.detail || 'Login failed';
		} finally {
			loading = false;
		}
	}

	function goToRegister() {
		goto('/register');
	}
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
		<div>
			<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
				Training App
			</h2>
			<p class="mt-2 text-center text-sm text-gray-600">
				Sign in to your account
			</p>
		</div>
		<form class="mt-8 space-y-6" onsubmit={(e) => { e.preventDefault(); handleLogin(); }}>
			{#if error}
				<div class="rounded-md bg-red-50 p-4">
					<p class="text-sm text-red-800">{error}</p>
				</div>
			{/if}
			<div class="rounded-md shadow-sm -space-y-px">
				<div>
					<label for="username" class="sr-only">Username</label>
					<input
						id="username"
						name="username"
						type="text"
						required
						bind:value={username}
						class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
						placeholder="Username"
					/>
				</div>
				<div>
					<label for="password" class="sr-only">Password</label>
					<input
						id="password"
						name="password"
						type="password"
						required
						bind:value={password}
						class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
						placeholder="Password"
					/>
				</div>
			</div>

			<div>
				<button
					type="submit"
					disabled={loading}
					class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
				>
					{loading ? 'Loading...' : 'Sign in'}
				</button>
			</div>

			<div class="text-center">
				<button
					type="button"
					onclick={goToRegister}
					class="font-medium text-indigo-600 hover:text-indigo-500"
				>
					Don't have an account? Register
				</button>
			</div>
		</form>
	</div>
</div>
