<script>
	import { Separator } from "$lib/components/ui/separator";
	import { ProgressAbs } from "$lib/components/ui/progress";
	import * as Card from "$lib/components/ui/card";

	export let valueAbs;
	export let colour;
	export let image;
	export let descriptor;
	export let emphasis;
	export let alt;

	let max = 75;
	let tempMultiplier = 3;
</script>

<Card.Root class="max-w-xl">
	<Card.Header>
		<Card.Title class="text-{colour}">Absolute Score Difference</Card.Title>
		<Card.Description
			>How far your scores are from the average, regardless of whether you rate
			higher/lower.
		</Card.Description>
	</Card.Header>
	<Card.Content class="space-y-4">
		<ProgressAbs value={(valueAbs * tempMultiplier).toFixed(2)} {max} />
		<Separator />
		<div
			class="max-h-[25rem] overflow-hidden border-solid border-2 border-border rounded-xl"
		>
			<img class="flex m-auto w-full" src={image} {alt} />
		</div>
		<h3
			class="text-5xl text-center text-{colour} font-bold tracking-wider scroll-m-20"
		>
			{descriptor}
		</h3>
		<Separator />
		<p class="text-2xl text-center scroll-m-20 tracking-tight">
			Your ratings differ by {emphasis}
			<span class="text-{colour} font-semibold">{valueAbs} points</span> compared
			to the average AniList user!
		</p>
	</Card.Content>
</Card.Root>
