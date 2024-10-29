<script>
  import { Button } from "$lib/components/ui/button";
  import Container from "$lib/components/Container.svelte";
  import { toggleMode } from "mode-watcher";
  import "../app.css";
  import { ModeWatcher } from "mode-watcher";
  import { navigating } from "$app/stores";
</script>

<svelte:head>
  <link
    href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap"
    rel="stylesheet"
  />
  <title>How Popular is Your Anime Taste?</title>
</svelte:head>

<ModeWatcher />
<div class="md:sticky z-10 top-0 h-0">
<div class="absolute z-10 right-0 p-4">
  <Button on:click={toggleMode} variant="outline" size="sm">
    <span class="hidden dark:flex">Dark</span>
    <span class="dark:hidden">Light</span>
  </Button>
</div>
  </div>

{#if $navigating}
  <Container>
    <div
      class="border-border h-20 w-20 animate-spin rounded-full border-[12px] border-t-primary"
    />
  </Container>
{/if}
<slot />

<style lang="postcss">
  :global(body) {
    font-family: "DM Sans", sans-serif;
  }
  :global(body) {
    @apply scroll-smooth;
  }
</style>
