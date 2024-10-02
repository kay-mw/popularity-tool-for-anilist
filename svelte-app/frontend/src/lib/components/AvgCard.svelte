<script>
	import { ProgressMid } from "$lib/components/ui/progress";
	import { Separator } from "$lib/components/ui/separator";
	import * as Card from "$lib/components/ui/card";

	export let valueAvg;
	export let accentColour;
	export let valueDirection;
	export let image;
	export let alt;
	export let descriptor;
</script>

<Card.Root class="max-w-xl">
	<Card.Header>
		<Card.Title class={accentColour}>Average Score Difference</Card.Title>
		<Card.Description>
			Whether you tend to rate anime higher/lower.
		</Card.Description>
	</Card.Header>
	<Card.Content class="space-y-4">
		<ProgressMid value={valueAvg} max={50} />
		<Separator />
		<img
			class="flex m-auto w-full border-solid border-2 border-border rounded-xl"
			src={image}
			{alt}
		/>
		<h3
			class="text-5xl text-center {accentColour} font-bold tracking-wider scroll-m-20"
		>
			{descriptor}
		</h3>
		<Separator />
		<p class="text-2xl text-center tracking-tight scroll-m-20">
			On average, you score anime <span class="{accentColour} font-semibold"
				>{Math.abs(valueAvg)} points {valueDirection}</span
			> than the typical AniList user!
		</p>
	</Card.Content>
</Card.Root>
