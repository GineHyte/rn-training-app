<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { planTrainingService, type PlanTraining } from '$lib/services/planTrainingService';
    import { planExerciseService, type PlanExercise } from '$lib/services/planExerciseService';
    import { trainingService, type Training, type TrainingExercise } from '$lib/services/trainingService';
    import Potentiometer from '$lib/components/Potentiometer.svelte';
    import ExerciseSelector from '$lib/components/ExerciseSelector.svelte';
    import type { Exercise } from '$lib/services/exerciseService';

    const trainingId = $derived(parseInt($page.params.id || '0'));
    let planTraining = $state<PlanTraining | null>(null);
    let planExercises = $state<PlanExercise[]>([]);
    let activeTraining = $state<Training | null>(null);
    let loggedExercises = $state<TrainingExercise[]>([]);
    let loading = $state(true);
    let error = $state('');
    let showExerciseSelector = $state(false);
    let showIntensitySelector = $state(false);
    let selectedExercise = $state<Exercise | null>(null);
    let exerciseIntensity = $state(2);
    let minReps = $state(8);
    let maxReps = $state(12);
    let minSets = $state(3);
    let maxSets = $state(4);
    let showLogSet = $state(false);
    let selectedPlanExerciseId = $state<number>(0);
    let reps = $state<number>(10);
    let kgs = $state<number>(20);
    let showExerciseDetails = $state(false);
    let selectedExerciseDetails = $state<any>(null);

    onMount(async () => {
        await loadTraining();
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

    async function addExerciseToPlan(exercise: Exercise) {
        selectedExercise = exercise;
        showExerciseSelector = false;
        showIntensitySelector = true;
    }

    async function confirmAddExercise() {
        if (!selectedExercise) return;
        
        try {
            await planExerciseService.create({
                planTrainingId: trainingId,
                exerciseId: selectedExercise.id,
                intensity: exerciseIntensity,
                minReps,
                maxReps,
                minSets,
                maxSets
            });
            exerciseIntensity = 2;
            minReps = 8;
            maxReps = 12;
            minSets = 3;
            maxSets = 4;
            selectedExercise = null;
            showIntensitySelector = false;
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

    function showExerciseInfo(exercise: any) {
        selectedExerciseDetails = exercise;
        showExerciseDetails = true;
    }

    function closeExerciseDetails() {
        showExerciseDetails = false;
        selectedExerciseDetails = null;
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
    <!-- Navigation -->
    <nav class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <button onclick={goBack} class="text-gray-700 hover:text-gray-900 mr-4">
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

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
            <!-- Error Alert -->
            {#if error}
                <div class="rounded-md bg-red-50 p-4 mb-4">
                    <p class="text-sm text-red-800">{error}</p>
                </div>
            {/if}

            <!-- Active Training Banner -->
            {#if activeTraining}
                <div class="rounded-md bg-green-50 p-4 mb-4 border-2 border-green-500">
                    <p class="text-sm text-green-800 font-medium">
                        🏋️ Training in progress{activeTraining.startTime ? ` - Started at ${new Date(activeTraining.startTime).toLocaleTimeString()}` : ''}
                    </p>
                </div>
            {/if}

            <!-- Loading State -->
            {#if loading}
                <div class="text-center py-12">
                    <p class="text-gray-500">Loading training...</p>
                </div>
            {:else if planTraining}
                <!-- Training Info Card -->
                <div class="bg-white shadow rounded-lg p-6 mb-6">
                    <h2 class="text-2xl font-bold text-gray-900 mb-4">{planTraining.name}</h2>
                    <div class="grid grid-cols-3 gap-4 text-sm">
                        <div>
                            <span class="text-gray-500">Start Time:</span>
                            <span class="ml-2 font-medium">{planTraining.startTime ? new Date(planTraining.startTime).toLocaleTimeString() : 'Not set'}</span>
                        </div>
                        <div>
                            <span class="text-gray-500">End Time:</span>
                            <span class="ml-2 font-medium">{planTraining.endTime ? new Date(planTraining.endTime).toLocaleTimeString() : 'Not set'}</span>
                        </div>
                        <div>
                            <span class="text-gray-500">Intensity:</span>
                            <span class="ml-2 font-medium">{planTraining.intensity}/3</span>
                        </div>
                    </div>
                </div>

                <!-- Exercises Section Header -->
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-xl font-bold text-gray-900">Exercises</h3>
                    {#if !activeTraining}
                        <button
                            onclick={() => showExerciseSelector = true}
                            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                        >
                            Add Exercise
                        </button>
                    {/if}
                </div>

                <!-- Exercises List -->
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
                                        <div class="mt-2 space-y-1">
                                            <p class="text-sm text-gray-500">
                                                💪 Intensity: {planExercise.intensity}/3
                                            </p>
                                            <p class="text-sm text-gray-500">
                                                🔁 Reps: {planExercise.minReps}-{planExercise.maxReps}
                                            </p>
                                            <p class="text-sm text-gray-500">
                                                📊 Sets: {planExercise.minSets}-{planExercise.maxSets}
                                            </p>
                                        </div>
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

                                <!-- Logged Sets for this Exercise -->
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

    <!-- Exercise Selector Modal -->
    <ExerciseSelector
        isOpen={showExerciseSelector}
        onClose={() => showExerciseSelector = false}
        onSelect={addExerciseToPlan}
    />

    <!-- Intensity Selector Modal -->
    {#if showIntensitySelector && selectedExercise}
        <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto">
                <h4 class="text-lg font-medium mb-4 text-center">Configure Exercise</h4>
                <p class="text-sm text-gray-600 mb-6 text-center">
                    <span class="font-semibold text-gray-900">{selectedExercise.name}</span>
                </p>
                
                <!-- Intensity -->
                <div class="mb-6">
                    <label for="exercise-intensity" class="block text-sm font-medium text-gray-700 mb-2">
                        Intensity: {exerciseIntensity}/3
                    </label>
                    <input
                        id="exercise-intensity"
                        type="range"
                        min="1"
                        max="3"
                        bind:value={exerciseIntensity}
                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                    <div class="flex justify-between text-xs text-gray-500 mt-1">
                        <span>Light</span>
                        <span>Moderate</span>
                        <span>Intense</span>
                    </div>
                </div>

                <!-- Reps Range -->
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-3">
                        Reps Range: {minReps} - {maxReps}
                    </label>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label for="min-reps" class="block text-xs text-gray-600 mb-1">Min Reps</label>
                            <input
                                id="min-reps"
                                type="number"
                                min="1"
                                max={maxReps}
                                bind:value={minReps}
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            />
                        </div>
                        <div>
                            <label for="max-reps" class="block text-xs text-gray-600 mb-1">Max Reps</label>
                            <input
                                id="max-reps"
                                type="number"
                                min={minReps}
                                max="100"
                                bind:value={maxReps}
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            />
                        </div>
                    </div>
                </div>

                <!-- Sets Range -->
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-3">
                        Sets Range: {minSets} - {maxSets}
                    </label>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label for="min-sets" class="block text-xs text-gray-600 mb-1">Min Sets</label>
                            <input
                                id="min-sets"
                                type="number"
                                min="1"
                                max={maxSets}
                                bind:value={minSets}
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            />
                        </div>
                        <div>
                            <label for="max-sets" class="block text-xs text-gray-600 mb-1">Max Sets</label>
                            <input
                                id="max-sets"
                                type="number"
                                min={minSets}
                                max="20"
                                bind:value={maxSets}
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            />
                        </div>
                    </div>
                </div>
                
                <div class="flex gap-4">
                    <button
                        onclick={confirmAddExercise}
                        class="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 font-medium"
                    >
                        Add Exercise
                    </button>
                    <button
                        onclick={() => { 
                            showIntensitySelector = false; 
                            selectedExercise = null; 
                            exerciseIntensity = 2;
                            minReps = 8;
                            maxReps = 12;
                            minSets = 3;
                            maxSets = 4;
                        }}
                        class="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 font-medium"
                    >
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    {/if}

    <!-- Log Set Modal -->
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