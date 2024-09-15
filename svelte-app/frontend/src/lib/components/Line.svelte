<script>
	import { line } from "d3-shape";

	export let data;
	export let xScale;
	export let yScale;

	$: userData = data.filter((d) => d.user_count > 0);
	$: averageData = data.filter((d) => d.average_count > 0);

	$: userLine = line()
		.x((d) => xScale(d.user_score))
		.y((d) => yScale(d.user_count));

	$: averageLine = line()
		.x((d) => xScale(d.average_score))
		.y((d) => yScale(d.average_count));
</script>

<svg>
	<path
		d={userLine(userData)}
		class="stroke-primary fill-none"
		stroke-width="2"
	/>
	<path
		d={averageLine(averageData)}
		class="stroke-plot-accent fill-none"
		stroke-width="2"
	/>
</svg>
