<script lang="ts">
	import { Progress as ProgressPrimitive } from "bits-ui";
	import { cn } from "$lib/utils.js";

	type $$Props = ProgressPrimitive.Props;
	let className: $$Props["class"] = undefined;
	export let max: $$Props["max"] = 100;
	export let value: $$Props["value"] = undefined;
	export { className as class };

	$: percentage = ((value ?? 0) / (max ?? 1)) * 100;
	$: isPositive = percentage >= 0;
	$: absolutePercentage = Math.abs(percentage);
</script>

<ProgressPrimitive.Root
	class={cn(
		"bg-secondary relative h-4 w-full overflow-hidden rounded-full",
		className,
	)}
	{...$$restProps}
>
	<div
		class="absolute top-0 bottom-0 w-1 left-1/2 bg-foreground"
		style="transform: translateX(-50%);"
	></div>
	<div
		class={cn(
			"h-full transition-all duration-700 absolute top-0 bottom-0 from-primary from-25%",
			isPositive
				? "to-plot-accent left-1/2 rounded-e-full bg-gradient-to-r"
				: "to-destructive right-1/2 rounded-s-full bg-gradient-to-l",
		)}
		style={`width: ${absolutePercentage}%;`}
	></div>
</ProgressPrimitive.Root>
