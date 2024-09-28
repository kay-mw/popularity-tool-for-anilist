<script>
	import { Separator } from "$lib/components/ui/separator";

	export let valueAbs;
	export let colour;
	export let image;
	export let descriptor;
	export let emphasis;
	export let alt;
</script>

<img
	class="flex m-auto w-full border-solid border-2 border-border rounded-xl"
	src={image}
	{alt}
/>
<h3
	class="text-5xl text-center text-{colour} font-bold tracking-widest scroll-m-20"
>
	{descriptor}
</h3>
<Separator />
<p class="text-2xl text-center scroll-m-20 tracking-tight">
	Your ratings differ by {emphasis}
	<span class="text-{colour} font-semibold">{valueAbs} points</span> compared to
	the average AniList user!
</p>
