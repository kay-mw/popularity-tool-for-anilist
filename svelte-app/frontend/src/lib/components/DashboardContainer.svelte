<script>
	import { fade } from "svelte/transition";
</script>

<div
	class="flex flex-col items-center m-auto w-full gap-4 p-8 max-w-screen-lg justify-center {$$restProps.class}"
transition:fade>
	<slot></slot>
</div>
