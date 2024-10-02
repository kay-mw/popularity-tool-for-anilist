<script>
	import { onMount } from "svelte";

	export let threshold = 0.1;
	export let animationClass = "visible";

	let element;
	let intersecting;

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

<div bind:this={element} class:animated={intersecting}>
	<slot />
</div>

<style>
	div {
		opacity: 0;
		transform: translateY(20px);
		transition:
			opacity 2s,
			transform 2s;
	}

	div.animated {
		opacity: 1;
		transform: translateY(0);
	}
</style>
