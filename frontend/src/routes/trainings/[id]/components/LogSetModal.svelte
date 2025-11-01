<script lang="ts">
	import Potentiometer from '$lib/components/Potentiometer.svelte';

	interface Props {
		isOpen: boolean;
		reps: number;
		kgs: number;
		onClose: () => void;
		onLog: () => void;
	}

	let { isOpen, reps = $bindable(), kgs = $bindable(), onClose, onLog }: Props = $props();
</script>

{#if isOpen}
	<div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
		<div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
			<h4 class="text-lg font-medium mb-6 text-center">Log Set</h4>
			<div class="flex justify-around items-center gap-8">
				<Potentiometer
					bind:value={reps}
					min={1}
					max={50}
					step={1}
					label="Reps"
					color="#3b82f6"
				/>
				
				<Potentiometer
					bind:value={kgs}
					min={0}
					max={200}
					step={0.5}
					label="Weight"
					unit="kg"
					color="#10b981"
				/>
			</div>
			<div class="flex gap-4 mt-6">
				<button
					onclick={onLog}
					class="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
				>
					Log Set
				</button>
				<button
					onclick={onClose}
					class="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
				>
					Cancel
				</button>
			</div>
		</div>
	</div>
{/if}
