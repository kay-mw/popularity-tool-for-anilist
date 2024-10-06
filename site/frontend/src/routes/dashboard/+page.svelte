<script lang="ts">
  import type { PageData } from "./$types";
  import { onMount } from "svelte";
  import { page } from "$app/stores";

  import * as Card from "$lib/components/ui/card";
  import * as Table from "$lib/components/ui/table";
  import * as Dialog from "$lib/components/ui/dialog";
  import { Button } from "$lib/components/ui/button";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import { Separator } from "$lib/components/ui/separator";

  import DashboardContainer from "$lib/components/DashboardContainer.svelte";
  import ImageCard from "$lib/components/ImageCard.svelte";
  import H1 from "$lib/components/H1.svelte";
  import H2 from "$lib/components/H2.svelte";
  import SectionHeader from "$lib/components/SectionHeader.svelte";
  import AvgCard from "$lib/components/AvgCard.svelte";
  import AbsCard from "$lib/components/AbsCard.svelte";
  import AnimatedScroll from "$lib/components/AnimatedScroll.svelte";

  import Bar from "$lib/components/Bar.svelte";
  import HorizontalBar from "$lib/components/HorizontalBar.svelte";

  export let data: PageData;

  const username = $page.url.searchParams.get("username");

  function copyURL() {
    const currentURL = window.location.href;
    navigator.clipboard.writeText(currentURL).then(() => {
      return toast.info("Copied URL to clipboard!");
    });
  }

  let valueAbs = 0;
  let valueAvg = 0;
  onMount(() => {
    valueAbs = data.insights.absScoreDiff;
    valueAvg = data.insights.avgScoreDiff;
  });
</script>

<section class="space-y-[50vw]">
  <AnimatedScroll>
    <DashboardContainer>
      <SectionHeader header="your overall taste" />
    </DashboardContainer>
  </AnimatedScroll>
  <AnimatedScroll>
    <DashboardContainer>
      {#if Math.floor(valueAbs) < 5}
        <AbsCard
          {valueAbs}
          colour="primary"
          image="https://media1.tenor.com/m/YjiuFd-KUVQAAAAC/one-piece-one-piece-movie-9.gif"
          alt="chopper lying in snow"
          descriptor="chillin"
          emphasis="only"
        />
      {:else if Math.floor(valueAbs) <= 10}
        <AbsCard
          {valueAbs}
          colour="red-400"
          image="https://cdn.midjourney.com/b5d8c3da-776d-4a6e-a40b-381eac63862c/0_1.png"
          alt="roy mustang snapping fingers"
          descriptor="heating up...!"
          emphasis="a solid"
        />
      {:else if Math.floor(valueAbs) < 20}
        <AbsCard
          {valueAbs}
          colour="destructive"
          image="https://media1.tenor.com/m/862gCSNfYggAAAAd/kyojuro-rengoku-9th-form-rengoku.gif"
          alt="rengoku conjuring fire"
          descriptor="SCALDING"
          emphasis="a WHOPPING"
        />
      {:else}
        <AbsCard
          {valueAbs}
          colour="destructive"
          image="https://media1.tenor.com/m/TYpc9J_jeRUAAAAd/sukuna-fire-arrow.gif"
          alt="sukuna conjuring fire arrow"
          descriptor="fire arrow"
          emphasis="a MASSIVE"
        />
      {/if}
    </DashboardContainer>
  </AnimatedScroll>

  <AnimatedScroll>
    <DashboardContainer>
      {#if valueAvg > 0}
        <AvgCard
          {valueAvg}
          accentColour="text-plot-accent"
          valueDirection="higher"
          image="https://media.tenor.com/q27KhS9kKmwAAAAi/dazai-liar-dancer.gif"
          alt="dazai dancing"
          descriptor="enjoyer"
        />
      {:else}
        <AvgCard
          {valueAvg}
          accentColour="text-destructive"
          valueDirection="lower"
          image="https://media1.tenor.com/m/9C-wnbKI-IQAAAAd/death-note.gif"
          alt="yamagi light frantically writing"
          descriptor="destroyer"
        />
      {/if}
    </DashboardContainer>
  </AnimatedScroll>

  <AnimatedScroll>
    <DashboardContainer>
      <section class="m-auto w-full">
        <Card.Root class="overflow-x-auto">
          <Card.Header>
            <Card.Title class="text-4xl">
              <span class="text-primary">{username}</span> vs.
              <span class="text-plot-accent">the AniList Average</span>
            </Card.Title>
            <Card.Description>
              How frequently you give certain scores compared to the AniList
              average.
            </Card.Description>
          </Card.Header>
          <Card.Content class="inline-flex">
            <Bar {data} />
          </Card.Content>
        </Card.Root>
      </section>
    </DashboardContainer>
  </AnimatedScroll>

  <AnimatedScroll>
    <DashboardContainer>
      <section class="flex flex-col md:grid md:grid-cols-2 md:grid-rows-1 md:gap-3">
        <ImageCard
          title="Your Hottest Take"
          description="The show you scored most differently compared to the AniList average."
          animeTitle={data.insights.titleMax}
          image={data.insights.imageMax}
          userScore={data.insights.userMaxScore}
          avgScore={data.insights.avgMaxScore}
          textColour="text-destructive"
          {username}
        ></ImageCard>
        <ImageCard
          title="Your Coldest Take"
          description="The show you scored least differently compared to the AniList average."
          animeTitle={data.insights.titleMin}
          image={data.insights.imageMin}
          userScore={data.insights.userMinScore}
          avgScore={data.insights.avgMinScore}
          textColour="text-primary"
          {username}
        ></ImageCard>
      </section>
    </DashboardContainer>
  </AnimatedScroll>

  <AnimatedScroll>
    <DashboardContainer>
      <SectionHeader header="your genre opinions" arrow={false} />
    </DashboardContainer>
  </AnimatedScroll>

  <AnimatedScroll>
    <DashboardContainer>
      <div class="m-auto w-full">
        <Card.Root class="overflow-x-auto">
          <Card.Header>
            <Card.Title
              class={data.insights.genreMax > 0
                ? "text-plot-accent"
                : "text-destructive"}>Score Difference by Genre</Card.Title
            >
            <Card.Description>
              Which genre do you love (or hate) the most?
            </Card.Description>
          </Card.Header>
          <Card.Content class="space-y-6">
            <H2
              class="{data.insights.genreMax > 0
                ? 'text-plot-accent'
                : 'text-destructive'} text-2xl"
              >{data.insights.genreMaxTitle}</H2
            >
            {#if data.insights.genreMax > 0}
              <p class="text-xl">
                Specifically, you <span class="text-plot-accent font-bold"
                  >love</span
                >
                {data.insights.genreMaxTitle} shows more than most users, scoring
                them
                {data.insights.genreMax} points higher on average.
              </p>
            {:else}
              <p class="text-xl">
                Specifically, you <span class="text-destructive font-bold"
                  >hate</span
                >
                {data.insights.genreMaxTitle} shows more than most users, scoring
                them
                <span class="text-destructive font-bold"
                  >{Math.abs(data.insights.genreMax)} points</span
                > lower on average.
              </p>
            {/if}
            <Separator />
            <h1
              class="text-2xl font-semibold leading-none tracking-tight text-center"
            >
              <span class="text-primary">{username}</span> vs.
              <span class="text-plot-accent">the AniList Average</span> (by genre)
            </h1>
            <div class="inline-flex">
              <HorizontalBar {data} />
            </div>
          </Card.Content>
        </Card.Root>
      </div>
    </DashboardContainer>
  </AnimatedScroll>

  <AnimatedScroll>
    <DashboardContainer>
      <ImageCard
        title="Your Hottest {data.insights.genreMaxTitle} Take"
        description="The {data.insights
          .genreMaxTitle} show you scored most differently compared to the AniList average."
        animeTitle={data.insights.genreDiffTitle}
        image={data.insights.imageGenre}
        userScore={data.insights.genreDiffUser}
        avgScore={data.insights.genreDiffAvg}
        textColour={data.insights.genreDiffUser > data.insights.genreDiffAvg
          ? "text-primary"
          : "text-destructive"}
        {username}
      ></ImageCard>
    </DashboardContainer>
  </AnimatedScroll>
</section>

<Toaster richColors position="bottom-right" />

<div class="flex justify-center mt-32">
  <AnimatedScroll>
    <div
      class="grid grid-cols-2 grid-rows-2 justify-center items-center m-auto w-full gap-4 p-8 max-w-screen-lg"
    >
      <Dialog.Root>
        <Dialog.Trigger>
          <Button>See All My Scores</Button>
        </Dialog.Trigger>
        <Dialog.Content
          class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 max-w-2xl max-h-[80vh] rounded-lg shadow-xl flex flex-col"
        >
          <Dialog.Header>
            <Dialog.Title>Scores</Dialog.Title>
            <Dialog.Description>
              All your scores, ordered from most to least controversial.
            </Dialog.Description>
          </Dialog.Header>
          <div class="flex-grow overflow-auto p-6 pt-4">
            <Table.Root class="w-full">
              <Table.Header>
                <Table.Row>
                  <Table.Head>Title</Table.Head>
                  <Table.Head>{username}</Table.Head>
                  <Table.Head>AniList</Table.Head>
                  <Table.Head>Difference</Table.Head>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                {#each data.insights.tableData as row}
                  <Table.Row>
                    <Table.Cell class="text-current"
                      >{row.title_romaji}</Table.Cell
                    >
                    <Table.Cell class="text-primary"
                      >{row.user_score}</Table.Cell
                    >
                    <Table.Cell class="text-plot-accent"
                      >{row.average_score}</Table.Cell
                    >
                    <Table.Cell class="text-destructive"
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

      <Button on:click={copyURL}>Share</Button>

      <Button class="col-span-2" variant="outline" href="/">Return Home</Button>
    </div>
  </AnimatedScroll>
</div>
