<script lang="ts">
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";
	import { Spring } from "svelte/motion";

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

	let percentiles: Array<number> = [];
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

	let tooltipVisible = $state(false);
	let toolPop = $state(0);
	let toolPct = $state(0);
	let hoveredIndex = $state(-1);

	let tooltipPosition = new Spring(
		{ x: 0, y: 0 },
		{
			stiffness: 0.15,
			damping: 0.4,
		},
	);

	function handleMouseMove(event: MouseEvent) {
		const svgRect = (event.currentTarget as SVGElement).getBoundingClientRect();
		const mouseX = event.clientX - svgRect.left;
		const mouseY = event.clientY - svgRect.top;
		const index = Math.floor((mouseX - padding.left) / barWidth);

		if (index >= 0 && index < data.length) {
			tooltipVisible = true;
			tooltipPosition.target = { x: mouseX + 20, y: mouseY - 80 };

			if (tooltipPosition.target.x > svgRect.width - 155) {
				tooltipPosition.damping = 1;
				if (tooltipPosition.target.y > 0) {
					tooltipPosition.target.x = mouseX - 175;
				} else {
					tooltipPosition.target = { x: mouseX - 175, y: 0 };
				}
			} else if (tooltipPosition.target.y < 0) {
				tooltipPosition.target.y = 0;
			} else {
				tooltipPosition.damping = 0.4;
			}

			const point = data[index];
			const pctPoint = percentiles[index];
			toolPop = point[y];
			toolPct = pctPoint;
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
		viewBox="0 0 {width} {height}"
		onmousemove={handleMouseMove}
		onmouseleave={hideTooltip}
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
				<g
					class:hovered={hoveredIndex === i}
					class:dimmed={hoveredIndex !== -1 && hoveredIndex !== i}
				>
					<rect
						class={scoreVariable == point[y] ? colorY1 : colorY2}
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
							x={xScale(i) + 15}
							y={yScale(point[y]) - 10}
							>{username}
						</text>
					{/if}
				</g>
			{/each}
		</g>
		<g class="axis x-axis">
			{#each percentiles as pct, i}
				<g
					class:hovered={hoveredIndex === i}
					class:dimmed={hoveredIndex !== -1 && hoveredIndex !== i}
				>
					<g
						class="tick"
						style="text-anchor: middle;"
						transform="translate({xScale(i)}, {height - 30})"
					>
						<text x="17" y="5">
							{pct}%
						</text>
					</g>
				</g>
			{/each}
			<g
				class="tick"
				transform="translate({(width + padding.left - 37) / 2}, {height -
					1})"
			>
				<text>{xLabel} →</text>
			</g>
		</g>
		{#if tooltipVisible}
			<foreignObject
				x={tooltipPosition.current.x}
				y={tooltipPosition.current.y}
				width="100%"
				height="100%"
			>
				<div class="tooltip">
					<span
						class={toolPop == scoreVariable
							? "text-primary"
							: "text-plot-accent"}
						>Popularity: {toolPop}<br />Percentile: {toolPct}%</span
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

	.bars g.dimmed rect {
		opacity: 0.3;
	}

	.bars g.hovered rect {
		opacity: 1;
	}

	.bars rect {
		transition: opacity 0.2s ease-in-out;
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

	.tooltip {
		@apply absolute bg-background border border-secondary font-semibold p-2 rounded shadow-lg text-base;
		pointer-events: none;
		z-index: 100;
		transition: opacity 0.2s ease-in-out;
	}
</style>
