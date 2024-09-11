<script lang="ts">
  import { goto } from "$app/navigation";

  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Checkbox } from "$lib/components/ui/checkbox";
  import { Label } from "$lib/components/ui/label";

  import Container from "$lib/components/Container.svelte";
  import H1 from "$lib/components/H1.svelte";
  import H3 from "$lib/components/H3.svelte";

  import { toggleMode } from "mode-watcher";

  let isChecked = false;
  let username = "";
  let isLoading = false;

  $: labelClass = isChecked ? "text-primary" : "text-current";

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    isLoading = true;
    try {
      const response = await fetch("http://localhost:8000/api/home", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ manga_checked: isChecked, username: username }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      sessionStorage.setItem("insights", JSON.stringify(data.insights));
      goto("/dashboard");
    } catch (error) {
      console.error("Error:", error);
    }
  }
</script>

{#if isLoading}
  <Container>
    <div
      class="border-border h-20 w-20 animate-spin rounded-full border-[12px] border-t-primary"
    />
  </Container>
{:else}
  <div class="flex items-start justify-end p-4">
    <Button on:click={toggleMode} variant="outline" size="sm">
      <span class="hidden dark:flex">Dark</span>
      <span class="dark:hidden">Light</span>
    </Button>
  </div>
  <Container>
    <H1>Have you ever wondered how controversial your anime taste is?"</H1>
    <div class="space-y-4">
      <H3>Find out by entering your AniList username below...</H3>
      <form class="flex flex-col w-full" on:submit={handleSubmit}>
        <div class="flex space-x-2">
          <Input placeholder="username" bind:value={username} required />
          <Button type="submit">Submit</Button>
        </div>
        <div class="flex items-center space-x-2 mt-2">
          <Checkbox
            class="peer"
            id="manga"
            bind:checked={isChecked}
            aria-labelledby="manga-label"
          />
          <Label
            class="transition text-base {labelClass}"
            id="manga-label"
            for="manga">I want manga insights instead!</Label
          >
        </div>
      </form>
    </div>
  </Container>
{/if}
