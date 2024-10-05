<script lang="ts">
  import { page } from "$app/stores";
  import H2 from "$lib/components/H2.svelte";
  import H3 from "$lib/components/H3.svelte";
  import DashboardContainer from "$lib/components/DashboardContainer.svelte";
  import { Button } from "$lib/components/ui/button";
</script>

<DashboardContainer>
  <div class="max-w-[40rem]">
    <H2 class="text-destructive text-4xl text-center">{$page.status}</H2>
    <H3 class="text-destructive text-2xl text-center">{$page.error?.message}</H3
    >
  </div>
  <img
    src="https://media1.tenor.com/m/v_bRv4rdmqMAAAAd/lain.gif"
    class="flex border-solid border-2 border-border rounded-xl w-full max-w-lg m-8"
    alt="lain hand releasing smoke"
  />
  <Button variant="outline" href="/">Return Home</Button>
</DashboardContainer>
