<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { planService, type Plan } from '$lib/services/planService';
	import { planWeekService, type PlanWeek } from '$lib/services/planWeekService';
	import { planTrainingService, type PlanTraining } from '$lib/services/planTrainingService';

	const planId = $derived(parseInt($page.params.id));
	let plan = $state<Plan | null>(null);
	let weeks = $state<PlanWeek[]>([]);
	let weekTrainings = $state<Map<number, PlanTraining[]>>(new Map());
	let loading = $state(true);
	let error = $state('');
	let showAddWeek = $state(false);
	let newWeekDate = $state('');

	onMount(async () => {
		await loadPlan();
	});

	async function loadPlan() {
		loading = true;
		error = '';
		try {
			const planData = await planService.getById(planId);
			plan = planData;
			const weeksData = await planWeekService.getByPlan(planId);
			weeks = weeksData;
			
			// Load trainings for each week
			const trainingsMap = new Map<number, PlanTraining[]>();
			for (const week of weeksData) {
				const trainings = await planTrainingService.getByWeek(week.id);
				trainingsMap.set(week.id, trainings);
			}
			weekTrainings = trainingsMap;
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load plan';
		} finally {
			loading = false;
		}
	}

	async function addWeek() {
		if (!newWeekDate) {
			error = 'Please select a date';
			return;
		}

		try {
			await planWeekService.create({
				planId,
				startDate: new Date(newWeekDate).toISOString()
			});
			showAddWeek = false;
			newWeekDate = '';
			await loadPlan();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to add week';
		}
	}

	async function deleteWeek(weekId: number) {
		if (!confirm('Are you sure? This will delete all trainings in this week.')) return;
		
		try {
			await planWeekService.delete(weekId);
			await loadPlan();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete week';
		}
	}

	function goBack() {
		goto('/plans');
	}

	function viewTraining(trainingId: number) {
		goto(`/trainings/${trainingId}`);
	}

	function addTrainingToWeek(weekId: number) {
		goto(`/plans/${planId}/weeks/${weekId}/trainings/create`);
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
						← Back to Plans
					</button>
					<h1 class="text-xl font-bold text-gray-900">
						{plan?.name || 'Plan Details'}
					</h1>
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

			{#if loading}
				<div class="text-center py-12">
					<p class="text-gray-500">Loading plan...</p>
				</div>
			{:else if plan}
				<div class="bg-white shadow rounded-lg p-6 mb-6">
					<h2 class="text-2xl font-bold text-gray-900 mb-4">{plan.name}</h2>
					<div class="grid grid-cols-2 gap-4 text-sm">
						<div>
							<span class="text-gray-500">Start Date:</span>
							<span class="ml-2 font-medium">{new Date(plan.startDate).toLocaleDateString()}</span>
						</div>
						<div>
							<span class="text-gray-500">Visibility:</span>
							<span class="ml-2 font-medium">{plan.public ? 'Public' : 'Private'}</span>
						</div>
					</div>
				</div>

				<div class="flex justify-between items-center mb-6">
					<h3 class="text-xl font-bold text-gray-900">Weeks & Trainings</h3>
					<button
						onclick={() => showAddWeek = true}
						class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
					>
						Add Week
					</button>
				</div>

				{#if showAddWeek}
					<div class="bg-white shadow rounded-lg p-6 mb-6">
						<h4 class="text-lg font-medium mb-4">Add New Week</h4>
						<div class="flex gap-4">
							<input
								type="date"
								bind:value={newWeekDate}
								class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
							/>
							<button
								onclick={addWeek}
								class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
							>
								Add
							</button>
							<button
								onclick={() => { showAddWeek = false; newWeekDate = ''; }}
								class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
							>
								Cancel
							</button>
						</div>
					</div>
				{/if}

				{#if weeks.length === 0}
					<div class="text-center py-12 bg-white rounded-lg shadow">
						<p class="text-gray-500 mb-4">No weeks yet. Add your first week!</p>
					</div>
				{:else}
					<div class="space-y-6">
						{#each weeks.sort((a, b) => new Date(a.startDate).getTime() - new Date(b.startDate).getTime()) as week, index}
							<div class="bg-white shadow rounded-lg p-6">
								<div class="flex justify-between items-center mb-4">
									<div>
										<h4 class="text-lg font-medium text-gray-900">Week {index + 1}</h4>
										<p class="text-sm text-gray-500">
											Starts: {new Date(week.startDate).toLocaleDateString()}
										</p>
									</div>
									<div class="flex gap-2">
										<button
											onclick={() => addTrainingToWeek(week.id)}
											class="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
										>
											Add Training
										</button>
										<button
											onclick={() => deleteWeek(week.id)}
											class="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
										>
											Delete Week
										</button>
									</div>
								</div>

								{#if weekTrainings.get(week.id)?.length === 0}
									<p class="text-sm text-gray-500">No trainings scheduled for this week.</p>
								{:else}
									<div class="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
										{#each weekTrainings.get(week.id) || [] as training}
											<div class="border border-gray-200 rounded-lg p-4 hover:border-indigo-500 cursor-pointer"
												onclick={() => viewTraining(training.id)}
											>
												<h5 class="font-medium text-gray-900 mb-2">{training.name}</h5>
												<div class="text-sm text-gray-500 space-y-1">
													<p>🕐 {new Date(training.startTime).toLocaleTimeString()} - {new Date(training.endTime).toLocaleTimeString()}</p>
													<p>💪 Intensity: {training.intensity}/10</p>
												</div>
											</div>
										{/each}
									</div>
								{/if}
							</div>
						{/each}
					</div>
				{/if}
			{/if}
		</div>
	</div>
</div>
