<script lang="ts">
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";

	let {
		data,
		x,
		y,
		scoreVariable,
		colorX1,
		colorX2,
		xLabel,
		diverging,
	}: {
		data: Array<Record<string, number>>;
		x: string;
		y: string;
		scoreVariable: number;
		colorX1: string;
		colorX2: string;
		xLabel: string;
		diverging: boolean;
	} = $props();

	scoreVariable = Math.round(scoreVariable);

	let width = $state(800);
	let height = $state(400);
	const padding = { top: 20, bottom: 65, left: 65, right: 0 };

	let yMax = $derived(max(data, (d) => +d[y]));

	let yTicks = $derived(
		Array.from({ length: Math.ceil(yMax / 5) + 1 }, (_, i) => i * 5),
	);

	let xScale = $derived(
		scaleLinear()
			.domain([0, data.length])
			.range([padding.left, width - padding.right]),
	);

	let yScale = $derived(
		scaleLinear()
			.domain([0, Math.max.apply(null, yTicks)])
			.range([height - padding.bottom, padding.top]),
	);

	let innerWidth = $derived(width - (padding.left + padding.right));
	let barWidth = $derived(innerWidth / data.length);

	let i = 0;
	let percentile = $state(0);
	let pct = 0;
	const sum = data.reduce((sm, d) => sm + +d[y], 0);
	while (data[i] && data[i][x] < scoreVariable) {
		pct = Math.round((data[i][y] / sum) * 100);
		percentile += pct;
		i++;
	}
	percentile = scoreVariable > 0 ? percentile : 100 - percentile;

	const barRadius = "0.5em";

	let hovering = $state(false);
	function handleEnter() {
		hovering = true;
	}
	function handleLeave() {
		hovering = false;
	}

	let direction = $state("");
	if (diverging) {
		direction = scoreVariable >= 0 ? "Positivity" : "Negativity";
	}
</script>

<div bind:clientWidth={width} bind:clientHeight={height}>
	<svg
		{width}
		{height}
		viewBox="0 0 {width} {height}"
		onmouseenter={handleEnter}
		onmouseleave={handleLeave}
		role="presentation"
	>
		<g class="axis y-axis">
			{#each yTicks as tick}
				<g class="tick tick-{tick}" transform="translate(25, {yScale(tick)})">
					<line x2="100%" />
					<text y="-4">{tick}</text>
				</g>
			{/each}
			<g
				class="tick"
				transform="translate({10}, {(height - padding.bottom + padding.top) /
					2}) rotate(-90)"
			>
				<text style="text-anchor: middle;">% of Users →</text>
			</g>
		</g>
		<g class="bars">
			{#each data as point, i}
				<rect
					class="{scoreVariable == point[x] && !diverging
						? `${colorX1}`
						: `${colorX2}`} 
					{scoreVariable != point[x] && hovering ? 'opacity-30' : 'opacity-100'} 
					{diverging && point[x] >= 0 && point[x] != scoreVariable
						? `${colorX1}`
						: `${colorX2}`} 
					{diverging && point[x] == scoreVariable ? 'fill-primary' : ''}"
					rx={barRadius}
					x={xScale(i)}
					y={yScale(point[y])}
					width={barWidth * 0.4}
					height={yScale(0) - yScale(point[y])}
				/>
				{#if scoreVariable == point[x]}
					<text
						class="fill-primary font-bold text-sm md:text-lg"
						style="text-anchor: middle;"
						x={xScale(i) + barWidth * 0.2}
						y={height - 22}
						>{direction} &gt;{percentile}% of Users
					</text>
				{/if}
			{/each}
		</g>
		<g class="axis x-axis">
			{#each data as point, i}
				<g class="text-xs fill-current font-semibold" style="text-anchor: middle;" transform="translate({xScale(i)}, {height - 55})">
					<text x={diverging ? "5" : "6.5"} y="5">
						{point[x]}
					</text>
				</g>
			{/each}
			<g
				class="tick"
				transform="translate({(width + padding.left - padding.right) /
					2}, {height - 5})"
			>
				<text>{xLabel} →</text>
			</g>
		</g>
	</svg>
</div>

<style lang="postcss">
	.x-axis .tick text {
		@apply text-center text-current;
		text-anchor: middle;
	}

	.tick {
		@apply text-sm text-current;
	}

	.tick text {
		@apply fill-current text-current font-semibold;
		text-anchor: start;
	}

	.tick line {
		@apply stroke-secondary opacity-100;
	}

	.tick.tick-0 line {
		@apply inline-block;
	}

	.bars rect {
		transition: opacity 0.5s ease-in-out;
	}
</style>
