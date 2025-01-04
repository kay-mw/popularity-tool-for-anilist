<script lang="ts">
	import { max, min } from "d3-array";
	import { scaleLinear } from "d3-scale";

	export let data: Array<Record<string, number>>;
	export let x: string;
	export let y: string;
	export let scoreVariable: number;

	scoreVariable = Math.round(scoreVariable);

	let width = 300;
	let height = 400;

	const padding = { top: 0, bottom: 65, left: 55, right: 0 };

	$: xMax = max(data, (d) => +d[x]);
	$: xMin = min(data, (d) => +d[x]);

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

	//NOTE: Currently, this percentile calculation works well for more positive scores. 
	//But what if someone's scores are more negative? They also want to know what % of people they are more negative than.
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
					class="{scoreVariable == point[x]
						? 'opacity-100 fill-primary'
						: 'opacity-30'} {point[x] >= 0
						? 'fill-plot-accent'
						: 'fill-destructive'}"
					rx="0.5em"
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
						y={height - 20}
						>&gt;{percentile}% of Users
					</text>
				{/if}
			{/each}
		</g>
		<g class="axis x-axis">
			{#each data as point, i}
				<g class="tick" transform="translate({xScale(i)}, {height - 40})">
					<text x={barWidth * 0.2} y="-5">
						{point[x]}
					</text>
				</g>
			{/each}
			<g class="tick" transform="translate({width / 2}, {height})">
				<text>Positive →</text>
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
