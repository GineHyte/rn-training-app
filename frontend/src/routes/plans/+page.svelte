<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';
	import { planService, type Plan } from '$lib/services/planService';

	let plans = $state<Plan[]>([]);
	let loading = $state(true);
	let error = $state('');

	onMount(async () => {
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

	async function deletePlan(id: number) {
		if (!confirm('Are you sure you want to delete this plan?')) return;
		
		try {
			await planService.delete(id);
			await loadPlans();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete plan';
		}
	}

	function createPlan() {
		goto('/plans/create');
	}

	function goToExercises() {
		goto('/exercises');
	}

	async function handleLogout() {
		await authStore.logout();
		goto('/login');
	}
</script>

<div class="min-h-screen bg-gray-50">
	<div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
		<div class="px-4 py-6 sm:px-0">
			<div class="flex justify-between items-center mb-6">
				<h2 class="text-2xl font-bold text-gray-900">My Plans</h2>
				<button
					onclick={createPlan}
					class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
				>
					Create Plan
				</button>
			</div>

			{#if error}
				<div class="rounded-md bg-red-50 p-4 mb-4">
					<p class="text-sm text-red-800">{error}</p>
				</div>
			{/if}

			{#if loading}
				<div class="text-center py-12">
					<p class="text-gray-500">Loading plans...</p>
				</div>
			{:else if plans.length === 0}
				<div class="text-center py-12 bg-white rounded-lg shadow">
					<p class="text-gray-500 mb-4">No plans yet. Create your first training plan!</p>
					<button
						onclick={createPlan}
						class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
					>
						Create Plan
					</button>
				</div>
			{:else}
				<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
					{#each plans as plan}
						<div class="bg-white overflow-hidden shadow rounded-lg">
							<div class="px-4 py-5 sm:p-6">
								<h3 class="text-lg font-medium text-gray-900 mb-2">{plan.name}</h3>
								<p class="text-sm text-gray-500 mb-2">
									Start Date: {plan.startDate ? new Date(plan.startDate).toLocaleDateString() : 'Not set'}
								</p>
								<p class="text-sm text-gray-500 mb-4">
									{plan.public ? 'Public' : 'Private'}
								</p>
								<div class="flex space-x-2">
									<button
										onclick={() => goto(`/plans/${plan.id}`)}
										class="flex-1 bg-indigo-600 text-white px-3 py-2 rounded text-sm hover:bg-indigo-700"
									>
										View
									</button>
									<button
										onclick={() => deletePlan(plan.id)}
										class="flex-1 bg-red-600 text-white px-3 py-2 rounded text-sm hover:bg-red-700"
									>
										Delete
									</button>
								</div>
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	</div>
</div>
