<script>
	import * as Card from "$lib/components/ui/card";
	import H2 from "$lib/components/H2.svelte";

	export let title = "";
	export let description = "";
	export let image = "";
	export let animeTitle = "";
	export let userScore = 0;
	export let avgScore = 0;
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>{title}</Card.Title>
		<Card.Description>{description}</Card.Description>
	</Card.Header>
	<Card.Content class="flex flex-col justify-center max-w-xs space-y-4">
		<H2>{animeTitle}</H2>
		<img
			class="border-solid border-2 border-border rounded-xl"
			src={image}
			alt="coldest take anime"
		/>
	</Card.Content>
	<Card.Footer class="flex flex-col items-start justify-start">
		<p>Your Score: {userScore}</p>
		<p>AniList Average: {avgScore}</p>
	</Card.Footer>
</Card.Root>
