<script>
	import * as Card from "$lib/components/ui/card";
	import H2 from "$lib/components/H2.svelte";
	import { Separator } from "$lib/components/ui/separator";

	export let title = "";
	export let description = "";
	export let image = "";
	export let animeTitle = "";
	export let userScore = 0;
	export let avgScore = 0;
	export let titleColour = "";
</script>

<Card.Root>
	<Card.Header>
		<Card.Title class={titleColour}>{title}</Card.Title>
		<Card.Description>{description}</Card.Description>
	</Card.Header>
	<Card.Content class="flex flex-col justify-center space-y-4">
		<H2 class={titleColour}>{animeTitle}</H2>
		<img
			class="flex border-solid border-2 border-border rounded-xl w-full"
			src={image}
			alt="coldest take anime"
		/>
	</Card.Content>
	<Separator />
	<Card.Footer class="flex flex-col mt-5 items-center justify-center font-semibold">
		<p class="text-primary">Your Score: {userScore}</p>
		<p class="text-plot-accent">AniList Average: {avgScore}</p>
	</Card.Footer>
</Card.Root>
