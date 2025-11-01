<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth';
	import Header from '$lib/components/Header.svelte';
	import { page } from '$app/stores';

	let { children } = $props();

	onMount(() => {
		authStore.checkAuth();
	});

	let showHeader = $derived($page.url.pathname !== '/login' && $page.url.pathname !== '/register');
</script>

<svelte:head>
	<title>Training App</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	{#if showHeader}
		<Header />
	{/if}
	<main>
		{@render children()}
	</main>
</div>
