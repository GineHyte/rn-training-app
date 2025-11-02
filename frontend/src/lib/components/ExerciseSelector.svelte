<script lang="ts">
	import { exerciseService } from '$lib/services/exerciseService';
    import type { Exercise as ExerciseBase } from '$lib/services/exerciseService';
	
	interface Exercise extends ExerciseBase {
		id: number;
		name: string;
		description?: string;
		image?: string;
		video?: string;
		public: boolean;
		userId: number;
	}

	interface Props {
		isOpen: boolean;
		onClose: () => void;
		onSelect: (exercise: Exercise) => Promise<void>;
		selectedExerciseId?: number;
	}

	let { isOpen, onClose, onSelect, selectedExerciseId }: Props = $props();

	let exercises = $state<Exercise[]>([]);
	let filteredExercises = $state<Exercise[]>([]);
	let searchQuery = $state('');
	let filterType = $state<'all' | 'my' | 'public'>('all');
	let loading = $state(false);
	let error = $state('');
	let selectedId = $state(selectedExerciseId || 0);

	// Load exercises when modal opens
	$effect(() => {
		if (isOpen) {
			loadExercises();
			selectedId = selectedExerciseId || 0;
		}
	});

	// Filter exercises based on search and filter type
	$effect(() => {
		let result = exercises;

		// Apply search filter
		if (searchQuery.trim()) {
			const query = searchQuery.toLowerCase();
			result = result.filter(ex => 
				ex.name.toLowerCase().includes(query) || 
				ex.description?.toLowerCase().includes(query)
			);
		}

		// Apply type filter
		if (filterType === 'my') {
			result = result.filter(ex => !ex.public);
		} else if (filterType === 'public') {
			result = result.filter(ex => ex.public);
		}

		filteredExercises = result;
	});

	async function loadExercises() {
		loading = true;
		error = '';
		try {
			const data = await exerciseService.getAll();
			exercises = data;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load exercises';
		} finally {
			loading = false;
		}
	}

	function handleSelect(exercise: Exercise) {
		onSelect(exercise);
		onClose();
	}

	function handleClose() {
		searchQuery = '';
		filterType = 'all';
		selectedId = 0;
		onClose();
	}
</script>

{#if isOpen}
	<div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50" onclick={handleClose}>
		<div class="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[85vh] flex flex-col" onclick={(e) => e.stopPropagation()}>
			<!-- Header -->
			<div class="flex justify-between items-center p-6 border-b border-gray-200">
				<h3 class="text-2xl font-bold text-gray-900">Select Exercise</h3>
				<button
					onclick={handleClose}
					class="text-gray-400 hover:text-gray-600 text-2xl leading-none"
				>
					×
				</button>
			</div>

			<!-- Search and Filters -->
			<div class="p-6 border-b border-gray-200 space-y-4">
				<div>
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search exercises..."
						class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
					/>
				</div>
				<div class="flex gap-2">
					<button
						onclick={() => filterType = 'all'}
						class={`px-4 py-2 rounded-lg font-medium transition ${
							filterType === 'all'
								? 'bg-indigo-600 text-white'
								: 'bg-gray-100 text-gray-700 hover:bg-gray-200'
						}`}
					>
						All ({exercises.length})
					</button>
					<button
						onclick={() => filterType = 'my'}
						class={`px-4 py-2 rounded-lg font-medium transition ${
							filterType === 'my'
								? 'bg-indigo-600 text-white'
								: 'bg-gray-100 text-gray-700 hover:bg-gray-200'
						}`}
					>
						My Exercises ({exercises.filter(ex => !ex.public).length})
					</button>
					<button
						onclick={() => filterType = 'public'}
						class={`px-4 py-2 rounded-lg font-medium transition ${
							filterType === 'public'
								? 'bg-indigo-600 text-white'
								: 'bg-gray-100 text-gray-700 hover:bg-gray-200'
						}`}
					>
						Public ({exercises.filter(ex => ex.public).length})
					</button>
				</div>
			</div>

			<!-- Exercise List -->
			<div class="flex-1 overflow-y-auto p-6">
				{#if loading}
					<div class="text-center py-12">
						<p class="text-gray-500">Loading exercises...</p>
					</div>
				{:else if error}
					<div class="rounded-md bg-red-50 p-4">
						<p class="text-sm text-red-800">{error}</p>
					</div>
				{:else if filteredExercises.length === 0}
					<div class="text-center py-12">
						<p class="text-gray-500">
							{searchQuery ? 'No exercises found matching your search.' : 'No exercises available.'}
						</p>
					</div>
				{:else}
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						{#each filteredExercises as exercise}
							<button
								onclick={() => handleSelect(exercise)}
								class={`text-left p-4 rounded-lg border-2 transition hover:shadow-md ${
									selectedId === exercise.id
										? 'border-indigo-600 bg-indigo-50'
										: 'border-gray-200 hover:border-indigo-300'
								}`}
							>
								<div class="flex items-start gap-4">
									{#if exercise.image}
										<img
											src={exercise.image}
											alt={exercise.name}
											class="w-20 h-20 object-cover rounded-lg flex-shrink-0"
										/>
									{:else}
										<div class="w-20 h-20 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
											<span class="text-gray-400 text-2xl">💪</span>
										</div>
									{/if}
									<div class="flex-1 min-w-0">
										<div class="flex items-center gap-2 mb-1">
											<h4 class="font-semibold text-gray-900 truncate">{exercise.name}</h4>
											{#if exercise.public}
												<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
													Public
												</span>
											{/if}
										</div>
										{#if exercise.description}
											<p class="text-sm text-gray-600 line-clamp-2">{exercise.description}</p>
										{/if}
									</div>
								</div>
							</button>
						{/each}
					</div>
				{/if}
			</div>

			<!-- Footer -->
			<div class="p-6 border-t border-gray-200 flex justify-end gap-4">
				<button
					onclick={handleClose}
					class="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 font-medium"
				>
					Cancel
				</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.line-clamp-2 {
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>
