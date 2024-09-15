<script>
	import { select } from "d3-selection";
	import { axisBottom, axisLeft } from "d3-axis";
	import { format } from "d3-format";

	export let width;
	export let height;
	export let margin;
	export let position;
	export let scale;
	export let tick_outer;
	export let tick_number;
	export let to_format;
	export let no_domain;
	export let formatString = "$.0f";
	export let format_mobile;

	const formatMobile = (tick) => {
		return '"' + tick.toString().slice(13, 15);
	};

	const formatter = format(formatString);
	let transform;
	let g;

	$: if (g && width && scale) {
		select(g).selectAll("*").remove();

		let axis;

		switch (position) {
			case "bottom":
				axis = axisBottom(scale).tickSizeOuter(tick_outer || 0);
				if (format_mobile) {
					axis.tickFormat((d) => formatMobile(d));
				}
				transform = `translate(0, ${height - margin.bottom})`;
				break;
			case "left":
				axis = axisLeft(scale)
					.tickSizeOuter(tick_outer || 0)
					.ticks(tick_number || 5)
					.tickSizeInner(-width + margin.left + margin.right);
				if (to_format) {
					axis.tickFormat((d) => formatter(d));
				}
				transform = `translate(${margin.left}, 0)`;
				break;
			default:
				console.warn(`Unsupported position: ${position}`);
		}

		const selection = select(g);
		selection.attr("transform", transform);

		if (no_domain) {
			selection.call(axis).select(".domain").remove();
		} else {
			selection.call(axis);
			selection.selectAll("path").attr("class", "stroke-border");
			selection.selectAll("line").attr("class", "stroke-border");
			selection.selectAll("text").attr("class", "fill-current text-sm");
		}
	}
</script>

<g class="axis" bind:this={g} />

<style>
	.axis {
		shape-rendering: crispEdges;
	}
</style>
