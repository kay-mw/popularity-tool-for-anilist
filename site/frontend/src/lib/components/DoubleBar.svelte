<script lang="ts">
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";
	import { Spring } from "svelte/motion";
	import { page } from "$app/state";

	let {
		data,
		y1,
		y2,
		x,
		xLabel = "Score →",
		yLabel = "Count →",
	}: {
		data: Array<Record<string, number>>;
		y1: string;
		y2: string;
		x: string;
		xLabel: string;
		yLabel: string;
	} = $props();

	const username = page.url.searchParams.get("username");

	let yMax = $derived(
		Math.max(
			max(data, (d) => +d[y1]),
			max(data, (d) => +d[y2]),
		),
	);

	let yTicks = $derived(
		Array.from({ length: Math.ceil(yMax / 5) + 1 }, (_, i) => i * 5),
	);
	const padding = { top: 20, right: 15, bottom: 40, left: 50 };

	let width = $state(913);
	let height = $state(525);

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

	let tooltipPosition = new Spring(
		{ x: 0, y: 0 },
		{
			stiffness: 0.15,
			damping: 0.4,
		},
	);

	let tooltipVisible = $state(false);
	let toolUser = $state("");
	let toolAvg = $state("");
	let hoveredIndex = $state(-1);

	function handleMouseMove(event: MouseEvent) {
		const svgRect = (event.currentTarget as SVGElement).getBoundingClientRect();
		const mouseX = event.clientX - svgRect.left;
		const mouseY = event.clientY - svgRect.top;
		const index = Math.floor((mouseX - padding.left) / barWidth);

		if (index >= 0 && index < data.length) {
			const point = data[index];
			tooltipVisible = true;
			tooltipPosition.target = { x: mouseX + 25, y: mouseY - 100 };
			if (mouseX + 25 > 820) {
				tooltipPosition.damping = 1;
				tooltipPosition.target = { x: mouseX - 115, y: mouseY - 100 };
			} else {
				tooltipPosition.damping = 0.4;
				tooltipPosition.target = { x: mouseX + 25, y: mouseY - 100 };
			}
			toolUser = `${point[y1]}`;
			toolAvg = `${point[y2]}`;
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

<div bind:clientWidth={width} bind:clientHeight={height}>
	<svg
		{width}
		{height}
		onmousemove={handleMouseMove}
		onmouseleave={hideTooltip}
		role="presentation"
		viewBox="0 0 {width} {height}"
	>
		<g class="axis y-axis">
			{#each yTicks as tick}
				<g class="tick tick-{tick}" transform="translate(0, {yScale(tick)})">
					<line x1="25" x2="100%" />
					<text y="-4" x="25">{tick}</text>
				</g>
			{/each}
			<g
				class="tick"
				transform="translate({10}, {(height - 35) /
					2}) rotate(-90)"
			>
				<text style="text-anchor: middle;">{yLabel}</text>
			</g>
		</g>
		<g class="bars">
			{#each data as point, i}
				<g
					class:hovered={hoveredIndex === i}
					class:dimmed={hoveredIndex !== -1 && hoveredIndex !== i}
				>
					{#if point[y2] > 0 && point[y1] > 0}
						<rect
							class="fill-plot-accent"
							rx="0.5rem"
							x={xScale(i) + barWidth / 2}
							y={yScale(point[y2])}
							width={barWidth * 0.35}
							height={yScale(0) - yScale(point[y2])}
						/>
						<rect
							class="fill-primary"
							rx="0.5rem"
							x={xScale(i) + 6.5}
							y={yScale(point[y1])}
							width={barWidth * 0.35}
							height={yScale(0) - yScale(point[y1])}
						/>
					{:else if point[y2] > 0 && point[y1] == 0}
						<rect
							class="fill-plot-accent"
							rx="0.5rem"
							x={xScale(i) + 2}
							y={yScale(point[y2])}
							width={barWidth * 0.9}
							height={yScale(0) - yScale(point[y2])}
						/>
					{:else}
						<rect
							class="fill-primary"
							rx="0.5rem"
							x={xScale(i) + 2}
							y={yScale(point[y1])}
							width={barWidth * 0.9}
							height={yScale(0) - yScale(point[y1])}
						/>
					{/if}
				</g>
			{/each}
		</g>
		<g class="axis x-axis">
			{#each data as point, i}
				<g
					class:hovered={hoveredIndex === i}
					class:dimmed={hoveredIndex !== -1 && hoveredIndex !== i}
				>
					<g class="tick" transform="translate({xScale(i)}, {height - 25})">
						<text x={barWidth / 2}>
							{point[x]}
						</text>
					</g>
					<g class="tick" transform="translate({width / 2 + 20}, {height})">
						<text>{xLabel}</text>
					</g>
				</g>
			{/each}
		</g>

		{#if tooltipVisible}
			<foreignObject
				x={tooltipPosition.current.x}
				y={tooltipPosition.current.y}
				width="100%"
				height="100%"
			>
				<div class="tooltip">
					<span class="text-primary">{username}: {toolUser}</span><br /><span
						class="text-plot-accent">AniList: {toolAvg}</span
					>
				</div>
			</foreignObject>
		{/if}
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
