<script lang="ts">
	import type { PlanTraining } from '$lib/services/planTrainingService';

	interface Props {
		planTraining: PlanTraining;
	}

	let { planTraining }: Props = $props();
</script>

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
