<script>
	import * as Card from "$lib/components/ui/card";
	import H2 from "$lib/components/H2.svelte";

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
	<Card.Content class="flex flex-col justify-center space-y-4 font-semibold">
		<H2 class="{textColour} text-2xl">{animeTitle}</H2>
		<figure class="relative">
			<img
				class="flex border-solid border-2 border-border rounded-xl w-full"
				src={image}
				alt="coldest take anime"
			/>
			<div
				class="absolute bottom-6 md:bottom-8 pt-1 md:pt-2 pl-3 h-[3rem] md:h-[4.5rem] bg-secondary w-full drop-shadow-lg"
				style="--tw-bg-opacity: 0.85; background-color: hsl(var(--secondary) / var(--tw-bg-opacity));"
			>
				<div class="font-semibold text-sm md:text-lg">
					<p class={textColour}>{username}: {userScore}</p>
					<p class="text-plot-accent">AniList: {avgScore}</p>
				</div>
			</div>
		</figure>
	</Card.Content>
</Card.Root>
