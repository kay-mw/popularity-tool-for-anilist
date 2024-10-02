<script lang="ts">
	import H1 from "$lib/components/H1.svelte";
	import { Separator } from "$lib/components/ui/separator";
	export let header = "";
</script>

<H1 class="tracking-normal text-primary {$$restProps.class}">{header}</H1>
