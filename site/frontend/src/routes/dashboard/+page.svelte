<script lang="ts">
  import type { PageData } from "./$types";
  import { onMount } from "svelte";
  import { page } from "$app/state";

  import * as Card from "$lib/components/ui/card";
  import * as Table from "$lib/components/ui/table";
  import * as Dialog from "$lib/components/ui/dialog";
  import { Button } from "$lib/components/ui/button";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";

  import H2 from "$lib/components/H2.svelte";

  import DashboardContainer from "$lib/components/DashboardContainer.svelte";
  import ImageCard from "$lib/components/ImageCard.svelte";
  import SectionHeader from "$lib/components/SectionHeader.svelte";
  import AnimatedScroll from "$lib/components/AnimatedScroll.svelte";

  import Bar from "$lib/components/Bar.svelte";
  import DoubleBar from "$lib/components/DoubleBar.svelte";
  import HorizontalBar from "$lib/components/HorizontalBar.svelte";

  import ScrollArrow from "$lib/components/ScrollArrow.svelte";

  export let data: PageData;

  const username = page.url.searchParams.get("username");

  function copyURL() {
    const currentURL = window.location.href;
    navigator.clipboard.writeText(currentURL).then(() => {
      return toast.info("Copied URL to clipboard!");
    });
  }

  let block = "center";
  let up = false;

  function* getValidElements() {
    while (true) {
      const elements = Array.from(
        document.getElementsByClassName(
          "flex flex-col items-center justify-center m-auto w-full max-w-screen-lg p-4 min-h-screen",
        ),
      ).slice(1);
      for (let [i, item] of elements.entries()) {
        if (i == 4) {
          block = "start";
          up = false;
          yield item;
        } else if (i == 6) {
          up = true;
          yield item;
        } else {
          block = "center";
          up = false;
          yield item;
        }
      }
    }
  }

  const g = getValidElements();

  let valueAbs = 0;
  let valueAvg = 0;
  onMount(() => {
    valueAbs = data.insights.absScoreDiff;
    valueAvg = data.insights.avgScoreDiff;
  });
</script>

<!--<div class="hidden md:flex sticky z-10 md:top-[45.5%] h-0">-->
<!--  <ScrollArrow class="absolute z-10 md:right-0 pr-8" {g} {block} {up} />-->
<!--</div>-->

<!-- TODO: Add nice animation to this, like have it fall onto the screen when people load in or something-->
<section>
  <AnimatedScroll duration="3s">
    <DashboardContainer class="min-h-[40vh]">
      <H2 class="text-primary text-center text-6xl">
        welcome to popularity tool for anilist.
      </H2>
      <H2 class="text-primary text-center text-6xl border-none">
        let's see how controversial your anime taste is...
      </H2>
    </DashboardContainer>
  </AnimatedScroll>
</section>

<section class="bg-band">
  <AnimatedScroll duration="5s">
    <DashboardContainer class="space-y-6">
      <H2 class="text-center text-background border-background text-6xl">
        your overall taste
      </H2>
      <section class="m-auto w-full">
        <Card.Root class="overflow-x-auto border-primary">
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
            <DoubleBar
              data={data.insights.userData}
              y1="user_count"
              y2="average_count"
              x="score"
            />
          </Card.Content>
        </Card.Root>
      </section>
    </DashboardContainer>
  </AnimatedScroll>
</section>

<section>
  <AnimatedScroll>
    <DashboardContainer
      class="space-y-6 max-w-screen-lg md:max-w-full"
      maxWidth={false}
    >
      <H2 class="text-center text-band border-band text-6xl">
        compared to other users
      </H2>
      <div
        class="flex flex-col m-auto w-full gap-6 md:w-auto md:grid md:grid-cols-2 md:grid-rows-2"
      >
        <Card.Root
          class="overflow-x-auto md:col-start-1 md:row-start-1 md:translate-x-40"
        >
          <Card.Header>
            <Card.Title class="text-4xl text-primary">
              Overall Score Difference
            </Card.Title>
            <Card.Description>
              How controversial your scores are compared to the average user.
            </Card.Description>
          </Card.Header>
          <Card.Content class="inline-flex">
            <Bar
              data={data.insights.absData}
              x="abs_score_diff"
              y="count"
              scoreVariable={data.insights.absScoreDiff}
              colorX1="fill-primary"
              colorX2="fill-plot-accent"
              xLabel="Difference"
              diverging={false}
            />
          </Card.Content>
        </Card.Root>

        <Card.Root
          class="overflow-x-auto md:col-start-2 md:row-start-2 md:-translate-x-40"
        >
          <Card.Header>
            <Card.Title class="text-4xl">
              <span class="text-plot-accent">Positivity</span>/<span
                class="text-destructive">Negativity</span
              >
            </Card.Title>
            <Card.Description>
              How positive your scores are compared to the average user.
            </Card.Description>
          </Card.Header>
          <Card.Content class="inline-flex">
            <Bar
              data={data.insights.avgData}
              x="avg_score_diff"
              y="count"
              scoreVariable={data.insights.avgScoreDiff}
              colorX1="fill-plot-accent"
              colorX2="fill-destructive"
              xLabel="Positive"
              diverging={true}
            />
          </Card.Content>
        </Card.Root>
      </div>
    </DashboardContainer>
  </AnimatedScroll>
</section>

<section class="bg-band">
  <AnimatedScroll>
    <DashboardContainer class="space-y-6">
      <H2 class="text-center text-background border-background text-6xl">
        specific takes
      </H2>
      <section
        class="flex flex-col gap-3 md:grid md:grid-cols-2 md:grid-rows-1"
      >
        <ImageCard
          title="Your Hottest Take"
          description="The show you scored most differently compared to the AniList average."
          animeTitle={data.insights.titleMax}
          image={data.insights.imageMax}
          userScore={data.insights.userMaxScore}
          avgScore={data.insights.avgMaxScore}
          borderColour="border-destructive"
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
          borderColour="border-primary"
          textColour="text-primary"
          {username}
        ></ImageCard>
      </section>
    </DashboardContainer>
  </AnimatedScroll>
</section>

<section>
  <AnimatedScroll>
    <DashboardContainer class="space-y-6">
      <H2 class="text-center text-band border-band text-6xl"
        >your genre opinions</H2
      >
      <div class="m-auto w-full">
        <Card.Root class="overflow-x-auto">
          <Card.Header>
            <Card.Title>
              <span class="text-primary">{username}</span> vs.
              <span class="text-plot-accent">the AniList Average</span> (by genre)
            </Card.Title>
            <Card.Description>
              Which genre do you love (or hate) the most?
            </Card.Description>
          </Card.Header>
          <Card.Content class="space-y-6">
            <div class="inline-flex">
              <HorizontalBar
                data={data.insights.genreData}
                x1="weighted_average"
                x2="weighted_user"
              />
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

  <AnimatedScroll>
    <DashboardContainer>
      <div class="grid grid-cols-2 grid-rows-2 gap-4">
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
        <Button class="col-span-2" variant="outline" href="/"
          >Return Home</Button
        >
      </div>
    </DashboardContainer>
  </AnimatedScroll>
</section>

<Toaster richColors position="bottom-right" />
