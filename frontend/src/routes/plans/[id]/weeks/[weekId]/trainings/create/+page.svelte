<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { planTrainingService } from '$lib/services/planTrainingService';

	let planId = parseInt($page.params.id || '0');
	let weekId = parseInt($page.params.weekId || '0');
	
	let name = $state('');
	let startTime = $state('');
	let endTime = $state('');
	let intensity = $state(5);
	let loading = $state(false);
	let error = $state('');

	async function handleSubmit() {
		if (!name || !startTime || !endTime) {
			error = 'Please fill in all required fields';
			return;
		}

		if (intensity < 1 || intensity > 10) {
			error = 'Intensity must be between 1 and 10';
			return;
		}

		loading = true;
		error = '';
		
		try {
			// Create full datetime by combining date with time
			const today = new Date().toISOString().split('T')[0];
			await planTrainingService.create({
				planWeekId: weekId,
				name,
				startTime: `${today}T${startTime}:00`,
				endTime: `${today}T${endTime}:00`,
				intensity
			});
			goto(`/plans/${planId}`);
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to create training';
		} finally {
			loading = false;
		}
	}

	function goBack() {
		goto(`/plans/${planId}`);
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
					<h1 class="text-xl font-bold text-gray-900">Add Training</h1>
				</div>
			</div>
		</div>
	</nav>

	<div class="max-w-2xl mx-auto py-6 sm:px-6 lg:px-8">
		<div class="px-4 py-6 sm:px-0">
			<div class="bg-white shadow rounded-lg p-6">
				<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
					{#if error}
						<div class="rounded-md bg-red-50 p-4 mb-4">
							<p class="text-sm text-red-800">{error}</p>
						</div>
					{/if}

					<div class="mb-4">
						<label for="name" class="block text-sm font-medium text-gray-700 mb-2">
							Training Name *
						</label>
						<input
							id="name"
							type="text"
							required
							bind:value={name}
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
							placeholder="e.g., Chest & Triceps"
						/>
					</div>

					<div class="grid grid-cols-2 gap-4 mb-4">
						<div>
							<label for="startTime" class="block text-sm font-medium text-gray-700 mb-2">
								Start Time *
							</label>
							<input
								id="startTime"
								type="time"
								required
								bind:value={startTime}
								class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
							/>
						</div>
						<div>
							<label for="endTime" class="block text-sm font-medium text-gray-700 mb-2">
								End Time *
							</label>
							<input
								id="endTime"
								type="time"
								required
								bind:value={endTime}
								class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
							/>
						</div>
					</div>

					<div class="mb-6">
						<label for="intensity" class="block text-sm font-medium text-gray-700 mb-2">
							Intensity: {intensity}/10
						</label>
						<input
							id="intensity"
							type="range"
							min="1"
							max="10"
							bind:value={intensity}
							class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
						/>
						<div class="flex justify-between text-xs text-gray-500 mt-1">
							<span>Light</span>
							<span>Moderate</span>
							<span>Intense</span>
						</div>
					</div>

					<div class="flex space-x-4">
						<button
							type="submit"
							disabled={loading}
							class="flex-1 bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
						>
							{loading ? 'Creating...' : 'Create Training'}
						</button>
						<button
							type="button"
							onclick={goBack}
							class="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
						>
							Cancel
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</div>
