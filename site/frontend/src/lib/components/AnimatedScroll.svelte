<script lang="ts">
	import { onMount } from "svelte";

	let {
		threshold = 0.2,
		movement = "20px",
		fadeInTime = 0.4,
		opacityDuration = "2s",
		transformDuration = "2s",
		delay = "0s",
		children,
		class: className = "",
	} = $props();

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
	style="--opacity-duration: {opacityDuration}; 
	--transform-duration: {transformDuration}; 
	--movement: {movement}; 
	--fade-in-time: {fadeInTime}; 
	--delay: {delay};"
	class={className}
>
	{@render children?.()}
</div>

<style>
	div {
		opacity: 0;
		transform: translateY(var(--movement));
		transition:
			opacity var(--opacity-duration)
				cubic-bezier(var(--fade-in-time), 0, 0.2, 1),
			transform var(--transform-duration)
				cubic-bezier(var(--fade-in-time), 0, 0.2, 1);
		transition-delay: var(--delay);
	}

	div.animated {
		opacity: 1;
		transform: translateY(0);
	}
</style>
