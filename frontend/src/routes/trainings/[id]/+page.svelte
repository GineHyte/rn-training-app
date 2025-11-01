<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { planTrainingService, type PlanTraining } from '$lib/services/planTrainingService';
	import { planExerciseService, type PlanExercise } from '$lib/services/planExerciseService';
	import { trainingService, type Training, type TrainingExercise } from '$lib/services/trainingService';
	import { exerciseService } from '$lib/services/exerciseService';
	import Potentiometer from '$lib/components/Potentiometer.svelte';

	const trainingId = $derived(parseInt($page.params.id || '0'));
	let planTraining = $state<PlanTraining | null>(null);
	let planExercises = $state<PlanExercise[]>([]);
	let activeTraining = $state<Training | null>(null);
	let loggedExercises = $state<TrainingExercise[]>([]);
	let loading = $state(true);
	let error = $state('');
	let showAddExercise = $state(false);
	let availableExercises = $state<any[]>([]);
	let selectedExerciseId = $state<number>(0);
	let exerciseIntensity = $state(1);

	// For logging sets
	let showLogSet = $state(false);
	let selectedPlanExerciseId = $state<number>(0);
	let reps = $state<number>(10);
	let kgs = $state<number>(20);

	onMount(async () => {
		await loadTraining();
		await loadAvailableExercises();
	});

	async function loadTraining() {
		loading = true;
		error = '';
		try {
			const ptData = await planTrainingService.getById(trainingId);
			planTraining = ptData;
			const peData = await planExerciseService.getByTraining(trainingId);
			planExercises = peData;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load training';
		} finally {
			loading = false;
		}
	}

	async function loadAvailableExercises() {
		try {
			const exercises = await exerciseService.getAll();
			availableExercises = exercises;
		} catch (err: any) {
			console.error('Failed to load exercises:', err);
		}
	}

	async function startTraining() {
		try {
			activeTraining = await trainingService.create({
				planTrainingId: trainingId,
				startTime: new Date().toISOString()
			});
			loggedExercises = [];
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to start training';
		}
	}

	async function endTraining() {
		if (!activeTraining) return;
		if (!confirm('Are you sure you want to end this training session?')) return;
		
		try {
			await trainingService.endTraining(activeTraining.id);
			activeTraining = null;
			loggedExercises = [];
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to end training';
		}
	}

	async function addExerciseToPlan() {
		if (!selectedExerciseId) {
			error = 'Please select an exercise';
			return;
		}

		try {
			await planExerciseService.create({
				planTrainingId: trainingId,
				exerciseId: selectedExerciseId,
				intensity: exerciseIntensity
			});
			showAddExercise = false;
			selectedExerciseId = 0;
			exerciseIntensity = 1;
			await loadTraining();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to add exercise';
		}
	}

	async function removeExerciseFromPlan(planExerciseId: number) {
		if (!confirm('Remove this exercise from the training plan?')) return;
		
		try {
			await planExerciseService.delete(planExerciseId);
			await loadTraining();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to remove exercise';
		}
	}

	function openLogSet(planExerciseId: number) {
		selectedPlanExerciseId = planExerciseId;
		showLogSet = true;
	}

	async function logSet() {
		if (!activeTraining || !selectedPlanExerciseId) return;
		
		try {
			const newSet = await trainingService.addExercise({
				trainingId: activeTraining.id,
				planExerciseId: selectedPlanExerciseId,
				reps,
				kgs,
				timestamp: new Date().toISOString()
			});
			loggedExercises = [...loggedExercises, newSet];
			showLogSet = false;
			selectedPlanExerciseId = 0;
			reps = 10;
			kgs = 20;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to log set';
		}
	}

	function getLoggedSetsForExercise(planExerciseId: number) {
		return loggedExercises.filter(e => e.planExerciseId === planExerciseId);
	}

	async function deleteSet(setId: number) {
		if (!confirm('Delete this set?')) return;
		
		try {
			await trainingService.deleteExercise(setId);
			loggedExercises = loggedExercises.filter(e => e.id !== setId);
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete set';
		}
	}

	function goBack() {
		goto('/plans');
	}
</script>

<div class="min-h-screen bg-gray-50">
	<nav class="bg-white shadow-sm">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between h-16">
				<div class="flex items-center">
					<button
						onclick={goBack}
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
							onclick={startTraining}
							class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium"
						>
							🚀 Start Training
						</button>
					{:else}
						<button
							onclick={endTraining}
							class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium"
						>
							⏹️ End Training
						</button>
					{/if}
				</div>
			</div>
		</div>
	</nav>

	<div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
		<div class="px-4 py-6 sm:px-0">
			{#if error}
				<div class="rounded-md bg-red-50 p-4 mb-4">
					<p class="text-sm text-red-800">{error}</p>
				</div>
			{/if}

			{#if activeTraining}
				<div class="rounded-md bg-green-50 p-4 mb-4 border-2 border-green-500">
					<p class="text-sm text-green-800 font-medium">
						🏋️ Training in progress - Started at {new Date(activeTraining.startTime).toLocaleTimeString()}
					</p>
				</div>
			{/if}

			{#if loading}
				<div class="text-center py-12">
					<p class="text-gray-500">Loading training...</p>
				</div>
			{:else if planTraining}
				<div class="bg-white shadow rounded-lg p-6 mb-6">
					<h2 class="text-2xl font-bold text-gray-900 mb-4">{planTraining.name}</h2>
					<div class="grid grid-cols-3 gap-4 text-sm">
						<div>
							<span class="text-gray-500">Start Time:</span>
							<span class="ml-2 font-medium">{new Date(planTraining.startTime).toLocaleTimeString()}</span>
						</div>
						<div>
							<span class="text-gray-500">End Time:</span>
							<span class="ml-2 font-medium">{new Date(planTraining.endTime).toLocaleTimeString()}</span>
						</div>
						<div>
							<span class="text-gray-500">Intensity:</span>
							<span class="ml-2 font-medium">{planTraining.intensity}/3</span>
						</div>
					</div>
				</div>

				<div class="flex justify-between items-center mb-6">
					<h3 class="text-xl font-bold text-gray-900">Exercises</h3>
					{#if !activeTraining}
						<button
							onclick={() => showAddExercise = true}
							class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
						>
							Add Exercise
						</button>
					{/if}
				</div>

				{#if showAddExercise}
					<div class="bg-white shadow rounded-lg p-6 mb-6">
						<h4 class="text-lg font-medium mb-4">Add Exercise to Training</h4>
						<div class="space-y-4">
							<div>
								<label class="block text-sm font-medium text-gray-700 mb-2">
									Select Exercise
								</label>
								<select
									bind:value={selectedExerciseId}
									class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
								>
									<option value={0}>Choose an exercise...</option>
									{#each availableExercises as exercise}
										<option value={exercise.id}>{exercise.name}</option>
									{/each}
								</select>
							</div>
							<div>
								<label class="block text-sm font-medium text-gray-700 mb-2">
									Intensity: {exerciseIntensity}/3
								</label>
								<input
									type="range"
									min="1"
									max="3"
									bind:value={exerciseIntensity}
									class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
								/>
							</div>
							<div class="flex gap-4">
								<button
									onclick={addExerciseToPlan}
									class="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
								>
									Add
								</button>
								<button
									onclick={() => { showAddExercise = false; selectedExerciseId = 0; }}
									class="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
								>
									Cancel
								</button>
							</div>
						</div>
					</div>
				{/if}

				{#if showLogSet}
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
									onclick={logSet}
									class="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
								>
									Log Set
								</button>
								<button
									onclick={() => { showLogSet = false; selectedPlanExerciseId = 0; }}
									class="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
								>
									Cancel
								</button>
							</div>
						</div>
					</div>
				{/if}

				{#if planExercises.length === 0}
					<div class="text-center py-12 bg-white rounded-lg shadow">
						<p class="text-gray-500 mb-4">No exercises in this training yet. Add your first exercise!</p>
					</div>
				{:else}
					<div class="space-y-4">
						{#each planExercises as planExercise}
							<div class="bg-white shadow rounded-lg p-6">
								<div class="flex justify-between items-start mb-4">
									<div>
										<h4 class="text-lg font-medium text-gray-900">
											{planExercise.exercise?.name || 'Exercise'}
										</h4>
										<p class="text-sm text-gray-500">Intensity: {planExercise.intensity}/3</p>
										{#if planExercise.exercise?.description}
											<p class="text-sm text-gray-600 mt-2">{planExercise.exercise.description}</p>
										{/if}
									</div>
									<div class="flex gap-2">
										{#if activeTraining}
											<button
												onclick={() => openLogSet(planExercise.id)}
												class="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
											>
												Log Set
											</button>
										{:else}
											<button
												onclick={() => removeExerciseFromPlan(planExercise.id)}
												class="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
											>
												Remove
											</button>
										{/if}
									</div>
								</div>

								{#if activeTraining}
									{@const sets = getLoggedSetsForExercise(planExercise.id)}
									{#if sets.length > 0}
										<div class="border-t border-gray-200 pt-4 mt-4">
											<h5 class="text-sm font-medium text-gray-700 mb-2">Logged Sets:</h5>
											<div class="space-y-2">
												{#each sets as set, index}
													<div class="flex justify-between items-center text-sm bg-gray-50 p-2 rounded">
														<span class="font-medium">Set {index + 1}:</span>
														<span>{set.reps} reps × {set.kgs} kg</span>
														<span class="text-gray-500 text-xs">{new Date(set.timestamp).toLocaleTimeString()}</span>
														<button
															onclick={() => deleteSet(set.id)}
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
								{/if}
							</div>
						{/each}
					</div>
				{/if}
			{/if}
		</div>
	</div>
</div>
