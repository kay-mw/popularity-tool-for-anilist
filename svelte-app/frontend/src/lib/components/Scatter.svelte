<script>
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";
	import Axis from "$lib/components/Axis.svelte";
	import Labels from "$lib/components/Labels.svelte";
	import Line from "$lib/components/Line.svelte";
	import Quadtree from "$lib/components/Quadtree.svelte";

	let width = 0;
	const height = 700;
	const margin = { top: 40, right: 200, bottom: 20, left: 35 };

	let xScale = scaleLinear(),
		yScale = scaleLinear();

	export let data;

	$: yMax =
		max([
			max(data, (d) => +d.user_count ?? 0) ?? 0,
			max(data, (d) => +d.average_count ?? 0) ?? 0,
		]) ?? 0;

	$: if (data) {
		xScale = scaleLinear()
			.domain([0, 100])
			.range([margin.left, width - margin.right]);
		yScale = scaleLinear()
			.domain([0, yMax])
			.range([height - margin.bottom, margin.top]);
	}
</script>

<div class="flex container pl-16 max-w-[70rem]" bind:clientWidth={width}>
	<div class="relative">
		{#if data && width}
			<Quadtree
				{data}
				{xScale}
				{yScale}
				{width}
				{height}
				{margin}
				let:hoveredItem
				let:visible
				let:x
				let:y
				let:radius
			>
				<div
					class="absolute leading-[1.2] z-[1] transition-all ease-in-out duration-300 tooltip pointer-events-none bg-card rounded-lg border font-normal border-border bg-opacity-90"
					style="top: {y + 5}px; left: {x.square + 10}px; display: {visible
						? 'block'
						: 'none'};"
				>
					{#if hoveredItem && hoveredItem.user_count > 0}
						<p class="text-primary p-1">
							Score → {hoveredItem.user_score} <br />
							Count → {hoveredItem.user_count}
						</p>
					{/if}
					{#if hoveredItem && hoveredItem.average_count > 0}
						<p class="text-plot-accent p-1">
							Score → {hoveredItem.average_score} <br />
							Count → {hoveredItem.average_count}
						</p>
					{/if}
				</div>
				<svg {width} {height}>
					<g>
						<Axis {width} {height} {margin} scale={xScale} position="bottom" />
						<Axis {width} {height} {margin} scale={yScale} position="left" />
						<Labels
							labelforx={true}
							{width}
							{height}
							{margin}
							yoffset={-30}
							xoffset={-170}
							label="Score →"
						/>
						<Labels
							labelfory={true}
							textanchor={"start"}
							{width}
							{height}
							{margin}
							yoffset={10}
							xoffset={10}
							label="Count ↑"
						/>
						<Line {data} {xScale} {yScale} />
						{#each data as d, i}
							{#if +d.user_count > 0}
								<circle
									class="fill-primary"
									cx={xScale(+d.user_score)}
									cy={yScale(+d.user_count)}
									r={hoveredItem === d ? radius : 5}
								/>
							{/if}
							{#if +d.average_count > 0}
								<circle
									class="fill-plot-accent"
									cx={xScale(+d.average_score)}
									cy={yScale(+d.average_count)}
									r={hoveredItem === d ? radius : 5}
								/>
							{/if}
						{/each}
					</g>
				</svg>
			</Quadtree>
		{/if}
	</div>
</div>
