<script lang="ts">
	// Reduce gap between bars to make it look more like obscurify ;)
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";
	import { page } from "$app/stores";

	export let data;
	export let x: string;
	export let y: string;
	export let scoreVariable: number;

	let width = 500;
	let height = 400;
	const padding = { top: 20, right: 15, bottom: 20, left: 25 };

	const username = $page.url.searchParams.get("username");

	//$: console.log(data);

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

	$: console.log(Math.round(scoreVariable * 5) / 5);
	$: console.log(data)
</script>

<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
	<svg {width} {height} role="tooltip" viewBox="0 0 {width} {height}">
		<g class="axis y-axis">
			{#each yTicks as tick}
				<g class="tick tick-{tick}" transform="translate(0, {yScale(tick)})">
					<line x2="100%" />
					<text y="-4">{tick}</text>
				</g>
			{/each}
		</g>
		<g class="bars">
			{#each data as point, i}
				{#if Math.round(scoreVariable * 5) / 5 == point[x]}
					<rect
						class="fill-primary"
						rx="0.5rem"
						x={xScale(i)}
						y={yScale(point[y])}
						width={barWidth * 0.4}
						height={yScale(0) - yScale(point[y])}
					/>
					<text
					class="fill-primary font-bold text-xl"
					style="text-anchor: middle;"
					x={xScale(i) + 15}
					y={yScale(point[y]) - 20}
					>{username}</text>
				{:else}
					<rect
						class="fill-plot-accent"
						rx="0.5rem"
						x={xScale(i)}
						y={yScale(point[y])}
						width={barWidth * 0.4}
						height={yScale(0) - yScale(point[y])}
					/>
				{/if}
			{/each}
		</g>
		<g class="axis x-axis">
			{#each data as point, i}
				<g class="tick" transform="translate({xScale(i)}, {height})">
					<text x={barWidth / 5}>
						{point[x]}
					</text>
				</g>
			{/each}
		</g>
	</svg>
</div>

<style lang="postcss">
	.x-axis .tick text {
		@apply text-center text-current;
		text-anchor: middle;
	}

	.bars rect {
		transition: opacity 0.2s ease-in-out;
	}

	.bars g.dimmed rect {
		opacity: 0.3;
	}

	.bars g.hovered rect {
		opacity: 1;
	}

	.x-axis text {
		transition: opacity 0.2s ease-in-out;
	}

	.x-axis g.dimmed text {
		opacity: 0.3;
	}

	.x-axis g.hovered text {
		opacity: 1;
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

	.tooltip {
		@apply absolute bg-background border border-secondary font-semibold p-2 rounded shadow-lg text-base;
		pointer-events: none;
		z-index: 100;
		transition: opacity 0.2s ease-in-out;
	}
</style>
