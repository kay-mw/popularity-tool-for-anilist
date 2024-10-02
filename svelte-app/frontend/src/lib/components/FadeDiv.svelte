<script>
	import { fade } from "svelte/transition";
	import { sineIn } from "svelte/easing";
	export let delay;
</script>

<div in:fade={{ duration: 1000, delay: delay, easing: sineIn }}>
	<slot />
</div>
