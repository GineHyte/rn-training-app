<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	interface Props {
		isOpen?: boolean;
		onClose?: () => void;
		children?: any;
	}

	let { isOpen = false, onClose = () => {}, children }: Props = $props();

	let dropdownRef = $state<HTMLDivElement>();

	function handleClickOutside(event: MouseEvent) {
		if (dropdownRef && !dropdownRef.contains(event.target as Node)) {
			onClose();
		}
	}

	onMount(() => {
		document.addEventListener('mousedown', handleClickOutside);
	});

	onDestroy(() => {
		document.removeEventListener('mousedown', handleClickOutside);
	});
</script>

{#if isOpen}
	<div
		bind:this={dropdownRef}
		class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 py-2 z-50"
	>
		{@render children()}
	</div>
{/if}
