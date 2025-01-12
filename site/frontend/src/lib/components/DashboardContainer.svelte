<script lang="ts">
	let { maxWidth = true, class: className = "", children, ...rest } = $props();
</script>

<div
	class="flex flex-col items-center justify-center m-auto w-full {maxWidth
		? 'max-w-screen-lg'
		: ''} p-4 {className}"
>
	{@render children?.()}
</div>
