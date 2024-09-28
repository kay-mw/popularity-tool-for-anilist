<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Checkbox } from "$lib/components/ui/checkbox";
  import { Label } from "$lib/components/ui/label";

  import Container from "$lib/components/Container.svelte";
  import H1 from "$lib/components/H1.svelte";
  import H3 from "$lib/components/H3.svelte";

  let manga = false;
  let username = "";

  $: labelClass = manga ? "text-primary" : "text-current";
</script>

<Container>
  <H1 class="text-primary">Have you ever wondered how controversial your anime taste is?</H1>
  <div class="space-y-4">
    <H3>Find out by entering your AniList username below...</H3>
    <form action="/dashboard" class="flex flex-col w-full">
      <div class="flex space-x-2">
        <Input
          placeholder="username"
          name="username"
          bind:value={username}
          required
        />
        <Button type="submit">Submit</Button>
      </div>
      <div class="flex items-center space-x-2 mt-2">
        <input type="checkbox" id="manga" name="manga" bind:checked={manga} />
        <!--<Checkbox class="peer" id="manga" name="manga" bind:checked={manga} />-->
        <Label
          class="transition text-base {labelClass}"
          id="manga-label"
          for="manga">I want manga insights instead!</Label
        >
      </div>
    </form>
  </div>
</Container>
<!--<Container>-->
<!--  <div-->
<!--    class="border-border h-20 w-20 animate-spin rounded-full border-[12px] border-t-primary"-->
<!--  />-->
<!--</Container>-->
<!--Redirect with URL params.-->
<!--Run page load function on dashboard that gets data with URL params.-->
<!--Show loader while awaiting.-->
<!--Display data!-->
