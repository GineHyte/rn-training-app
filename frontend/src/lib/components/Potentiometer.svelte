<script lang="ts">
	interface Props {
		value: number;
		min?: number;
		max?: number;
		step?: number;
		label?: string;
		unit?: string;
		color?: string;
		onchange?: (value: number) => void;
	}

	let {
		value = $bindable(0),
		min = 0,
		max = 100,
		step = 1,
		label = '',
		unit = '',
		color = '#3b82f6',
		onchange = () => {}
	}: Props = $props();

	let isDragging = $state(false);
	let knobRef = $state<SVGSVGElement>();

	const radius = 70;
	const strokeWidth = 15;
	const center = 100;
	const circumference = 2 * Math.PI * radius;

	// Calculate angle based on value (270 degrees rotation, -135 to +135)
	let angle = $derived(((value - min) / (max - min)) * 270 - 135);
	let progress = $derived(((value - min) / (max - min)) * 100);

	function handleMouseDown(e: MouseEvent) {
		isDragging = true;
		updateValue(e);
	}

	function handleMouseMove(e: MouseEvent) {
		if (isDragging) {
			updateValue(e);
		}
	}

	function handleMouseUp() {
		isDragging = false;
	}

	function handleTouchStart(e: TouchEvent) {
		isDragging = true;
		updateValueFromTouch(e);
	}

	function handleTouchMove(e: TouchEvent) {
		if (isDragging) {
			updateValueFromTouch(e);
		}
	}

	function handleTouchEnd() {
		isDragging = false;
	}

	function updateValue(e: MouseEvent) {
		if (!knobRef) return;

		const rect = knobRef.getBoundingClientRect();
		const centerX = rect.left + rect.width / 2;
		const centerY = rect.top + rect.height / 2;
		
		const deltaX = e.clientX - centerX;
		const deltaY = e.clientY - centerY;
		
		let angleRad = Math.atan2(deltaY, deltaX);
		let angleDeg = angleRad * (180 / Math.PI);
		
		// Convert to 0-270 range starting from bottom (-135 to +135)
		angleDeg = angleDeg + 135;
		if (angleDeg < 0) angleDeg += 360;
		if (angleDeg > 270) {
			// Clamp to nearest edge
			angleDeg = Math.abs(angleDeg - 360) < 45 ? 0 : 270;
		}
		
		const newValue = min + (angleDeg / 270) * (max - min);
		const steppedValue = Math.round(newValue / step) * step;
		value = Math.max(min, Math.min(max, steppedValue));
		onchange(value);
	}

	function updateValueFromTouch(e: TouchEvent) {
		if (!knobRef || e.touches.length === 0) return;
		
		const touch = e.touches[0];
		const rect = knobRef.getBoundingClientRect();
		const centerX = rect.left + rect.width / 2;
		const centerY = rect.top + rect.height / 2;
		
		const deltaX = touch.clientX - centerX;
		const deltaY = touch.clientY - centerY;
		
		let angleRad = Math.atan2(deltaY, deltaX);
		let angleDeg = angleRad * (180 / Math.PI);
		
		angleDeg = angleDeg + 135;
		if (angleDeg < 0) angleDeg += 360;
		if (angleDeg > 270) {
			angleDeg = Math.abs(angleDeg - 360) < 45 ? 0 : 270;
		}
		
		const newValue = min + (angleDeg / 270) * (max - min);
		const steppedValue = Math.round(newValue / step) * step;
		value = Math.max(min, Math.min(max, steppedValue));
		onchange(value);
	}

	$effect(() => {
		if (typeof window !== 'undefined') {
			document.addEventListener('mousemove', handleMouseMove);
			document.addEventListener('mouseup', handleMouseUp);
			document.addEventListener('touchmove', handleTouchMove);
			document.addEventListener('touchend', handleTouchEnd);

			return () => {
				document.removeEventListener('mousemove', handleMouseMove);
				document.removeEventListener('mouseup', handleMouseUp);
				document.removeEventListener('touchmove', handleTouchMove);
				document.removeEventListener('touchend', handleTouchEnd);
			};
		}
	});
</script>

<div class="flex flex-col items-center">
	<div class="text-sm font-medium text-gray-700 mb-2">{label}</div>
	
	<svg
		bind:this={knobRef}
		width="200"
		height="200"
		viewBox="0 0 200 200"
		class="cursor-pointer select-none"
		onmousedown={handleMouseDown}
		ontouchstart={handleTouchStart}
		role="slider"
		aria-label={label}
		aria-valuemin={min}
		aria-valuemax={max}
		aria-valuenow={value}
	>
		<!-- Background circle -->
		<circle
			cx={center}
			cy={center}
			r={radius}
			fill="none"
			stroke="#e5e7eb"
			stroke-width={strokeWidth}
			stroke-linecap="round"
			transform="rotate(-135 {center} {center})"
			stroke-dasharray="{circumference * 0.75} {circumference}"
		/>
		
		<!-- Progress arc -->
		<circle
			cx={center}
			cy={center}
			r={radius}
			fill="none"
			stroke={color}
			stroke-width={strokeWidth}
			stroke-linecap="round"
			transform="rotate(-135 {center} {center})"
			stroke-dasharray="{(circumference * 0.75 * progress) / 100} {circumference}"
			style="transition: stroke-dasharray 0.1s ease"
		/>
		
		<!-- Center circle -->
		<circle cx={center} cy={center} r="50" fill="white" stroke={color} stroke-width="2" />
		
		<!-- Value text -->
		<text
			x={center}
			y={center}
			text-anchor="middle"
			dominant-baseline="middle"
			class="text-3xl font-bold"
			fill="#1f2937"
		>
			{value}
		</text>
		
		{#if unit}
			<text
				x={center}
				y={center + 25}
				text-anchor="middle"
				dominant-baseline="middle"
				class="text-sm"
				fill="#6b7280"
			>
				{unit}
			</text>
		{/if}
	</svg>
	
	<div class="flex justify-between w-full max-w-[180px] mt-2 text-xs text-gray-500">
		<span>{min}</span>
		<span>{max}</span>
	</div>
</div>

<style>
	svg {
		user-select: none;
		-webkit-user-select: none;
		touch-action: none;
	}
</style>
