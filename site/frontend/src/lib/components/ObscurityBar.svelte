<script lang="ts">
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";

	let {
		data,
		x,
		y,
		scoreVariable,
		colorY1,
		colorY2,
		xLabel,
		yLabel,
		username,
	}: {
		data: Array<Record<string, number>>;
		x: string;
		y: string;
		scoreVariable: number;
		colorY1: string;
		colorY2: string;
		xLabel: string;
		yLabel: string;
		username: string;
	} = $props();

	let width = $state(800);
	let height = $state(400);
	const padding = { top: 20, bottom: 40, left: 130, right: 0 };

	let yMax = $derived(max(data, (d) => +d[y]));

	let yTicks = $derived(
		Array.from({ length: Math.ceil(yMax / 100000) + 1 }, (_, i) => i * 100000),
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

	const barRadius = "0.5em";

	let hovering = $state(false);
	function handleEnter() {
		hovering = true;
	}
	function handleLeave() {
		hovering = false;
	}

	let percentiles = [];
	for (let i = 0; i < data.length; i++) {
		let pct = Math.round((i / data.length) * 100);
		percentiles.push(pct);
	}

	let i = 0;
	let percentile = $state(0);
	while (data[i] && data[i][y] > scoreVariable) {
		i++;
		percentile = Math.round((i / data.length) * 100);
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
				transform="translate({10}, {(height - padding.bottom) / 2}) rotate(-90)"
			>
				<text style="text-anchor: middle;">{yLabel} →</text>
			</g>
		</g>
		<g class="bars">
			{#each data as point, i}
				<rect
					class="{scoreVariable == point[y]
						? colorY1
						: colorY2} {scoreVariable != point[y] && hovering
						? 'opacity-30'
						: 'opacity-100'}"
					rx={barRadius}
					x={xScale(i)}
					y={yScale(point[y])}
					width={barWidth * 0.4}
					height={yScale(0) - yScale(point[y])}
				/>
				{#if scoreVariable == point[y]}
					<text
						class="fill-primary font-bold text-sm md:text-lg"
						style="text-anchor: middle;"
						x={xScale(i) + 18}
						y={yScale(point[y]) - 10}
						>{username}
					</text>
				{/if}
			{/each}
		</g>
		<g class="axis x-axis">
			{#each percentiles as pct, i}
				<g
					class="tick"
					style="text-anchor: middle;"
					transform="translate({xScale(i)}, {height - 30})"
				>
					<text x="21" y="5">
						{pct}%
					</text>
				</g>
			{/each}
			<g
				class="tick"
				transform="translate({(width + padding.left / 2 + 10) / 2}, {height -
					1})"
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
