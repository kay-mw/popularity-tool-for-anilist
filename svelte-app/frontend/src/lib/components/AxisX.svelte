<script>
	export let xmin;
	export let height;
	export let xScale;
	export let margin;

	$: xTicks = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
	//$: if (xmin > 0) {
	//	xTicks = Array.from(
	//		{ length: Math.ceil((100 - xmin) / 10) + 1 },
	//		(_, i) => Math.min(xmin + i * 10, 100),
	//	);
	//}
</script>

<g>
	{#each xTicks as tick}
		<text
			class="text-current fill-current"
			x={xScale(tick)}
			y={height - margin.bottom}
			dominant-baseline="hanging"
			dy="8"
			dx="-7"
			>{tick}</text
		>
	{/each}
</g>
