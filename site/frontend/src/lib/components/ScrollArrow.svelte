<script lang="ts">
	export let g: Generator;
	export let block: string;
	export let up: boolean;

	function scrollToElement() {
		let element = g.next().value;
		if (element) {
			element.scrollIntoView({ behavior: "smooth", block: `${block}` });
		}
	}
</script>

<button class={$$restProps.class} on:click={() => scrollToElement()}>
	{#if up === false}
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			stroke-width="3.5"
			stroke="currentColor"
			class="size-10 stroke-primary mt-3 animate-pulse"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3"
			/>
		</svg>
	{:else}
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			stroke-width="3.5"
			stroke="currentColor"
			class="size-10 stroke-primary mt-3"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18"
			/>
		</svg>
	{/if}
</button>
