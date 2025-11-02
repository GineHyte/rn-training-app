<script lang="ts">
	import { onMount } from 'svelte';
	import { title } from '$lib/stores/title';
	import { trainingService, type Training } from '$lib/services/trainingService';
	import { goto } from '$app/navigation';

	let trainings = $state<Training[]>([]);
	let loading = $state(true);
	let error = $state('');
	let currentDate = $state(new Date());
	let selectedDate = $state<Date | null>(null);

	// Calendar state
	let currentMonth = $derived(currentDate.getMonth());
	let currentYear = $derived(currentDate.getFullYear());

	onMount(async () => {
		title.setTitle('Training History');
		await loadTrainings();
	});

	async function loadTrainings() {
		loading = true;
		error = '';
		try {
			trainings = await trainingService.getAll();
		} catch (err: any) {
			error = err.response?.data?.detail || 'Failed to load training history';
		} finally {
			loading = false;
		}
	}

	function getDaysInMonth(year: number, month: number): number {
		return new Date(year, month + 1, 0).getDate();
	}

	function getFirstDayOfMonth(year: number, month: number): number {
		return new Date(year, month, 1).getDay();
	}

	function previousMonth() {
		currentDate = new Date(currentYear, currentMonth - 1, 1);
	}

	function nextMonth() {
		currentDate = new Date(currentYear, currentMonth + 1, 1);
	}

	function isToday(day: number): boolean {
		const today = new Date();
		return (
			day === today.getDate() &&
			currentMonth === today.getMonth() &&
			currentYear === today.getFullYear()
		);
	}

	function hasTrainingOnDate(day: number): boolean {
		const dateStr = new Date(currentYear, currentMonth, day).toDateString();
		return trainings.some((training) => {
			const trainingDate = new Date(training.startTime).toDateString();
			return trainingDate === dateStr;
		});
	}

	function getTrainingsForDate(day: number): Training[] {
		const dateStr = new Date(currentYear, currentMonth, day).toDateString();
		return trainings.filter((training) => {
			const trainingDate = new Date(training.startTime).toDateString();
			return trainingDate === dateStr;
		});
	}

	function selectDate(day: number) {
		selectedDate = new Date(currentYear, currentMonth, day);
	}

	let filteredTrainings = $derived(
		selectedDate
			? getTrainingsForDate(selectedDate.getDate())
			: trainings.filter((t) => t.endTime) // Show only completed trainings
	);

	const monthNames = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December'
	];

	const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

	function formatDuration(training: Training): string {
		if (!training.endTime) return 'In progress';
		const start = new Date(training.startTime);
		const end = new Date(training.endTime);
		const durationMs = end.getTime() - start.getTime();
		const minutes = Math.floor(durationMs / 60000);
		return `${minutes} min`;
	}
</script>

<div class="max-w-6xl mx-auto px-4 py-8">
	{#if error}
		<div class="rounded-md bg-red-50 p-4 mb-6">
			<p class="text-sm text-red-800">{error}</p>
		</div>
	{/if}

	{#if loading}
		<div class="text-center py-12">
			<p class="text-gray-500">Loading history...</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<!-- Calendar -->
			<div class="lg:col-span-2">
				<div class="bg-white rounded-lg shadow p-6">
					<!-- Calendar Header -->
					<div class="flex items-center justify-between mb-6">
						<button
							onclick={previousMonth}
							class="p-2 hover:bg-gray-100 rounded-full transition"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke-width="2"
								stroke="currentColor"
								class="w-6 h-6"
							>
								<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
							</svg>
						</button>
						<h2 class="text-xl font-bold text-gray-900">
							{monthNames[currentMonth]}
							{currentYear}
						</h2>
						<button
							onclick={nextMonth}
							class="p-2 hover:bg-gray-100 rounded-full transition"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke-width="2"
								stroke="currentColor"
								class="w-6 h-6"
							>
								<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
							</svg>
						</button>
					</div>

					<!-- Day names -->
					<div class="grid grid-cols-7 gap-2 mb-2">
						{#each dayNames as day}
							<div class="text-center text-sm font-medium text-gray-600 py-2">
								{day}
							</div>
						{/each}
					</div>

					<!-- Calendar days -->
					<div class="grid grid-cols-7 gap-2">
						{#each Array(getFirstDayOfMonth(currentYear, currentMonth)) as _}
							<div class="aspect-square"></div>
						{/each}

						{#each Array(getDaysInMonth(currentYear, currentMonth)) as _, i}
							{@const day = i + 1}
							{@const hasTraining = hasTrainingOnDate(day)}
							{@const selected =
								selectedDate?.getDate() === day &&
								selectedDate?.getMonth() === currentMonth &&
								selectedDate?.getFullYear() === currentYear}
							<button
								onclick={() => selectDate(day)}
								class={`aspect-square p-2 rounded-lg text-center transition relative ${
									isToday(day)
										? 'bg-blue-100 border-2 border-blue-500 font-bold'
										: selected
											? 'bg-blue-500 text-white font-semibold'
											: 'hover:bg-gray-100'
								}`}
							>
								<div>{day}</div>
								{#if hasTraining}
									<div class="absolute bottom-1 left-1/2 transform -translate-x-1/2">
										<div class="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
									</div>
								{/if}
							</button>
						{/each}
					</div>

					<div class="mt-4 flex items-center gap-4 text-sm text-gray-600">
						<div class="flex items-center gap-2">
							<div class="w-3 h-3 bg-blue-100 border-2 border-blue-500 rounded"></div>
							<span>Today</span>
						</div>
						<div class="flex items-center gap-2">
							<div class="w-3 h-3 bg-gray-100 rounded flex items-center justify-center">
								<div class="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
							</div>
							<span>Has training</span>
						</div>
					</div>
				</div>
			</div>

			<!-- Training List -->
			<div class="lg:col-span-1">
				<div class="bg-white rounded-lg shadow p-6">
					<h3 class="text-lg font-bold text-gray-900 mb-4">
						{selectedDate
							? `Trainings on ${selectedDate.toLocaleDateString()}`
							: 'Completed Trainings'}
					</h3>

					{#if filteredTrainings.length === 0}
						<p class="text-gray-500 text-sm">No trainings found</p>
					{:else}
						<div class="space-y-3">
							{#each filteredTrainings as training}
								<button
									onclick={() => goto(`/history/${training.id}`)}
									class="w-full border border-gray-200 rounded-lg p-4 hover:border-blue-500 hover:shadow-md transition text-left"
								>
									<div class="flex justify-between items-start mb-2">
										<div class="text-sm font-medium text-gray-900">
											{training.startTime ? new Date(training.startTime).toLocaleTimeString([], {
												hour: '2-digit',
												minute: '2-digit'
											}) : 'No time set'}
										</div>
										<span
											class={`text-xs px-2 py-1 rounded ${
												training.endTime
													? 'bg-green-100 text-green-800'
													: 'bg-yellow-100 text-yellow-800'
											}`}
										>
											{training.endTime ? 'Completed' : 'In Progress'}
										</span>
									</div>
									<div class="text-sm text-gray-600">{formatDuration(training)}</div>
									<div class="text-xs text-blue-600 mt-2">Click to view details →</div>
								</button>
							{/each}
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
