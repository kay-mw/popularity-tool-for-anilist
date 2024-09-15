<script>
	import { scaleLinear } from "d3-scale";
	import { max } from "d3-array";
	import Axis from "$lib/components/Axis.svelte";
	import Labels from "$lib/components/Labels.svelte";
	import Line from "$lib/components/Line.svelte";
	import Legend from "$lib/components/Legend.svelte";

	let width;
	const height = 700;
	const margin = { top: 40, right: 200, bottom: 20, left: 35 };

	let xScale, yScale;

	export let data;

	$: console.log(width);

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
