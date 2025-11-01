<script lang="ts">
	interface Exercise {
		name: string;
		description?: string;
		image?: string;
		video?: string;
	}

	interface Props {
		isOpen: boolean;
		exercise: Exercise | null;
		onClose: () => void;
	}

	let { isOpen, exercise, onClose }: Props = $props();
</script>

{#if isOpen && exercise}
	<div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
		<div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
			<div class="flex justify-between items-start mb-4">
				<h3 class="text-2xl font-bold text-gray-900">{exercise.name}</h3>
				<button
					onclick={onClose}
					class="text-gray-400 hover:text-gray-600 text-2xl"
				>
					×
				</button>
			</div>

			{#if exercise.image}
				<div class="mb-4">
					<img
						src={exercise.image}
						alt={exercise.name}
						class="w-full rounded-lg shadow-md"
					/>
				</div>
			{/if}

			{#if exercise.description}
				<div class="mb-4">
					<h4 class="text-lg font-semibold text-gray-900 mb-2">Description</h4>
					<p class="text-gray-700 whitespace-pre-wrap">{exercise.description}</p>
				</div>
			{/if}

			{#if exercise.video}
				<div class="mb-4">
					<h4 class="text-lg font-semibold text-gray-900 mb-2">Video</h4>
					{#if exercise.video.includes('youtube.com') || exercise.video.includes('youtu.be')}
						<div class="aspect-video">
							<iframe
								src={exercise.video.replace('watch?v=', 'embed/')}
								title={exercise.name}
								class="w-full h-full rounded-lg"
								frameborder="0"
								allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
								allowfullscreen
							></iframe>
						</div>
					{:else}
						<a
							href={exercise.video}
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
					onclick={onClose}
					class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
				>
					Close
				</button>
			</div>
		</div>
	</div>
{/if}
