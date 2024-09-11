<script lang="ts">
  import { onMount } from "svelte";
  import * as Card from "$lib/components/ui/card";

  import { Button } from "$lib/components/ui/button";
  import { toggleMode } from "mode-watcher";

  import DashboardContainer from "$lib/components/DashboardContainer.svelte";

  import ImageCard from "$lib/components/ImageCard.svelte";

  let width = 400;
  let height = 400;

  let insights = {} as {
    absScoreDiff: number;
    avgScoreDiff: number;
    userMinScore: number;
    userMaxScore: number;
    avgMinScore: number;
    avgMaxScore: number;
    titleMin: string;
    titleMax: string;
    imageMin: string;
    imageMax: string;
    userData: Array<JSON>;
  };

  let data = [] as Array<{
    user_id: number;
    anime_id: number;
    user_score: number;
  }>;

  onMount(() => {
    setTimeout(() => {
      const storedInsights = sessionStorage.getItem("insights");
      if (storedInsights) {
        insights = JSON.parse(storedInsights);
        data = insights.userData;
      }
    }, 0);
  });
</script>

<div class="flex items-start justify-end p-4">
  <Button on:click={toggleMode} variant="outline" size="sm">
    <span class="hidden dark:flex">Dark</span>
    <span class="dark:hidden">Light</span>
  </Button>
</div>
<DashboardContainer>
  <Card.Root>
    <Card.Header>
      <Card.Title>Absolute Score Difference</Card.Title>
      <Card.Description
        >How far your scores are from the average, regardless of whether you
        rate higher or lower.</Card.Description
      >
    </Card.Header>
    <Card.Content>
      <p>{insights.absScoreDiff}</p>
    </Card.Content>
  </Card.Root>
  <Card.Root>
    <Card.Header>
      <Card.Title>Average Score Difference</Card.Title>
      <Card.Description
        >Whether you tend to rate anime higher or lower than average.</Card.Description
      >
    </Card.Header>
    <Card.Content>
      <p>{insights.avgScoreDiff}</p>
    </Card.Content>
  </Card.Root>
  <ImageCard
    title="Your Coldest Take"
    description="The most popular score you've given."
    animeTitle={insights.titleMin}
    image={insights.imageMin}
    userScore={insights.userMinScore}
    avgScore={insights.avgMinScore}
  ></ImageCard>
  <ImageCard
    title="Your Hottest Take"
    description="The most unpopular score you've given."
    animeTitle={insights.titleMax}
    image={insights.imageMax}
    userScore={insights.userMaxScore}
    avgScore={insights.avgMaxScore}
  ></ImageCard>
  {#each data as item}
    {item.anime_id}, {item.user_score}, {item.user_id}
    <br />
  {/each}
</DashboardContainer>
