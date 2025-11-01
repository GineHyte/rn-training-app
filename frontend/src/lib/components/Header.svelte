<script lang="ts">
	import { title } from '$lib/stores/title';
	import { authStore } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import Dropdown from './Dropdown.svelte';

	let isDropdownOpen = $state(false);

	let showBackButton = $derived($page.url.pathname !== '/home' && $page.url.pathname !== '/');

	function goBack() {
		window.history.back();
	}

	function toggleDropdown() {
		isDropdownOpen = !isDropdownOpen;
	}

	function closeDropdown() {
		isDropdownOpen = false;
	}

	function handleSettings() {
		closeDropdown();
		// TODO: Navigate to settings page
		console.log('Settings clicked');
	}

	function handleLogout() {
		closeDropdown();
		authStore.logout();
		goto('/login');
	}
</script>

<header class="bg-blue-600 text-white shadow-lg">
	<div class="container mx-auto px-4 py-4">
		<div class="flex items-center justify-between">
			<div class="flex items-center space-x-4">
				{#if showBackButton}
					<button
						onclick={goBack}
						class="w-10 h-10 rounded-full hover:bg-blue-500 flex items-center justify-center transition"
						aria-label="Go back"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="2"
							stroke="currentColor"
							class="w-6 h-6"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M15.75 19.5L8.25 12l7.5-7.5"
							/>
						</svg>
					</button>
				{/if}
				<h1 class="text-2xl font-bold">
					{$title}
				</h1>
			</div>

			{#if $authStore.isAuthenticated}
				<nav class="flex items-center space-x-4">
					<div class="relative">
						<button
							onclick={toggleDropdown}
							class="w-10 h-10 rounded-full bg-blue-500 hover:bg-blue-400 flex items-center justify-center transition"
							aria-label="Profile menu"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke-width="2"
								stroke="currentColor"
								class="w-6 h-6"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
								/>
							</svg>
						</button>

						<Dropdown isOpen={isDropdownOpen} onClose={closeDropdown}>
							<button
								onclick={handleSettings}
								class="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 flex items-center gap-3"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="2"
									stroke="currentColor"
									class="w-5 h-5"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"
									/>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
									/>
								</svg>
								Settings
							</button>

							<button
								onclick={handleLogout}
								class="w-full text-left px-4 py-2 text-red-600 hover:bg-gray-100 flex items-center gap-3"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="2"
									stroke="currentColor"
									class="w-5 h-5"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"
									/>
								</svg>
								Logout
							</button>
						</Dropdown>
					</div>
				</nav>
			{:else}
				<nav class="flex items-center space-x-4">
					<a href="/login" class="hover:text-blue-200 transition">Login</a>
					<a href="/register" class="hover:text-blue-200 transition">Register</a>
				</nav>
			{/if}
		</div>
	</div>
</header>

