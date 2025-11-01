<script lang="ts">
	import { goto } from '$app/navigation';

	function startTraining() {
		goto('/start-training');
	}

	function goToHistory() {
		goto('/history');
	}

	function goToPlans() {
		goto('/plans');
	}

	function goToExercises() {
		goto('/exercises');
	}
</script>

<div class="flex flex-col items-center justify-center min-h-screen gap-8">
	<button
		onclick={startTraining}
		class="w-64 h-64 rounded-full bg-blue-600 hover:bg-blue-700 text-white font-bold text-2xl shadow-2xl transform transition-all duration-200 hover:scale-110"
	>
		Start Training
	</button>

	<div class="flex flex-col gap-4 w-full max-w-md px-4">
		<button
			onclick={goToHistory}
			class="w-full px-8 py-4 bg-gray-600 hover:bg-gray-700 text-white font-semibold rounded-lg shadow-lg transition-all duration-200 hover:scale-105"
		>
			History
		</button>

		<button
			onclick={goToPlans}
			class="w-full px-8 py-4 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg shadow-lg transition-all duration-200 hover:scale-105"
		>
			Plans
		</button>

		<button
			onclick={goToExercises}
			class="w-full px-8 py-4 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg shadow-lg transition-all duration-200 hover:scale-105"
		>
			Exercises
		</button>
	</div>
</div>
