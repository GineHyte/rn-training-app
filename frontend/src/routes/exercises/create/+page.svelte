<script lang="ts">
	import { goto } from '$app/navigation';
	import { exerciseService } from '$lib/services/exerciseService';

	let name = $state('');
	let description = $state('');
	let video = $state('');
	let image = $state('');
	let isPublic = $state(false);
	let loading = $state(false);
	let error = $state('');

	async function handleSubmit() {
		if (!name) {
			error = 'Please enter an exercise name';
			return;
		}

		loading = true;
		error = '';
		
		try {
			await exerciseService.create({
				name,
				description: description || undefined,
				video: video || undefined,
				image: image || undefined,
				public: isPublic
			});
			goto('/exercises');
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to create exercise';
		} finally {
			loading = false;
		}
	}

	function goBack() {
		goto('/exercises');
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
					<h1 class="text-xl font-bold text-gray-900">Create Exercise</h1>
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
							Exercise Name *
						</label>
						<input
							id="name"
							type="text"
							required
							bind:value={name}
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
							placeholder="e.g., Bench Press"
						/>
					</div>

					<div class="mb-4">
						<label for="description" class="block text-sm font-medium text-gray-700 mb-2">
							Description
						</label>
						<textarea
							id="description"
							bind:value={description}
							rows="3"
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
							placeholder="Exercise description..."
						></textarea>
					</div>

					<div class="mb-4">
						<label for="video" class="block text-sm font-medium text-gray-700 mb-2">
							Video URL
						</label>
						<input
							id="video"
							type="url"
							bind:value={video}
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
							placeholder="https://..."
						/>
					</div>

					<div class="mb-4">
						<label for="image" class="block text-sm font-medium text-gray-700 mb-2">
							Image URL
						</label>
						<input
							id="image"
							type="url"
							bind:value={image}
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
							placeholder="https://..."
						/>
					</div>

					<div class="mb-6">
						<label class="flex items-center">
							<input
								type="checkbox"
								bind:checked={isPublic}
								class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
							/>
							<span class="ml-2 text-sm text-gray-700">Make this exercise public</span>
						</label>
					</div>

					<div class="flex space-x-4">
						<button
							type="submit"
							disabled={loading}
							class="flex-1 bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
						>
							{loading ? 'Creating...' : 'Create Exercise'}
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
