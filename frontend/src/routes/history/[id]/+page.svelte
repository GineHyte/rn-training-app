<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { trainingService, type Training, type TrainingExercise } from '$lib/services/trainingService';
	import { planExerciseService, type PlanExercise } from '$lib/services/planExerciseService';
	import { planTrainingService, type PlanTraining } from '$lib/services/planTrainingService';

	const trainingId = $derived(parseInt($page.params.id || '0'));
	let training = $state<Training | null>(null);
	let planTraining = $state<PlanTraining | null>(null);
	let trainingExercises = $state<TrainingExercise[]>([]);
	let planExercises = $state<PlanExercise[]>([]);
	let loading = $state(true);
	let error = $state('');
	let showDeleteConfirm = $state(false);

	onMount(async () => {
		await loadTrainingDetails();
	});

	async function loadTrainingDetails() {
		loading = true;
		error = '';
		try {
			training = await trainingService.getById(trainingId);
			trainingExercises = await trainingService.getExercises(trainingId);
			
			if (training) {
				planTraining = await planTrainingService.getById(training.planTrainingId);
				planExercises = await planExerciseService.getByTraining(training.planTrainingId);
			}
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load training details';
		} finally {
			loading = false;
		}
	}

	async function deleteTraining() {
		try {
			await trainingService.delete(trainingId);
			goto('/history');
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete training';
			showDeleteConfirm = false;
		}
	}

	function formatDuration(start: string | null, end: string | null): string {
		if (!start) return 'N/A';
		if (!end) return 'In progress';
		const startTime = new Date(start);
		const endTime = new Date(end);
		const durationMs = endTime.getTime() - startTime.getTime();
		const hours = Math.floor(durationMs / 3600000);
		const minutes = Math.floor((durationMs % 3600000) / 60000);
		if (hours > 0) {
			return `${hours}h ${minutes}m`;
		}
		return `${minutes}m`;
	}

	function getExerciseSets(planExerciseId: number): TrainingExercise[] {
		return trainingExercises.filter(ex => ex.planExerciseId === planExerciseId);
	}

	function getPlanExerciseDetails(planExerciseId: number): PlanExercise | undefined {
		return planExercises.find(pe => pe.id === planExerciseId);
	}

	function calculateTotalVolume(sets: TrainingExercise[]): number {
		return sets.reduce((total, set) => total + (set.reps * set.kgs), 0);
	}

	function goBack() {
		goto('/history');
	}
</script>

<div class="min-h-screen bg-gray-50">
	<!-- Navigation -->
	<nav class="bg-white shadow-sm">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between h-16">
				<div class="flex items-center">
					<button onclick={goBack} class="text-gray-700 hover:text-gray-900 mr-4">
						← Back to History
					</button>
					<h1 class="text-xl font-bold text-gray-900">Training Overview</h1>
				</div>
				<div class="flex items-center">
					<button
						onclick={() => showDeleteConfirm = true}
						class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium"
					>
						🗑️ Delete Training
					</button>
				</div>
			</div>
		</div>
	</nav>

	<!-- Main Content -->
	<div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
		<div class="px-4 py-6 sm:px-0">
			<!-- Error Alert -->
			{#if error}
				<div class="rounded-md bg-red-50 p-4 mb-4">
					<p class="text-sm text-red-800">{error}</p>
				</div>
			{/if}

			<!-- Loading State -->
			{#if loading}
				<div class="text-center py-12">
					<p class="text-gray-500">Loading training details...</p>
				</div>
			{:else if training && planTraining}
				<!-- Training Summary Card -->
				<div class="bg-white shadow rounded-lg p-6 mb-6">
					<h2 class="text-2xl font-bold text-gray-900 mb-4">{planTraining.name}</h2>
					<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
						<div>
							<span class="text-sm text-gray-500">Date:</span>
							<p class="font-medium">{training.startTime ? new Date(training.startTime).toLocaleDateString() : 'N/A'}</p>
						</div>
						<div>
							<span class="text-sm text-gray-500">Start Time:</span>
							<p class="font-medium">{training.startTime ? new Date(training.startTime).toLocaleTimeString() : 'N/A'}</p>
						</div>
						<div>
							<span class="text-sm text-gray-500">End Time:</span>
							<p class="font-medium">{training.endTime ? new Date(training.endTime).toLocaleTimeString() : 'In progress'}</p>
						</div>
						<div>
							<span class="text-sm text-gray-500">Duration:</span>
							<p class="font-medium">{formatDuration(training.startTime, training.endTime)}</p>
						</div>
					</div>
					<div class="mt-4 pt-4 border-t border-gray-200">
						<div class="grid grid-cols-2 md:grid-cols-3 gap-4">
							<div>
								<span class="text-sm text-gray-500">Plan Intensity:</span>
								<p class="font-medium">{planTraining.intensity}/3</p>
							</div>
							<div>
								<span class="text-sm text-gray-500">Total Exercises:</span>
								<p class="font-medium">{planExercises.length}</p>
							</div>
							<div>
								<span class="text-sm text-gray-500">Total Sets:</span>
								<p class="font-medium">{trainingExercises.length}</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Exercises Section -->
				<div class="bg-white shadow rounded-lg p-6">
					<h3 class="text-xl font-bold text-gray-900 mb-6">Exercises Performed</h3>

					{#if planExercises.length === 0}
						<p class="text-gray-500">No exercises in this training plan.</p>
					{:else}
						<div class="space-y-6">
							{#each planExercises as planExercise}
								{@const sets = getExerciseSets(planExercise.id)}
								{@const totalVolume = calculateTotalVolume(sets)}
								<div class="border border-gray-200 rounded-lg p-5">
									<!-- Exercise Header -->
									<div class="flex justify-between items-start mb-4">
										<div class="flex-1">
											<h4 class="text-lg font-semibold text-gray-900 mb-2">
												{planExercise.exercise?.name || 'Unknown Exercise'}
											</h4>
											<div class="flex gap-4 text-sm text-gray-600">
												<span>💪 Intensity: {planExercise.intensity}/3</span>
												<span>🔁 Target: {planExercise.minReps}-{planExercise.maxReps} reps</span>
												<span>📊 Target: {planExercise.minSets}-{planExercise.maxSets} sets</span>
											</div>
										</div>
										{#if sets.length > 0}
											<div class="text-right">
												<div class="text-sm text-gray-500">Total Volume</div>
												<div class="text-xl font-bold text-indigo-600">{totalVolume} kg</div>
											</div>
										{/if}
									</div>

									<!-- Sets Table -->
									{#if sets.length > 0}
										<div class="mt-4">
											<div class="overflow-x-auto">
												<table class="min-w-full divide-y divide-gray-200">
													<thead class="bg-gray-50">
														<tr>
															<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Set</th>
															<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reps</th>
															<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Weight (kg)</th>
															<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Volume</th>
															<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
														</tr>
													</thead>
													<tbody class="bg-white divide-y divide-gray-200">
														{#each sets.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()) as set, index}
															<tr class="hover:bg-gray-50">
																<td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
																	{index + 1}
																</td>
																<td class="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
																	{set.reps}
																</td>
																<td class="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
																	{set.kgs}
																</td>
																<td class="px-4 py-3 whitespace-nowrap text-sm text-gray-700 font-medium">
																	{set.reps * set.kgs} kg
																</td>
																<td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
																	{new Date(set.timestamp).toLocaleTimeString()}
																</td>
															</tr>
														{/each}
													</tbody>
												</table>
											</div>
											<!-- Sets Summary -->
											<div class="mt-3 flex gap-6 text-sm">
												<div>
													<span class="text-gray-500">Sets completed:</span>
													<span class="ml-1 font-medium">{sets.length}</span>
												</div>
												<div>
													<span class="text-gray-500">Avg reps:</span>
													<span class="ml-1 font-medium">{(sets.reduce((sum, s) => sum + s.reps, 0) / sets.length).toFixed(1)}</span>
												</div>
												<div>
													<span class="text-gray-500">Avg weight:</span>
													<span class="ml-1 font-medium">{(sets.reduce((sum, s) => sum + s.kgs, 0) / sets.length).toFixed(1)} kg</span>
												</div>
											</div>
										</div>
									{:else}
										<div class="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
											<p class="text-sm text-yellow-800">No sets logged for this exercise</p>
										</div>
									{/if}
								</div>
							{/each}
						</div>
					{/if}
				</div>
			{/if}
		</div>
	</div>

	<!-- Delete Confirmation Modal -->
	{#if showDeleteConfirm}
		<div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
			<div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
				<h3 class="text-lg font-medium text-gray-900 mb-4">Delete Training?</h3>
				<p class="text-sm text-gray-600 mb-6">
					Are you sure you want to delete this training session? This action cannot be undone and will delete all exercise logs associated with this training.
				</p>
				<div class="flex gap-4">
					<button
						onclick={deleteTraining}
						class="flex-1 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium"
					>
						Delete
					</button>
					<button
						onclick={() => showDeleteConfirm = false}
						class="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 font-medium"
					>
						Cancel
					</button>
				</div>
			</div>
		</div>
	{/if}
</div>
