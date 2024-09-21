<script lang="ts">
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";
	import { spring } from "svelte/motion";
	import { page } from "$app/stores";

	import Labels from "$lib/components/Labels.svelte";

	export let data;

	const username = $page.url.searchParams.get("username");

	$: yMax = Math.max(
		max(data.insights.userData, (d) => +d.user_count),
		max(data.insights.userData, (d) => +d.average_count),
	);

	$: yTicks = Array.from({ length: Math.ceil(yMax / 5) + 1 }, (_, i) => i * 5);
	const padding = { top: 20, right: 15, bottom: 20, left: 25 };

	let width = 913;
	let height = 525;

	$: xScale = scaleLinear()
		.domain([0, data.insights.userData.length])
		.range([padding.left, width - padding.right]);

	$: yScale = scaleLinear()
		.domain([0, Math.max.apply(null, yTicks)])
		.range([height - padding.bottom, padding.top]);

	$: innerWidth = width - (padding.left + padding.right);
	$: barWidth = innerWidth / data.insights.userData.length;

	function formatMobile(tick: number) {
		return "'" + tick.toString().slice(-2);
	}

	let tooltipVisible = false;
	const tooltipPosition = spring(
		{ x: 0, y: 0 },
		{
			stiffness: 0.15,
			damping: 0.4,
		},
	);
	let tooltipContent = "";

	let hoveredIndex = -1;

	function handleMouseMove(event) {
		const svgRect = event.currentTarget.getBoundingClientRect();
		const mouseX = event.clientX - svgRect.left;
		const index = Math.floor((mouseX - padding.left) / barWidth);

		if (index >= 0 && index < data.insights.userData.length) {
			const point = data.insights.userData[index];
			tooltipVisible = true;
			tooltipPosition.set({ x: event.clientX + 10, y: event.clientY - 10 });
			tooltipContent = `<span class="text-primary">${username}: ${point.user_count}</span><br><span class="text-plot-accent">AniList: ${point.average_count}</span>`;
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
		on:mousemove={handleMouseMove}
		on:mouseleave={hideTooltip}
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
		<Labels
			labelfory={true}
			textanchor={"start"}
			{width}
			{height}
			margin={padding}
			yoffset={height / 2}
			xoffset={10}
			label="Count ↑"
		/>
		<g class="bars">
			{#each data.insights.userData as point, i}
				<g
					class:hovered={hoveredIndex === i}
					class:dimmed={hoveredIndex !== -1 && hoveredIndex !== i}
				>
					{#if point.average_count > point.user_count}
						<rect
							class="fill-plot-accent"
							x={xScale(i) + 2}
							y={yScale(point.average_count)}
							width={barWidth * 0.9}
							height={yScale(0) - yScale(point.average_count)}
						/>
						<rect
							class="fill-primary"
							x={xScale(i) + 2}
							y={yScale(point.user_count)}
							width={barWidth * 0.9}
							height={yScale(0) - yScale(point.user_count)}
						/>
					{:else}
						<rect
							class="fill-primary"
							x={xScale(i) + 2}
							y={yScale(point.user_count)}
							width={barWidth * 0.9}
							height={yScale(0) - yScale(point.user_count)}
						/>
						<rect
							class="fill-plot-accent"
							x={xScale(i) + 2}
							y={yScale(point.average_count)}
							width={barWidth * 0.9}
							height={yScale(0) - yScale(point.average_count)}
						/>
					{/if}
				</g>
			{/each}
		</g>
		<g class="axis x-axis">
			{#each data.insights.userData as point, i}
				<g class="tick" transform="translate({xScale(i)}, {height})">
					<text x={barWidth / 2} y="-4">
						{width > 380 ? point.user_score : formatMobile(point.user_score)}
					</text>
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
			{@html tooltipContent}
		</div>
	{/if}
</div>

<style lang="postcss">
	.x-axis .tick text {
		@apply text-center text-current;
		text-anchor: middle;
	}

	.bars rect {
		@apply stroke-2 stroke-secondary;
		transition: opacity 0.2s ease-in-out;
	}

	.bars g.dimmed rect {
		opacity: 0.3;
	}

	.bars g.hovered rect {
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
		@apply stroke-secondary stroke-2 opacity-100;
	}

	.tick.tick-0 line {
		@apply inline-block;
	}

	.tooltip {
		@apply absolute bg-background border border-secondary font-semibold p-2 rounded shadow-lg text-base top-1 left-9;
		pointer-events: none;
		z-index: 100;
		transition: opacity 0.2s ease-in-out;
	}
</style>
