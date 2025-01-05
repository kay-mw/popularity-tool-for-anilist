<script lang="ts">
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";
	import { page } from "$app/stores";

	export let data: Array<Record<string, number>>;
	export let x: string;
	export let y: string;
	export let scoreVariable: number;

	scoreVariable = Math.round(scoreVariable);

	let width = 300;
	let height = 400;
	const padding = { top: 20, bottom: 55, left: 65, right: 0 };

	const username = $page.url.searchParams.get("username");

	$: yMax = max(data, (d) => +d[y]);

	$: yTicks = Array.from({ length: Math.ceil(yMax / 5) + 1 }, (_, i) => i * 5);

	$: xScale = scaleLinear()
		.domain([0, data.length])
		.range([padding.left, width - padding.right]);

	$: yScale = scaleLinear()
		.domain([0, Math.max.apply(null, yTicks)])
		.range([height - padding.bottom, padding.top]);

	$: innerWidth = width - (padding.left + padding.right);
	$: barWidth = innerWidth / data.length;

	let i = 0;
	let percentile = 0;
	let pct = 0;
	const sum = data.reduce((sm, d) => sm + +d[y], 0);
	while (data[i] && data[i][x] < scoreVariable) {
		pct = Math.round((data[i][y] / sum) * 100);
		percentile += pct;
		i++;
	}

	const barRadius = "0.5em";
</script>

<div class="relative" bind:clientWidth={width} bind:clientHeight={height}>
	<svg {width} {height} viewBox="0 0 {width} {height}">
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
					class={scoreVariable == point[x]
						? "fill-primary opacity-100"
						: "fill-plot-accent opacity-30"}
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
						y={height - 35}
						>&gt;{percentile}% of Users
					</text>
				{/if}
			{/each}
		</g>
		<g class="axis x-axis">
			<g
				class="tick"
				transform="translate({(padding.left + width - 25) / 2}, {height - 10})"
			>
				<text>Controversial →</text>
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
</style>
