<script lang="ts">
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';

	let auth = $state({ isAuthenticated: false, loading: true });

	authStore.subscribe((value) => {
		auth = value;
	});

	$effect(() => {
		if (!auth.loading) {
			if (auth.isAuthenticated) {
				goto('/home');
			} else {
				goto('/login');
			}
		}
	});
</script>

{#if auth.loading}
	<div class="min-h-screen flex items-center justify-center">
		<p class="text-gray-500">Loading...</p>
	</div>
{/if}
