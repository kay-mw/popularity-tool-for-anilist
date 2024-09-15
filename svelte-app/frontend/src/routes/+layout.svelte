<script>
  import { Button } from "$lib/components/ui/button";
  import { toggleMode } from "mode-watcher";
  import "../app.css";
  import { ModeWatcher } from "mode-watcher";
</script>

<svelte:head>
  <link
    href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap"
    rel="stylesheet"
  />
  <title>How Popular is Your Anime Taste?</title>
</svelte:head>

<ModeWatcher />
<div class="absolute p-4">
  <Button on:click={toggleMode} variant="outline" size="sm">
    <span class="hidden dark:flex">Dark</span>
    <span class="dark:hidden">Light</span>
  </Button>
</div>
<slot />

<style>
  :global(body) {
    font-family: "DM Sans", sans-serif;
  }
</style>
