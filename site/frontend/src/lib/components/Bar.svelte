<script lang="ts">
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";
	import { page } from "$app/stores";

	export let data;
	export let x: string;
	export let y: string;

	let width = 913;
	let height = 525;
	const padding = { top: 20, right: 15, bottom: 20, left: 25 };

	const username = $page.url.searchParams.get("username");

	$: console.log(data);

	$: xMax = 100;
	$: yMax = max(data, (d) => +d[y])

	$: xTicks = [0, 25, 50, 75, 100]
	$: yTicks = Array.from({ length: Math.ceil(yMax / 5) + 1 }, (_, i) => i * 5);

	$: xScale = scaleLinear()
		.domain([0, data.length])
		.range([padding.left, width - padding.right]);

	$: yScale = scaleLinear()
		.domain([0, Math.max.apply(null, yTicks)])
		.range([height - padding.bottom, padding.top]);

	$: innerWidth = width - (padding.left + padding.right);
	$: barWidth = innerWidth / data.length;
</script>

<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
	<svg
		{width}
		{height}
		role="tooltip"
		viewBox="0 0 {width} {height}"
	>
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
						<rect
							class="fill-primary"
							rx="0.5rem"
							x={xScale(i) + barWidth / 2}
							y={yScale(point[y])}
							width={barWidth * 0.35}
							height={yScale(0) - yScale(point[y])}
						/>
			{/each}
		</g>
		<g class="axis x-axis">
			{#each data as point, i}
					<g class="tick" transform="translate({xScale(i)}, {height})">
						<text x={barWidth / 2}>
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
