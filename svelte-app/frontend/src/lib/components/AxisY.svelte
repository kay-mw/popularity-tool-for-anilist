<script>
	export let ymax;
	export let width;
	export let yScale;
	export let margin;

	$: yTicks = Array.from(
		{ length: Math.ceil(ymax / 5) + 1 },
		(_, i) => i * 5,
	);
</script>

<g transform="translate({margin.left} {margin.top})">
	{#each yTicks as tick}
		<text
			class="text-current fill-current"
			x={0}
			dy="-6"
			y={yScale(tick)}>{tick}</text
		>
		<line
			x1="0"
			x2={width}
			y1={yScale(tick)}
			y2={yScale(tick)}
			class="stroke-border"
		/>
	{/each}
</g>
