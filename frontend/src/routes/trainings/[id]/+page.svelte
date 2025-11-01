<script lang="ts"></script><script lang="ts">

	import { onMount } from 'svelte';	import { onMount } from 'svelte';

	import { goto } from '$app/navigation';	import { goto } from '$app/navigation';

	import { page } from '$app/stores';	import { page } from '$app/stores';

	import { planTrainingService, type PlanTraining } from '$lib/services/planTrainingService';	import { planTrainingService, type PlanTraining } from '$lib/services/planTrainingService';

	import { planExerciseService, type PlanExercise } from '$lib/services/planExerciseService';	import { planExerciseService, type PlanExercise } from '$lib/services/planExerciseService';

	import { trainingService, type Training, type TrainingExercise } from '$lib/services/trainingService';	import { trainingService, type Training, type TrainingExercise } from '$lib/services/trainingService';

	import ExerciseSelector from '$lib/components/ExerciseSelector.svelte';	import ExerciseSelector from '$lib/components/ExerciseSelector.svelte';

	import type { Exercise } from '$lib/services/exerciseService';	import type { Exercise } from '$lib/services/exerciseService';

		

	// Import local components	// Import local components

	import TrainingHeader from './components/TrainingHeader.svelte';	import TrainingHeader from './components/TrainingHeader.svelte';

	import TrainingInfo from './components/TrainingInfo.svelte';	import TrainingInfo from './components/TrainingInfo.svelte';

	import ExerciseCard from './components/ExerciseCard.svelte';	import ExerciseCard from './components/ExerciseCard.svelte';

	import LogSetModal from './components/LogSetModal.svelte';	import LogSetModal from './components/LogSetModal.svelte';

	import ExerciseDetailsModal from './components/ExerciseDetailsModal.svelte';	import ExerciseDetailsModal from './components/ExerciseDetailsModal.svelte';



	const trainingId = $derived(parseInt($page.params.id || '0'));	const trainingId = $derived(parseInt($page.params.id || '0'));

	let planTraining = $state<PlanTraining | null>(null);	let planTraining = $state<PlanTraining | null>(null);

	let planExercises = $state<PlanExercise[]>([]);	let planExercises = $state<PlanExercise[]>([]);

	let activeTraining = $state<Training | null>(null);	let activeTraining = $state<Training | null>(null);

	let loggedExercises = $state<TrainingExercise[]>([]);	let loggedExercises = $state<TrainingExercise[]>([]);

	let loading = $state(true);	let loading = $state(true);

	let error = $state('');	let error = $state('');

	let showExerciseSelector = $state(false);	let showExerciseSelector = $state(false);

	let exerciseIntensity = $state(1);	let exerciseIntensity = $state(1);



	// For logging sets	// For logging sets

	let showLogSet = $state(false);	let showLogSet = $state(false);

	let selectedPlanExerciseId = $state<number>(0);	let selectedPlanExerciseId = $state<number>(0);

	let reps = $state<number>(10);	let reps = $state<number>(10);

	let kgs = $state<number>(20);	let kgs = $state<number>(20);



	// For exercise details modal	// For exercise details modal

	let showExerciseDetails = $state(false);	let showExerciseDetails = $state(false);

	let selectedExerciseDetails = $state<any>(null);	let selectedExerciseDetails = $state<any>(null);



	onMount(async () => {	onMount(async () => {

		await loadTraining();		await loadTraining();

	});	});



	async function loadTraining() {	async function loadTraining() {

		loading = true;		loading = true;

		error = '';		error = '';

		try {		try {

			const ptData = await planTrainingService.getById(trainingId);			const ptData = await planTrainingService.getById(trainingId);

			planTraining = ptData;			planTraining = ptData;

			const peData = await planExerciseService.getByTraining(trainingId);			const peData = await planExerciseService.getByTraining(trainingId);

			planExercises = peData;			planExercises = peData;

		} catch (err: any) {		} catch (err: any) {

			error = err.response?.data?.detail || 'Failed to load training';			error = err.response?.data?.detail || 'Failed to load training';

		} finally {		} finally {

			loading = false;			loading = false;

		}		}

	}	}



	async function startTraining() {	async function startTraining() {

		try {		try {

			activeTraining = await trainingService.create({			activeTraining = await trainingService.create({

				planTrainingId: trainingId,				planTrainingId: trainingId,

				startTime: new Date().toISOString()				startTime: new Date().toISOString()

			});			});

			loggedExercises = [];			loggedExercises = [];

		} catch (err: any) {		} catch (err: any) {

			error = err.response?.data?.detail || 'Failed to start training';			error = err.response?.data?.detail || 'Failed to start training';

		}		}

	}	}



	async function endTraining() {	async function endTraining() {

		if (!activeTraining) return;		if (!activeTraining) return;

		if (!confirm('Are you sure you want to end this training session?')) return;		if (!confirm('Are you sure you want to end this training session?')) return;

				

		try {		try {

			await trainingService.endTraining(activeTraining.id);			await trainingService.endTraining(activeTraining.id);

			activeTraining = null;			activeTraining = null;

			loggedExercises = [];			loggedExercises = [];

		} catch (err: any) {		} catch (err: any) {

			error = err.response?.data?.detail || 'Failed to end training';			error = err.response?.data?.detail || 'Failed to end training';

		}		}

	}	}



	async function addExerciseToPlan(exercise: Exercise) {	async function addExerciseToPlan(exercise: Exercise) {

		try {		try {

			await planExerciseService.create({			await planExerciseService.create({

				planTrainingId: trainingId,				planTrainingId: trainingId,

				exerciseId: exercise.id,				exerciseId: exercise.id,

				intensity: exerciseIntensity				intensity: exerciseIntensity

			});			});

			exerciseIntensity = 1;			exerciseIntensity = 1;

			await loadTraining();			await loadTraining();

		} catch (err: any) {		} catch (err: any) {

			error = err.response?.data?.detail || 'Failed to add exercise';			error = err.response?.data?.detail || 'Failed to add exercise';

		}		}

	}	}



	async function removeExerciseFromPlan(planExerciseId: number) {	async function removeExerciseFromPlan(planExerciseId: number) {

		if (!confirm('Remove this exercise from the training plan?')) return;		if (!confirm('Remove this exercise from the training plan?')) return;

				

		try {		try {

			await planExerciseService.delete(planExerciseId);			await planExerciseService.delete(planExerciseId);

			await loadTraining();			await loadTraining();

		} catch (err: any) {		} catch (err: any) {

			error = err.response?.data?.detail || 'Failed to remove exercise';			error = err.response?.data?.detail || 'Failed to remove exercise';

		}		}

	}	}



	function openLogSet(planExerciseId: number) {	function openLogSet(planExerciseId: number) {

		selectedPlanExerciseId = planExerciseId;		selectedPlanExerciseId = planExerciseId;

		showLogSet = true;		showLogSet = true;

	}	}



	async function logSet() {	async function logSet() {

		if (!activeTraining || !selectedPlanExerciseId) return;		if (!activeTraining || !selectedPlanExerciseId) return;

				

		try {		try {

			const newSet = await trainingService.addExercise({			const newSet = await trainingService.addExercise({

				trainingId: activeTraining.id,				trainingId: activeTraining.id,

				planExerciseId: selectedPlanExerciseId,				planExerciseId: selectedPlanExerciseId,

				reps,				reps,

				kgs,				kgs,

				timestamp: new Date().toISOString()				timestamp: new Date().toISOString()

			});			});

			loggedExercises = [...loggedExercises, newSet];			loggedExercises = [...loggedExercises, newSet];

			showLogSet = false;			showLogSet = false;

			selectedPlanExerciseId = 0;			selectedPlanExerciseId = 0;

			reps = 10;			reps = 10;

			kgs = 20;			kgs = 20;

		} catch (err: any) {		} catch (err: any) {

			error = err.response?.data?.detail || 'Failed to log set';			error = err.response?.data?.detail || 'Failed to log set';

		}		}

	}	}



	function closeLogSetModal() {	function getLoggedSetsForExercise(planExerciseId: number) {

		showLogSet = false;		return loggedExercises.filter(e => e.planExerciseId === planExerciseId);

		selectedPlanExerciseId = 0;	}

	}

	function showExerciseInfo(exercise: any) {

	function getLoggedSetsForExercise(planExerciseId: number) {		selectedExerciseDetails = exercise;

		return loggedExercises.filter(e => e.planExerciseId === planExerciseId);		showExerciseDetails = true;

	}	}



	function showExerciseInfo(exercise: any) {	function closeExerciseDetails() {

		selectedExerciseDetails = exercise;		showExerciseDetails = false;

		showExerciseDetails = true;		selectedExerciseDetails = null;

	}	}



	function closeExerciseDetails() {	async function deleteSet(setId: number) {

		showExerciseDetails = false;		if (!confirm('Delete this set?')) return;

		selectedExerciseDetails = null;		

	}		try {

			await trainingService.deleteExercise(setId);

	async function deleteSet(setId: number) {			loggedExercises = loggedExercises.filter(e => e.id !== setId);

		if (!confirm('Delete this set?')) return;		} catch (err: any) {

					error = err.response?.data?.detail || 'Failed to delete set';

		try {		}

			await trainingService.deleteExercise(setId);	}

			loggedExercises = loggedExercises.filter(e => e.id !== setId);

		} catch (err: any) {	function goBack() {

			error = err.response?.data?.detail || 'Failed to delete set';		goto('/plans');

		}	}

	}</script>



	function goBack() {<div class="min-h-screen bg-gray-50">

		goto('/plans');	<nav class="bg-white shadow-sm">

	}		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

</script>			<div class="flex justify-between h-16">

				<div class="flex items-center">

<div class="min-h-screen bg-gray-50">					<button

	<TrainingHeader						onclick={goBack}

		{planTraining}						class="text-gray-700 hover:text-gray-900 mr-4"

		{activeTraining}					>

		onBack={goBack}						← Back

		onStartTraining={startTraining}					</button>

		onEndTraining={endTraining}					<h1 class="text-xl font-bold text-gray-900">

	/>						{planTraining?.name || 'Training Details'}

					</h1>

	<div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">				</div>

		<div class="px-4 py-6 sm:px-0">				<div class="flex items-center">

			{#if error}					{#if !activeTraining}

				<div class="rounded-md bg-red-50 p-4 mb-4">						<button

					<p class="text-sm text-red-800">{error}</p>							onclick={startTraining}

				</div>							class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium"

			{/if}						>

							🚀 Start Training

			{#if activeTraining}						</button>

				<div class="rounded-md bg-green-50 p-4 mb-4 border-2 border-green-500">					{:else}

					<p class="text-sm text-green-800 font-medium">						<button

						🏋️ Training in progress - Started at {new Date(activeTraining.startTime).toLocaleTimeString()}							onclick={endTraining}

					</p>							class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-medium"

				</div>						>

			{/if}							⏹️ End Training

						</button>

			{#if loading}					{/if}

				<div class="text-center py-12">				</div>

					<p class="text-gray-500">Loading training...</p>			</div>

				</div>		</div>

			{:else if planTraining}	</nav>

				<TrainingInfo {planTraining} />

	<div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">

				<div class="flex justify-between items-center mb-6">		<div class="px-4 py-6 sm:px-0">

					<h3 class="text-xl font-bold text-gray-900">Exercises</h3>			{#if error}

					{#if !activeTraining}				<div class="rounded-md bg-red-50 p-4 mb-4">

						<button					<p class="text-sm text-red-800">{error}</p>

							onclick={() => showExerciseSelector = true}				</div>

							class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"			{/if}

						>

							Add Exercise			{#if activeTraining}

						</button>				<div class="rounded-md bg-green-50 p-4 mb-4 border-2 border-green-500">

					{/if}					<p class="text-sm text-green-800 font-medium">

				</div>						🏋️ Training in progress - Started at {new Date(activeTraining.startTime).toLocaleTimeString()}

					</p>

				<!-- Exercise Selector Modal -->				</div>

				<ExerciseSelector			{/if}

					isOpen={showExerciseSelector}

					onClose={() => showExerciseSelector = false}			{#if loading}

					onSelect={addExerciseToPlan}				<div class="text-center py-12">

				/>					<p class="text-gray-500">Loading training...</p>

				</div>

				<!-- Log Set Modal -->			{:else if planTraining}

				<LogSetModal				<div class="bg-white shadow rounded-lg p-6 mb-6">

					isOpen={showLogSet}					<h2 class="text-2xl font-bold text-gray-900 mb-4">{planTraining.name}</h2>

					bind:reps					<div class="grid grid-cols-3 gap-4 text-sm">

					bind:kgs						<div>

					onClose={closeLogSetModal}							<span class="text-gray-500">Start Time:</span>

					onLog={logSet}							<span class="ml-2 font-medium">{new Date(planTraining.startTime).toLocaleTimeString()}</span>

				/>						</div>

						<div>

				<!-- Exercises List -->							<span class="text-gray-500">End Time:</span>

				{#if planExercises.length === 0}							<span class="ml-2 font-medium">{new Date(planTraining.endTime).toLocaleTimeString()}</span>

					<div class="text-center py-12 bg-white rounded-lg shadow">						</div>

						<p class="text-gray-500 mb-4">No exercises in this training yet. Add your first exercise!</p>						<div>

					</div>							<span class="text-gray-500">Intensity:</span>

				{:else}						<span class="ml-2 font-medium">{planTraining.intensity}/3</span>

					<div class="space-y-4">					</div>

						{#each planExercises as planExercise}				</div>

							<ExerciseCard			</div>

								{planExercise}

								activeTraining={!!activeTraining}			<div class="flex justify-between items-center mb-6">

								loggedSets={getLoggedSetsForExercise(planExercise.id)}				<h3 class="text-xl font-bold text-gray-900">Exercises</h3>

								onShowDetails={showExerciseInfo}				{#if !activeTraining}

								onLogSet={openLogSet}					<button

								onRemove={removeExerciseFromPlan}						onclick={() => showExerciseSelector = true}

								onDeleteSet={deleteSet}						class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"

							/>					>

						{/each}						Add Exercise

					</div>					</button>

				{/if}				{/if}

			{/if}			</div>

		</div>

	</div>			<!-- Exercise Selector Modal -->

			<ExerciseSelector

	<!-- Exercise Details Modal -->				isOpen={showExerciseSelector}

	<ExerciseDetailsModal				onClose={() => showExerciseSelector = false}

		isOpen={showExerciseDetails}				onSelect={addExerciseToPlan}

		exercise={selectedExerciseDetails}			/>

		onClose={closeExerciseDetails}

	/>			{#if showLogSet}				{#if showLogSet}

</div>					<div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">

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
									<div class="flex-1">
										<button
											onclick={() => showExerciseInfo(planExercise.exercise)}
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

	<!-- Exercise Details Modal -->
	{#if showExerciseDetails && selectedExerciseDetails}
		<div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
			<div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
				<div class="flex justify-between items-start mb-4">
					<h3 class="text-2xl font-bold text-gray-900">{selectedExerciseDetails.name}</h3>
					<button
						onclick={closeExerciseDetails}
						class="text-gray-400 hover:text-gray-600 text-2xl"
					>
						×
					</button>
				</div>

				{#if selectedExerciseDetails.image}
					<div class="mb-4">
						<img
							src={selectedExerciseDetails.image}
							alt={selectedExerciseDetails.name}
							class="w-full rounded-lg shadow-md"
						/>
					</div>
				{/if}

				{#if selectedExerciseDetails.description}
					<div class="mb-4">
						<h4 class="text-lg font-semibold text-gray-900 mb-2">Description</h4>
						<p class="text-gray-700 whitespace-pre-wrap">{selectedExerciseDetails.description}</p>
					</div>
				{/if}

				{#if selectedExerciseDetails.video}
					<div class="mb-4">
						<h4 class="text-lg font-semibold text-gray-900 mb-2">Video</h4>
						{#if selectedExerciseDetails.video.includes('youtube.com') || selectedExerciseDetails.video.includes('youtu.be')}
							<div class="aspect-video">
								<iframe
									src={selectedExerciseDetails.video.replace('watch?v=', 'embed/')}
									class="w-full h-full rounded-lg"
									frameborder="0"
									allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
									allowfullscreen
								></iframe>
							</div>
						{:else}
							<a
								href={selectedExerciseDetails.video}
								target="_blank"
								rel="noopener noreferrer"
								class="text-blue-600 hover:underline"
							>
								Watch Video
							</a>
						{/if}
					</div>
				{/if}

				<div class="flex justify-end mt-6">
					<button
						onclick={closeExerciseDetails}
						class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
					>
						Close
					</button>
				</div>
			</div>
		</div>
	{/if}
</div>
