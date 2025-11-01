<script lang="ts">
	import type { PlanExercise } from '$lib/services/planExerciseService';
	import type { TrainingExercise } from '$lib/services/trainingService';

	interface Props {
		planExercise: PlanExercise;
		activeTraining: boolean;
		loggedSets: TrainingExercise[];
		onShowDetails: (exercise: any) => void;
		onLogSet: (planExerciseId: number) => void;
		onRemove: (planExerciseId: number) => void;
		onDeleteSet: (setId: number) => void;
	}

	let { 
		planExercise, 
		activeTraining, 
		loggedSets, 
		onShowDetails, 
		onLogSet, 
		onRemove, 
		onDeleteSet 
	}: Props = $props();
</script>

<div class="bg-white shadow rounded-lg p-6">
	<div class="flex justify-between items-start mb-4">
		<div class="flex-1">
			<button
				onclick={() => onShowDetails(planExercise.exercise)}
				class="text-left hover:text-blue-600 transition"
			>
				<h4 class="text-lg font-medium text-gray-900 hover:underline">
					{planExercise.exercise?.name || 'Exercise'}
				</h4>
			</button>
			<p class="text-sm text-gray-500">Intensity: {planExercise.intensity}/3</p>
		</div>
		<div class="flex gap-2">
			{#if activeTraining}
				<button
					onclick={() => onLogSet(planExercise.id)}
					class="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
				>
					Log Set
				</button>
			{:else}
				<button
					onclick={() => onRemove(planExercise.id)}
					class="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
				>
					Remove
				</button>
			{/if}
		</div>
	</div>

	{#if activeTraining && loggedSets.length > 0}
		<div class="border-t border-gray-200 pt-4 mt-4">
			<h5 class="text-sm font-medium text-gray-700 mb-2">Logged Sets:</h5>
			<div class="space-y-2">
				{#each loggedSets as set, index}
					<div class="flex justify-between items-center text-sm bg-gray-50 p-2 rounded">
						<span class="font-medium">Set {index + 1}:</span>
						<span>{set.reps} reps × {set.kgs} kg</span>
						<span class="text-gray-500 text-xs">{new Date(set.timestamp).toLocaleTimeString()}</span>
						<button
							onclick={() => onDeleteSet(set.id)}
							class="ml-2 px-2 py-1 bg-red-500 text-white rounded text-xs hover:bg-red-600"
							title="Delete set"
						>
							×
						</button>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>
