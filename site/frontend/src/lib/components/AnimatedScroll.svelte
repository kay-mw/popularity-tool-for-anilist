<script lang="ts">
	import { onMount } from "svelte";

	let { threshold = 0.2, children, duration = "2s" } = $props();

	let element: HTMLDivElement;
	let intersecting = $state();

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				intersecting = entries[0].isIntersecting;
			},
			{ threshold },
		);
		observer.observe(element);
		return () => observer.unobserve(element);
	});
</script>

<div
	bind:this={element}
	class:animated={intersecting}
	style="--duration: {duration}"
>
	{@render children?.()}
</div>

<style>
	div {
		opacity: 0;
		transform: translateY(20px);
		transition:
			opacity var(--duration),
			transform 2s;
	}

	div.animated {
		opacity: 1;
		transform: translateY(0);
	}
</style>
