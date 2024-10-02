<script lang="ts">
	import { min, max } from "d3-array";
	import { scaleLinear } from "d3-scale";
	import { spring } from "svelte/motion";
	import { page } from "$app/stores";

	export let data;
	const username = $page.url.searchParams.get("username");

	$: yMin =
		Math.ceil(
			Math.min(
				min(data.insights.genreData, (d) => +d.weighted_average),
				min(data.insights.genreData, (d) => +d.weighted_user),
			),
		) - 5;

	$: yMax = Math.ceil(
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
	$: yTicks = range(yMin, yMax, 1);

	const padding = { top: 15, right: 0, bottom: 20, left: 35 };

	let width = 913;
	let height = 525;

	$: xScale = scaleLinear()
		.domain([0, data.insights.genreData.length])
		.range([padding.left, width - padding.right]);

	$: yScale = scaleLinear()
		.domain([Math.min.apply(null, yTicks), Math.max.apply(null, yTicks)])
		.range([height - padding.bottom, padding.top]);

	$: innerWidth = width - (padding.left + padding.right);
	$: barWidth = innerWidth / data.insights.genreData.length;

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
		const mouseX = event.clientX - svgRect.left;
		const index = Math.floor((mouseX - padding.left) / barWidth);

		if (index >= 0 && index < data.insights.genreData.length) {
			const point = data.insights.genreData[index];
			tooltipVisible = true;
			tooltipPosition.set({ x: event.clientX + 10, y: event.clientY + 10 });
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
</script>

<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
	<svg
		{width}
		{height}
		viewBox="0 0 {width} {height}"
		on:mousemove={handleMouseMove}
		on:mouseleave={hideTooltip}
		role="tooltip"
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
			{#each data.insights.genreData as point, i}
				<g
					class:hovered={hoveredIndex === i}
					class:dimmed={hoveredIndex !== -1 && hoveredIndex !== i}
				>
					{#if point.weighted_average > point.weighted_user}
						<rect
							class="fill-plot-accent"
							x={xScale(i) + 4.3}
							y={yScale(point.weighted_average)}
							width={barWidth * 0.4}
							height={yScale(yMin) - yScale(point.weighted_average)}
						/>
						<rect
							class="fill-primary"
							x={xScale(i) - 4.3 + barWidth / 2}
							y={yScale(point.weighted_user)}
							width={barWidth * 0.4}
							height={yScale(yMin) - yScale(point.weighted_user)}
						/>
					{:else}
						<rect
							class="fill-primary"
							x={xScale(i) + 4.3}
							y={yScale(point.weighted_user)}
							width={barWidth * 0.40}
							height={yScale(yMin) - yScale(point.weighted_user)}
						/>
						<rect
							class="fill-plot-accent"
							x={xScale(i) - 4.3 + barWidth / 2}
							y={yScale(point.weighted_average)}
							width={barWidth * 0.40}
							height={yScale(yMin) - yScale(point.weighted_average)}
						/>
					{/if}
				</g>
			{/each}
		</g>
		<g class="axis x-axis">
			{#each data.insights.genreData as point, i}
				<g
					class:hovered={hoveredIndex === i}
					class:dimmed={hoveredIndex !== -1 && hoveredIndex !== i}
				>
					<g class="tick" transform="translate({xScale(i)}, {height})">
						<text x={barWidth / 2} y="-4">
							{point.genres}
						</text>
					</g>
				</g>
			{/each}
		</g>
		<rect
			x={padding.left}
			y={padding.top}
			width={width - padding.left - padding.right}
			height={height - padding.top - padding.bottom}
			fill="transparent"
		/>
	</svg>
	{#if tooltipVisible}
		<div class="tooltip">
			<span class="text-primary">{username}: {toolUser}</span><br
			/><span class="text-plot-accent">AniList: {toolAvg}</span
			><br /><span class="text-destructive"
				>Difference: {toolDiff}</span
			>
		</div>
	{/if}
</div>

<style lang="postcss">
	.x-axis .tick text {
		@apply text-current;
		text-anchor: middle;
	}

	.bars rect {
		@apply stroke-1 stroke-secondary;
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
		@apply text-current text-sm shadow-lg;
	}

	.tick text {
		@apply fill-current text-current font-semibold;
		text-anchor: start;
	}

	.tick line {
		@apply stroke-secondary stroke-2 opacity-100;
	}

	.tick.tick-0 line {
		@apply inline-block;
	}

	.tooltip {
		@apply absolute bg-background border border-secondary font-semibold p-2 rounded shadow-lg text-base top-0 right-1;
		pointer-events: none;
		z-index: 100;
		transition: opacity 0.2s ease-in-out;
	}
</style>
