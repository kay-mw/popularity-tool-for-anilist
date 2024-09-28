<script>
	import { ProgressMid } from "$lib/components/ui/progress";
	import { Separator } from "$lib/components/ui/separator";

	export let valueAvg;
	export let accentColour;
	export let valueDirection;
	export let image;
	export let alt;
</script>

<ProgressMid value={valueAvg} max={50} />
<br />
<Separator />
<br />
<img
	class="flex m-auto w-full border-solid border-2 border-border rounded-xl"
	src={image}
	{alt}
/>
<br />
<p class="text-2xl text-center tracking-tight scroll-m-20">
	On average, you score anime <span class="{accentColour} font-semibold"
		>{Math.abs(valueAvg)} points {valueDirection}</span
	> than the typical AniList user!
</p>
