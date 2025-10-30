<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { exerciseService, type Exercise } from '$lib/services/exerciseService';

	let exerciseId = parseInt($page.params.id || '0');
	let exercise = $state<Exercise | null>(null);
	let loading = $state(true);
	let error = $state('');

	onMount(async () => {
		await loadExercise();
	});

	async function loadExercise() {
		loading = true;
		error = '';
		try {
			exercise = await exerciseService.getById(exerciseId);
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load exercise';
		} finally {
			loading = false;
		}
	}

	function goBack() {
		goto('/exercises');
	}

	async function handleDelete() {
		if (!confirm('Are you sure you want to delete this exercise?')) return;
		
		try {
			await exerciseService.delete(exerciseId);
			goto('/exercises');
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to delete exercise';
		}
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
						← Back to Exercises
					</button>
					<h1 class="text-xl font-bold text-gray-900">
						{exercise?.name || 'Exercise Details'}
					</h1>
				</div>
			</div>
		</div>
	</nav>

	<div class="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
		<div class="px-4 py-6 sm:px-0">
			{#if error}
				<div class="rounded-md bg-red-50 p-4 mb-4">
					<p class="text-sm text-red-800">{error}</p>
				</div>
			{/if}

			{#if loading}
				<div class="text-center py-12">
					<p class="text-gray-500">Loading exercise...</p>
				</div>
			{:else if exercise}
				<div class="bg-white shadow rounded-lg overflow-hidden">
					{#if exercise.image}
						<img src={exercise.image} alt={exercise.name} class="w-full h-64 object-cover" />
					{/if}
					
					<div class="p-6">
						<div class="flex justify-between items-start mb-4">
							<div>
								<h2 class="text-3xl font-bold text-gray-900 mb-2">{exercise.name}</h2>
								<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium {exercise.public ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}">
									{exercise.public ? 'Public' : 'Private'}
								</span>
							</div>
							<button
								onclick={handleDelete}
								class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
							>
								Delete Exercise
							</button>
						</div>

						{#if exercise.description}
							<div class="mb-6">
								<h3 class="text-lg font-medium text-gray-900 mb-2">Description</h3>
								<p class="text-gray-700 whitespace-pre-wrap">{exercise.description}</p>
							</div>
						{/if}

						{#if exercise.video}
							<div class="mb-6">
								<h3 class="text-lg font-medium text-gray-900 mb-2">Video</h3>
								<a 
									href={exercise.video} 
									target="_blank" 
									rel="noopener noreferrer"
									class="text-indigo-600 hover:text-indigo-800 underline"
								>
									Watch video →
								</a>
							</div>
						{/if}

						<div class="border-t border-gray-200 pt-4">
							<div class="grid grid-cols-2 gap-4 text-sm">
								<div>
									<span class="text-gray-500">Created:</span>
									<span class="ml-2 font-medium">{new Date(exercise.createdAt).toLocaleDateString()}</span>
								</div>
								<div>
									<span class="text-gray-500">Updated:</span>
									<span class="ml-2 font-medium">{new Date(exercise.updatedAt).toLocaleDateString()}</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>
