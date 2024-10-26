<script lang="ts">
	import H2 from "$lib/components/H2.svelte";

	export let header = "";

	function* getValidElements() {
		const elements = document.getElementsByClassName("bg-card");
		for (let item of elements) {
			yield item;
		}
	}

	let g = getValidElements();

	function scrollToElement() {
		let element = g.next().value;
		if (element) {
			element.scrollIntoView({ behavior: "smooth" });
		} else {
			g = getValidElements();
			let element = g.next().value;
			element.scrollIntoView({ behavior: "smooth" });
		}
	}
</script>

<H2 class="text-primary text-center text-6xl">{header}</H2>
