<script>
	import { quadtree } from "d3-quadtree";
	export let xScale, yScale, width, height;

	let visible = false;
	let found = { user: null, average: null };
	let e = {};

	export let margin;
	export let data;
	export let searchRadius = 10;

	function findItem(evt) {
		const xLayerKey = "layerX";
		const yLayerKey = "layerY";

		const x = evt[xLayerKey];
		const y = evt[yLayerKey];

		found.user = userFinder.find(x, y, searchRadius);
		found.average = averageFinder.find(x, y, searchRadius);
		
		visible = found.user || found.average;
	}

	let userFinder, averageFinder;

	$: if (data) {
		userFinder = quadtree()
			.x(d => xScale(+d.user_score))
			.y(d => yScale(+d.user_count))
			.addAll(data.filter(d => d.user_count > 0));

		averageFinder = quadtree()
			.x(d => xScale(+d.average_score))
			.y(d => yScale(+d.average_count))
			.addAll(data.filter(d => d.average_count > 0));
	}

	const getPosition = (found) => {
		if (found) {
			const xPos = xScale(+found.user_score || +found.average_score);
			if (xPos > 0.9 * xScale.range()[1]) {
				return { circle: xPos, square: xPos - 100 };
			} else {
				return { circle: xPos, square: xPos };
			}
		}
	};
</script>

<div
	aria-hidden
	class="absolute top-0 right-0 bottom-0 left-0"
	on:mousemove={findItem}
	on:blur={() => (visible = false)}
	on:mouseout={() => (visible = false)}
/>
{#if visible}
	<slot
		x={getPosition(found.user || found.average)}
		y={yScale(+(found.user?.user_count || found.average?.average_count))}
		{found}
		{visible}
		{margin}
		{e}
	/>
{/if}
