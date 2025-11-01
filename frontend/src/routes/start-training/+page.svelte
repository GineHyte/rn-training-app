<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { title } from '$lib/stores/title';
	import { planService, type Plan } from '$lib/services/planService';
	import { planWeekService, type PlanWeek } from '$lib/services/planWeekService';
	import { planTrainingService, type PlanTraining } from '$lib/services/planTrainingService';

	let plans = $state<Plan[]>([]);
	let selectedPlanId = $state<number>(0);
	let weeks = $state<PlanWeek[]>([]);
	let selectedWeekId = $state<number>(0);
	let trainings = $state<PlanTraining[]>([]);
	let loading = $state(true);
	let error = $state('');

	onMount(async () => {
		title.setTitle('Start Training');
		await loadPlans();
	});

	async function loadPlans() {
		loading = true;
		error = '';
		try {
			plans = await planService.getAll();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load plans';
		} finally {
			loading = false;
		}
	}

	async function onPlanSelect() {
		if (!selectedPlanId) {
			weeks = [];
			trainings = [];
			return;
		}
		
		try {
			weeks = await planWeekService.getByPlan(selectedPlanId);
			selectedWeekId = 0;
			trainings = [];
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load weeks';
		}
	}

	async function onWeekSelect() {
		if (!selectedWeekId) {
			trainings = [];
			return;
		}
		
		try {
			trainings = await planTrainingService.getByWeek(selectedWeekId);
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load trainings';
		}
	}

	function startTraining(trainingId: number) {
		goto(`/trainings/${trainingId}`);
	}

	function formatTime(timeStr: string) {
		const date = new Date(`1970-01-01T${timeStr}`);
		return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
	}
</script>

<div class="max-w-4xl mx-auto px-4 py-8">
	{#if error}
		<div class="rounded-md bg-red-50 p-4 mb-6">
			<p class="text-sm text-red-800">{error}</p>
		</div>
	{/if}

	{#if loading}
		<div class="text-center py-12">
			<p class="text-gray-500">Loading plans...</p>
		</div>
	{:else if plans.length === 0}
		<div class="text-center py-12 bg-white rounded-lg shadow">
			<p class="text-gray-500 mb-4">No plans available. Create a plan first!</p>
			<button
				onclick={() => goto('/plans/create')}
				class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
			>
				Create Plan
			</button>
		</div>
	{:else}
		<div class="space-y-6">
			<!-- Step 1: Select Plan -->
			<div class="bg-white rounded-lg shadow p-6">
				<h2 class="text-xl font-bold text-gray-900 mb-4">1. Select a Plan</h2>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					{#each plans as plan}
						<button
							onclick={() => { selectedPlanId = plan.id; onPlanSelect(); }}
							class={`p-4 rounded-lg border-2 text-left transition ${
								selectedPlanId === plan.id
									? 'border-blue-600 bg-blue-50'
									: 'border-gray-200 hover:border-blue-300'
							}`}
						>
							<h3 class="font-semibold text-gray-900">{plan.name}</h3>
							<p class="text-sm text-gray-600 mt-1">
								Start: {new Date(plan.startDate).toLocaleDateString()}
							</p>
						</button>
					{/each}
				</div>
			</div>

			<!-- Step 2: Select Week -->
			{#if weeks.length > 0}
				<div class="bg-white rounded-lg shadow p-6">
					<h2 class="text-xl font-bold text-gray-900 mb-4">2. Select a Week</h2>
					<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
						{#each weeks as week, index}
							<button
								onclick={() => { selectedWeekId = week.id; onWeekSelect(); }}
								class={`p-4 rounded-lg border-2 text-center transition ${
									selectedWeekId === week.id
										? 'border-blue-600 bg-blue-50'
										: 'border-gray-200 hover:border-blue-300'
								}`}
							>
								<div class="font-semibold text-gray-900">Week {index + 1}</div>
								<div class="text-xs text-gray-500 mt-1">
									{new Date(week.startDate).toLocaleDateString()}
								</div>
							</button>
						{/each}
					</div>
				</div>
			{/if}

			<!-- Step 3: Select Training -->
			{#if trainings.length > 0}
				<div class="bg-white rounded-lg shadow p-6">
					<h2 class="text-xl font-bold text-gray-900 mb-4">3. Select a Training Session</h2>
					<div class="space-y-4">
						{#each trainings as training}
							<button
								onclick={() => startTraining(training.id)}
								class="w-full p-6 rounded-lg border-2 border-gray-200 hover:border-blue-600 hover:bg-blue-50 text-left transition group"
							>
								<div class="flex justify-between items-start">
									<div>
										<h3 class="font-semibold text-gray-900 text-lg group-hover:text-blue-600">
											{training.name}
										</h3>
										<div class="flex items-center gap-4 mt-2 text-sm text-gray-600">
											<span>⏰ {formatTime(training.startTime)} - {formatTime(training.endTime)}</span>
											<span>💪 Intensity: {training.intensity}/3</span>
										</div>
									</div>
									<div class="text-blue-600 font-medium group-hover:translate-x-1 transition">
										Start →
									</div>
								</div>
							</button>
						{/each}
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>
