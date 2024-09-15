<script>
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";
	import Axis from "$lib/components/Axis.svelte";
	import Labels from "$lib/components/Labels.svelte";
	import Line from "$lib/components/Line.svelte";
	import Quadtree from "$lib/components/Quadtree.svelte";

	let width;
	const height = 700;
	const margin = { top: 40, right: 200, bottom: 20, left: 35 };

	let xScale, yScale;

	export let data;

	$: yMax = max([
		max(data, (d) => +d.user_count ?? 0) ?? 0,
		max(data, (d) => +d.average_count ?? 0) ?? 0,
	]);

	$: if (data) {
		xScale = scaleLinear()
			.domain([0, 100])
			.range([margin.left, width - margin.right]);
		yScale = scaleLinear()
			.domain([0, yMax])
			.range([height - margin.bottom, margin.top]);
	}
</script>

<div
	class="flex max-w-[70rem] justify-center items-center"
	bind:clientWidth={width}
>
	<div class="relative">
		{#if data && width}
			<Quadtree
				{data}
				{xScale}
				{yScale}
				{width}
				{height}
				{margin}
				let:visible
				let:x
				let:y
				let:found
			>
				{#if found.user}
					<div
						class="position absolute rounded-[50%] pointer-events-none w-3 h-3 border border-primary transition-all duration-300 ease-in-out"
						style="transform: translate(-50%, -50%); top: {y}px; left: {x.circle}px; display: {visible
							? 'block'
							: 'none'}; width: {+found.user.user_count * 2 +
							5}px; height: {+found.user.user_count * 2 + 5}px;"
					/>
				{/if}
				{#if found.average}
					<div
						class="position absolute rounded-[50%] pointer-events-none w-3 h-3 border border-plot-accent transition-all duration-300 ease-in-out"
						style="transform: translate(-50%, -50%); top: {yScale(
							+found.average.average_count,
						)}px; left: {xScale(
							+found.average.average_score,
						)}px; display: {visible ? 'block' : 'none'}; width: {+found.average
							.average_count *
							2 +
							5}px; height: {+found.average.average_count * 2 + 5}px;"
					/>
				{/if}
				<div
					class="absolute min-w-[8em] leading-[1.2] z-[1] p-2 transition-all ease-in-out duration-300 tooltip pointer-events-none bg-card rounded-lg border font-normal border-border bg-opacity-90"
					style="top: {y + 5}px; left: {x.square + 10}px; display: {visible
						? 'block'
						: 'none'};"
				>
					{#if found.user}
						<p class="text-primary">
							User Score: {found.user.user_score} <br /> User Count: {found.user
								.user_count}
						</p>
					{/if}
					{#if found.user && found.average}
						<hr class="my-1" />
					{/if}
					{#if found.average}
						<p class="text-plot-accent">
							Average Score: {found.average.average_score} <br /> Average Count: {found
								.average.average_count}
						</p>
					{/if}
				</div>
			</Quadtree>
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
								r="5"
							/>
						{/if}
						{#if +d.average_count > 0}
							<circle
								class="fill-plot-accent"
								cx={xScale(+d.average_score)}
								cy={yScale(+d.average_count)}
								r="5"
							/>
						{/if}
					{/each}
				</g>
			</svg>
		{/if}
	</div>
</div>
