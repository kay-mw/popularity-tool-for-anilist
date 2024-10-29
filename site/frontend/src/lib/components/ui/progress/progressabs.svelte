<script lang="ts">
	import { Progress as ProgressPrimitive } from "bits-ui";
	import { cn } from "$lib/utils.js";

	type $$Props = ProgressPrimitive.Props;

	let className: $$Props["class"] = undefined;
	export let max: $$Props["max"] = 100;
	export let value: $$Props["value"] = undefined;
	//export let color: $$Props["color"] = undefined;
	//export { className as class };
	$: percentage = ((value ?? 0) / (max ?? 1)) * 100;
</script>

<!--<div-->
<!--	class={cn(-->
<!--		"inline-block bg-background mb-[-1rem] mt-[-1rem] py-0.5 px-1.5 rounded-lg border border-secondary font-semibold text-lg",-->
<!--		Math.floor(value) < 5 ? "text-primary" : "",-->
<!--		Math.floor(value) <= 10 ? "text-red-400" : "",-->
<!--		Math.floor(value) > 20 ? "text-destructive" : ""-->
<!--	)}-->
<!--	style={`margin-inline-start: calc(${percentage}% - 2.25em)`}-->
<!-->-->
<!--	{value}°C-->
<!--</div>-->
<ProgressPrimitive.Root
	class="bg-secondary relative h-4 w-full overflow-hidden rounded-full"
>
	<div
		class="absolute top-0 right-0 w-full h-full bg-gradient-to-r from-primary from-10% to-80% to-destructive"
	></div>
	<div
		class="bg-secondary absolute top-0 right-0 h-full border-8 border-secondary"
		style={`width: ${100 - percentage}%`}
	></div>
</ProgressPrimitive.Root>
