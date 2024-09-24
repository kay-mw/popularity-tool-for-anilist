<script lang="ts">
	import { min, max } from "d3-array";
	import { scaleLinear } from "d3-scale";
	import { spring } from "svelte/motion";
	import { page } from "$app/stores";

	export let data;

	const padding = { top: 40, right: 40, bottom: 0, left: 150 };
	const username = $page.url.searchParams.get("username");

	let width = 800;
	let height = 1000;

	$: xMin =
		Math.ceil(
			Math.min(
				min(data.insights.genreData, (d) => +d.weighted_average),
				min(data.insights.genreData, (d) => +d.weighted_user),
			),
		) - 5;

	$: xMax = Math.ceil(
		Math.max(
			max(data.insights.genreData, (d) => +d.weighted_average),
			max(data.insights.genreData, (d) => +d.weighted_user),
		),
	);

	function range(low: number, hi: number, increment: number) {
		function rangeRec(low: number, hi: number, vals: Array<number>) {
			if (low > hi) return vals;
			vals.push(low);
			return rangeRec(low + increment, hi, vals);
		}
		return rangeRec(low, hi, []);
	}
	$: xTicks = range(xMin, xMax, 1);

	$: xScale = scaleLinear()
		.domain([Math.min.apply(null, xTicks), Math.max.apply(null, xTicks)])
		.range([padding.left, width - padding.right]);

	$: yScale = scaleLinear()
		.domain([0, data.insights.genreData.length])
		.range([padding.top, height - padding.bottom]);

	$: innerWidth = width - (padding.left + padding.right);
	$: barWidth = innerWidth / data.insights.genreData.length;
	$: innerHeight = height - (padding.top + padding.bottom);
	$: barHeight = innerHeight / data.insights.genreData.length;

	let tooltipVisible = false;
	const tooltipPosition = spring(
		{ x: 0, y: 0 },
		{
			stiffness: 0.15,
			damping: 0.4,
		},
	);
	let toolUser = "";
	let toolAvg = "";
	let toolDiff = "";
	let hoveredIndex = -1;

	function handleMouseMove(event) {
		const svgRect = event.currentTarget.getBoundingClientRect();
		const mouseY = event.clientY - svgRect.top;
		const mouseX = event.clientX - svgRect.left;
		const index = Math.floor((mouseY - padding.top + 40) / barHeight);

		if (index >= 0 && index < data.insights.genreData.length) {
			const point = data.insights.genreData[index];
			tooltipVisible = true;
			tooltipPosition.set({ x: mouseX + 20, y: mouseY - 120 });
			toolUser = `${point.weighted_user}`;
			toolAvg = `${point.weighted_average}`;
			toolDiff = `${point.weighted_diff}`;
			hoveredIndex = index;
		} else {
			hideTooltip();
		}
	}

	function hideTooltip() {
		tooltipVisible = false;
		hoveredIndex = -1;
	}

	let yAdj = 4;
</script>

<div class="chart" bind:clientWidth={width}>
	<svg
		{width}
		{height}
		viewBox="0 0 {width} {height}"
		on:mousemove={handleMouseMove}
		on:mouseleave={hideTooltip}
		role="tooltip"
	>
		<g class="axis x-axis">
			{#each xTicks as tick}
				<g
					class="tick tick-{tick}"
					transform="translate({xScale(tick)}, {height})"
				>
					<line y1="-20" y2={-height} />
					<text>{tick}</text>
				</g>
			{/each}
		</g>
		<g class="bars">
			{#each data.insights.genreData as point, i}
				<g
					class:hovered={hoveredIndex === i}
					class:dimmed={hoveredIndex !== -1 && hoveredIndex !== i}
				>
					<rect
						class="fill-primary"
						x={xScale(xMin)}
						y={yScale(i) - yAdj - barWidth / 2.5}
						height={width > 380 ? barWidth * 0.4 : barWidth * 1.5}
						width={xScale(point.weighted_user) - xScale(xMin)}
					/>
					<rect
						class="fill-plot-accent"
						x={xScale(xMin)}
						y={yScale(i) - yAdj}
						height={width > 380 ? barWidth * 0.4 : barWidth * 1.5}
						width={xScale(point.weighted_average) - xScale(xMin)}
					/>
				</g>
			{/each}
		</g>
		<g class="axis y-axis">
			{#each data.insights.genreData as point, i}
				<g
					class:hovered={hoveredIndex === i}
					class:dimmed={hoveredIndex !== -1 && hoveredIndex !== i}
				>
					<g class="tick" transform="translate(0, {yScale(i)})">
						<text x={barHeight * 2.4}>{point.genres}</text>
					</g>
				</g>
			{/each}
		</g>
	</svg>
	{#if tooltipVisible}
		<div class="tooltip" style="left: {$tooltipPosition.x}px; top: {$tooltipPosition.y}px">
			<span class="text-primary">{username}: {toolUser}</span><br /><span
				class="text-plot-accent">AniList: {toolAvg}</span
			><br /><span class="text-destructive">Difference: {toolDiff}</span>
		</div>
	{/if}
</div>

<style lang="postcss">
	.x-axis .tick text {
		@apply text-current;
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

	.y-axis text {
		transition: opacity 0.2s ease-in-out;
	}

	.y-axis g.dimmed text {
		opacity: 0.3;
	}

	.y-axis g.hovered text {
		opacity: 1;
	}

	.tick {
		@apply text-current text-sm shadow-lg;
	}

	.tick text {
		@apply fill-current text-current font-semibold;
		text-anchor: start;
	}

	.y-axis .tick text {
		text-anchor: end;
	}

	.tick line {
		@apply stroke-secondary stroke-1 opacity-100;
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
