<script lang="ts">
  import type { PageData } from "./$types";
  import { onMount } from "svelte";

  import * as Card from "$lib/components/ui/card";
  import * as Table from "$lib/components/ui/table";
  import * as Dialog from "$lib/components/ui/dialog";
  import { Button } from "$lib/components/ui/button";
  import { Progress } from "$lib/components/ui/progress";
  import { Separator } from "$lib/components/ui/separator";
  import { ScrollArea } from "$lib/components/ui/scroll-area";

  import DashboardContainer from "$lib/components/DashboardContainer.svelte";
  import ImageCard from "$lib/components/ImageCard.svelte";
  import H2 from "$lib/components/H2.svelte";

  import Bar from "$lib/components/Bar.svelte";
  import HorizontalBar from "$lib/components/HorizontalBar.svelte";

  export let data: PageData;

  let valueAbs = 0;
  let valueAvg = 0;
  onMount(() => {
    valueAbs = data.insights.absScoreDiff;
    valueAvg = data.insights.avgScoreDiff;
  });
</script>

<DashboardContainer>
  <Card.Root>
    <Card.Header>
      <Card.Title class="title">Absolute Score Difference</Card.Title>
      <Card.Description
        >How far your scores are from the average, regardless of whether you
        rate higher or lower.
      </Card.Description>
    </Card.Header>
    <Card.Content>
      <Progress value={valueAbs} max={10} />
    </Card.Content>
  </Card.Root>
  <Card.Root>
    <Card.Header>
      <Card.Title class="title">Average Score Difference</Card.Title>
      <Card.Description>
        Whether you tend to rate anime higher or lower than average.
      </Card.Description>
    </Card.Header>
    <Card.Content>
      <Progress value={valueAvg} max={50} />
    </Card.Content>
  </Card.Root>
  <div class="grid grid-cols-2 grid-rows-1 max-w-xl gap-6">
    <ImageCard
      title="Your Hottest Take"
      description="Your most 'unpopular' score."
      animeTitle={data.insights.titleMax}
      image={data.insights.imageMax}
      userScore={data.insights.userMaxScore}
      avgScore={data.insights.avgMaxScore}
      titleColour="text-destructive"
    ></ImageCard>
    <ImageCard
      title="Your Coldest Take"
      description="Your most 'popular' score."
      animeTitle={data.insights.titleMin}
      image={data.insights.imageMin}
      userScore={data.insights.userMinScore}
      avgScore={data.insights.avgMinScore}
      titleColour="text-primary"
    ></ImageCard>
  </div>
</DashboardContainer>

<div class="items-center justify-center m-auto w-full max-w-[60rem]">
  <Card.Root>
    <Card.Header>
      <Card.Title class="text-2xl text-center">
        <span class="text-primary">Your Scores</span> vs.
        <span class="text-plot-accent">the AniList Average</span>
      </Card.Title>
    </Card.Header>
    <Card.Content class="pl-6 pr-6 pb-6">
      <Bar {data} />
    </Card.Content>
  </Card.Root>
</div>

<DashboardContainer>
  <Separator class="mb-4" />
  <Card.Root>
    <Card.Header>
      <Card.Title>Score Difference by Genre</Card.Title>
      <Card.Description>
        Which genre do you love (or hate) the most?
      </Card.Description>
    </Card.Header>
    <Card.Content>
      <H2 class="text-primary text-2xl">{data.insights.genreMaxTitle} Anime</H2>
      {#if data.insights.genreMax > 0}
        <p class="pt-3 text-base">
          Specifically, you <span class="text-plot-accent font-bold">love</span>
          {data.insights.genreMaxTitle} shows more than most users, scoring them
          {data.insights.genreMax} points higher on average.
        </p>
      {:else}
        <p class="pt-3">
          Specifically, you <span class="text-destructive font-bold">hate</span>
          {data.insights.genreMaxTitle} shows more than most users, scoring them
          {data.insights.genreMax} points lower on average.
        </p>
      {/if}
    </Card.Content>
  </Card.Root>
  <ImageCard
    title="Your Hottest {data.insights.genreMaxTitle} Take"
    description=""
    animeTitle={data.insights.genreDiffTitle}
    image={data.insights.imageGenre}
    userScore={data.insights.genreDiffUser}
    avgScore={data.insights.genreDiffAvg}
    titleColour="text-base"
  ></ImageCard>
</DashboardContainer>

<div class="items-center justify-center m-auto min-w-[30rem] max-w-[60rem]">
  <Card.Root>
    <Card.Header>
      <Card.Title class="text-2xl text-center">
        <span class="text-primary">Your Genre Scores</span> vs.
        <span class="text-plot-accent">the AniList Average</span>
      </Card.Title>
    </Card.Header>
    <Card.Content class="pl-6 pr-6 pb-6">
  <HorizontalBar {data} />
    </Card.Content>
  </Card.Root>
</div>

<DashboardContainer>
  <Dialog.Root>
    <Dialog.Trigger>
      <Button>All Scores</Button>
    </Dialog.Trigger>
    <Dialog.Content
      class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 max-w-2xl max-h-[80vh] rounded-lg shadow-xl flex flex-col"
    >
      <Dialog.Header>
        <Dialog.Title class="text-lg font-semibold">Scores</Dialog.Title>
        <Dialog.Description class="mt-2 text-sm text-gray-500">
          All your scores, ordered from most to least controversial.
        </Dialog.Description>
      </Dialog.Header>
      <div class="flex-grow overflow-auto p-6 pt-4">
        <Table.Root class="w-full">
          <Table.Header>
            <Table.Row>
              <Table.Head class="w-full">Title</Table.Head>
              <Table.Head class="text-right">Score Difference</Table.Head>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {#each data.insights.tableData as row}
              <Table.Row>
                <Table.Cell class="text-primary">{row.title_romaji}</Table.Cell>
                <Table.Cell class="text-right text-plot-accent"
                  >{row.score_diff}</Table.Cell
                >
              </Table.Row>
            {/each}
          </Table.Body>
        </Table.Root>
      </div>
      <Dialog.Footer>
        <Dialog.Close>
          <Button>Close</Button>
        </Dialog.Close>
      </Dialog.Footer>
    </Dialog.Content>
  </Dialog.Root>
</DashboardContainer>


<DashboardContainer>
  <div class="flex flex-col">
    <Button href="/">Return Home</Button>
  </div>
</DashboardContainer>

<style lang="postcss">
.title {
  @apply text-5xl
}
</style>
