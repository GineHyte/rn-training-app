<script lang="ts">
	import type { PlanTraining } from '$lib/services/planTrainingService';
	import type { Training } from '$lib/services/trainingService';

	interface Props {
		planTraining: PlanTraining | null;
		activeTraining: Training | null;
		onBack: () => void;
		onStartTraining: () => void;
		onEndTraining: () => void;
	}

	let { planTraining, activeTraining, onBack, onStartTraining, onEndTraining }: Props = $props();
</script>

<nav class="bg-white shadow-sm">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex justify-between h-16">
			<div class="flex items-center">
				<button
					onclick={onBack}
					class="text-gray-700 hover:text-gray-900 mr-4"
				>
					← Back
				</button>
				<h1 class="text-xl font-bold text-gray-900">
					{planTraining?.name || 'Training Details'}
				</h1>
			</div>
			<div class="flex items-center">
				{#if !activeTraining}
					<button
						onclick={onStartTraining}
						class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium"
					>
						🚀 Start Training
					</button>
				{:else}
					<button
						onclick={onEndTraining}
						class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium"
					>
						⏹️ End Training
					</button>
				{/if}
			</div>
		</div>
	</div>
</nav>
