<script lang="ts">
	import { Progress as ProgressPrimitive } from "bits-ui";
	import { cn } from "$lib/utils.js";

	type $$Props = ProgressPrimitive.Props;

	let className: $$Props["class"] = undefined;
	export let max: $$Props["max"] = 100;
	export let value: $$Props["value"] = undefined;
	export { className as class };
	$: percentage = ((value ?? 0) / (max ?? 1)) * 100;
</script>

<div
	class={cn(
		"inline-block bg-background mb-[-1rem] mt-[-1rem] py-0.5 px-1.5 rounded-lg border border-secondary font-semibold text-lg",
		value > 20 && value <= 30 ? "text-red-400" : "",
		value <= 20 ? "text-primary" : "",
		value > 30 ? "text-destructive" : "",
	)}
	style={`margin-inline-start: ${percentage - 5}%`}
>
	{value}°C
</div>
<ProgressPrimitive.Root
	class={cn(
		"bg-secondary relative h-4 w-full overflow-hidden rounded-full",
		className,
	)}
	{...$$restProps}
>
	<div
		class="absolute top-0 right-0 w-full h-full bg-gradient-to-r from-primary from-30% to-70% to-destructive"
	></div>
	<div
		class="bg-secondary absolute top-0 right-0 h-full border-8 border-secondary"
		style={`width: ${100 - percentage}%`}
	></div>
</ProgressPrimitive.Root>
