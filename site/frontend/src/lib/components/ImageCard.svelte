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
	export let textColour = "";
	export let username;
</script>

<Card.Root class="max-w-xl">
	<Card.Header>
		<Card.Title class={textColour}>{title}</Card.Title>
		<Card.Description>{description}</Card.Description>
	</Card.Header>
	<Card.Content class="relative justify-center space-y-4 font-semibold">
		<H2 class="{textColour} text-2xl">{animeTitle}</H2>
		<div class="relative">
			<figure>
				<img
					class="border-solid border-2 border-border rounded-lg w-full opacity-25"
					src={image}
					alt="coldest take anime"
				/>
			</figure>
			<div class="absolute space-y-2 font-semibold text-xl md:text-3xl top-1/2 left-1/2 w-[75%] text-center" style="transform: translate(-50%, -50%);">
				{#if userScore < avgScore}
					<p class={textColour}>{username} ↓ {userScore}</p>
					<Separator />
					<p class="text-plot-accent">AniList ↑ {avgScore}</p>
				{:else if userScore == avgScore}
					<p class={textColour}>{username} ~ {userScore}</p>
					<Separator />
					<p class="text-plot-accent">AniList ~ {avgScore}</p>
				{:else}
					<p class={textColour}>{username} ↑ {userScore}</p>
					<Separator />
					<p class="text-plot-accent">AniList ↓ {avgScore}</p>
				{/if}
			</div>
		</div>
	</Card.Content>
</Card.Root>
