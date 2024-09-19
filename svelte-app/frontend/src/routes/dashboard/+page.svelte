<script lang="ts">
  import type { PageData } from "./$types";
  import { onMount } from "svelte";

  import * as Card from "$lib/components/ui/card";
  import { Button } from "$lib/components/ui/button";

  import DashboardContainer from "$lib/components/DashboardContainer.svelte";
  import ImageCard from "$lib/components/ImageCard.svelte";

  import Scatter from "$lib/components/Scatter.svelte";

  import { Progress } from "$lib/components/ui/progress";

  export let data: PageData;

  console.log(data);

  let value = data.insights.absScoreDiff

  onMount(() => {
    const timer = setTimeout(() => (value = data.insights.absScoreDiff), 500);
    return () => clearTimeout(timer);
  })
</script>

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
      <Progress {value} max={5} />
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
      <p>{data.insights.avgScoreDiff}</p>
    </Card.Content>
  </Card.Root>
  <ImageCard
    title="Your Coldest Take"
    description="The most popular score you've given."
    animeTitle={data.insights.titleMin}
    image={data.insights.imageMin}
    userScore={data.insights.userMinScore}
    avgScore={data.insights.avgMinScore}
  ></ImageCard>
  <ImageCard
    title="Your Hottest Take"
    description="The most unpopular score you've given."
    animeTitle={data.insights.titleMax}
    image={data.insights.imageMax}
    userScore={data.insights.userMaxScore}
    avgScore={data.insights.avgMaxScore}
  ></ImageCard>
</DashboardContainer>

<!--<div class="flex max-h-0.5 items-center justify-center">-->
<!--  <Card.Root>-->
<!--    <Card.Content>-->
<!--      <Scatter data={data.insights.userData} />-->
<!--    </Card.Content>-->
<!--  </Card.Root>-->
<!--</div>-->

<!--<div class="absolute bottom-0 left-1/2 right-1/2">-->
<!--  <Button href="/">Return Home</Button>-->
<!--</div>-->
