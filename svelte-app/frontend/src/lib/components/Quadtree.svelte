<script>
	import { quadtree } from "d3-quadtree";
	import { spring } from "svelte/motion";

	export let xScale, yScale, width, height;
	export let margin;
	export let data;
	export let searchRadius = 10;

	let hoveredItem = null;
	let userFinder, averageFinder;
	let visible = false;
	let x = { circle: 0, square: 0 };
	let y = 0;

	const radius = spring(5); // Default radius
	const hoverRadius = 10; // Radius when hovered

	$: if (data) {
		userFinder = quadtree()
			.x((d) => xScale(+d.user_score))
			.y((d) => yScale(+d.user_count))
			.addAll(data.filter((d) => d.user_count > 0));

		averageFinder = quadtree()
			.x((d) => xScale(+d.average_score))
			.y((d) => yScale(+d.average_count))
			.addAll(data.filter((d) => d.average_count > 0));
	}

	function findItem(evt) {
		const mouseX = evt.layerX;
		const mouseY = evt.layerY;

		const foundUser = userFinder.find(mouseX, mouseY, searchRadius);
		const foundAverage = averageFinder.find(mouseX, mouseY, searchRadius);

		hoveredItem = foundUser || foundAverage;

		if (hoveredItem) {
			radius.set(hoverRadius);
			visible = true;
			x = getPosition(hoveredItem);
			y = yScale(+(hoveredItem.user_count || hoveredItem.average_count));
		} else {
			resetHover();
		}
	}

	function resetHover() {
		hoveredItem = null;
		visible = false;
		radius.set(5);
	}

	const getPosition = (item) => {
		if (item) {
			const xPos = xScale(+item.user_score || +item.average_score);
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
	on:mouseout={resetHover}
	on:blur={resetHover}
/>

<slot {hoveredItem} {visible} {x} {y} radius={$radius} />
