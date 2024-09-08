<script>
  import { onMount } from 'svelte';

  let insights = {};

  onMount(() => {
    const storedInsights = sessionStorage.getItem('insights');
    if (storedInsights) {
      insights = JSON.parse(storedInsights);
    }
  });
</script>

<div class="container mx-auto p-4">
  <h1 class="text-2xl font-bold mb-4">Your AniList Insights</h1>
  
  {#if Object.keys(insights).length > 0}
    {#each Object.entries(insights) as [key, value]}
      <div class="mb-4">
        <h2 class="text-xl font-semibold">{key}</h2>
        <p>{value}</p>
      </div>
    {/each}
  {:else}
    <p>No insights available. Please go back and submit your username.</p>
  {/if}
</div>
