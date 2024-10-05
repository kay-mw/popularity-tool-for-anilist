<script lang="ts">
	import H2 from "$lib/components/H2.svelte";
	export let header = "";
	export let arrow = true;
</script>

<H2 class="text-primary text-center text-6xl">{header}</H2>
{#if arrow}
	<svg
		xmlns="http://www.w3.org/2000/svg"
		fill="none"
		viewBox="0 0 24 24"
		stroke-width="3.5"
		stroke="currentColor"
		class="size-8 stroke-primary mt-3 animate-pulse"
	>
		<path
			stroke-linecap="round"
			stroke-linejoin="round"
			d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3"
		/>
	</svg>
{/if}
