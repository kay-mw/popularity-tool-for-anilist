<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  import { toggleMode } from "mode-watcher";

  //import * as Card from "$lib/components/ui/card";
  import { Button } from "$lib/components/ui/button";

  //import Container from "$lib/components/Container.svelte";
  //import DashboardContainer from "$lib/components/DashboardContainer.svelte";
  //import ImageCard from "$lib/components/ImageCard.svelte";

  import Scatter from "$lib/components/Scatter.svelte";
  import Axis from "$lib/components/Axis.svelte";

  //import { scaleLinear } from "d3-scale";
  //import { max, min } from "d3-array";
  //import { line } from "d3-shape";

  let width = 600;
  let height = 600;
  let extraTopMargin = 15;

  const margin = { top: 0, right: 30, left: 10, bottom: 0 };

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
    userData: Array<{
      user_score: number;
      user_count: number;
      average_score: number;
      average_count: number;
    }>;
  };

  let data = [] as Array<{
    user_score: number;
    user_count: number;
    average_score: number;
    average_count: number;
  }>;

  let username = "" as string | null;

  onMount(() => {
    const storedInsights = sessionStorage.getItem("insights");
    username = sessionStorage.getItem("username");

    if (storedInsights) {
      insights = JSON.parse(storedInsights);
      data = insights.userData;
      console.log(data);
    }
  });

  //type DataPoint = {
  //  user_score: number;
  //  user_count: number;
  //  average_score: number;
  //  average_count: number;
  //};
  //
  //$: ymax = max([
  //  max(data, (d) => d.user_count ?? 0) ?? 0,
  //  max(data, (d) => d.average_count ?? 0) ?? 0,
  //]);
  //
  //$: xmin = min([
  //  min(
  //    data.filter((d) => d.user_count > 0),
  //    (d) => d.user_score ?? 0,
  //  ) ?? 0,
  //  min(
  //    data.filter((d) => d.average_count > 0),
  //    (d) => d.average_score ?? 0,
  //  ) ?? 0,
  //]);
  //
  //$: xScale = scaleLinear()
  //  .domain([0, 100])
  //  .range([0, width - margin.right]);
  //$: yScale = scaleLinear()
  //  .domain([0, ymax ?? 0])
  //  .range([height - margin.top - margin.bottom, 0]);
  //
  //$: svgHeight = height + extraTopMargin;
  //
  //$: userLine = line<DataPoint>()
  //  .x((d) => xScale(d.user_score))
  //  .y((d) => yScale(d.user_count));
  //
  //$: averageLine = line<DataPoint>()
  //  .x((d) => xScale(d.average_score))
  //  .y((d) => yScale(d.average_count));
  //
  //$: userData = data.filter((d) => d.user_count > 0);
  //$: averageData = data.filter((d) => d.average_count > 0);
  //
  //let hoveredData: (typeof data)[0] | null = null;
  //
  async function returnHome() {
    goto("/");
  }
</script>

<div class="flex items-start justify-end p-4">
  <Button on:click={toggleMode} variant="outline" size="sm">
    <span class="hidden dark:flex">Dark</span>
    <span class="dark:hidden">Light</span>
  </Button>
</div>
<Scatter {data} />

<!--- Add legend.-->
<!--Add animations to tooltip (preferably with tailwind).-->
<!--Add line to separate y-axis from plot.-->
<!--Find nice, complementary colour to replace fill-destructive.-->
<!--Convert from line to scatter (or line WITH scatter).-->
<!--Add axis labels.-->
<!--<div-->
<!--  bind:clientWidth={width}-->
<!--  on:mouseleave={() => {-->
<!--    hoveredData = null;-->
<!--  }}-->
<!--  role="figure"-->
<!--  class="flex container justify-center items-center max-h-[50rem] max-w-[50rem]"-->
<!-->-->
<!--  <svg {width} height={svgHeight} viewBox="0 0 {width} {svgHeight}">-->
<!--    <g-->
<!--      class="chart"-->
<!--      transform="translate({margin.left}, {margin.top + extraTopMargin})"-->
<!--    >-->
<!--      <AxisX {xmin} {height} {xScale} {margin} />-->
<!--      <AxisY {ymax} {width} {yScale} {margin} />-->
<!--      <path-->
<!--        d={userLine(userData)}-->
<!--        class="stroke-primary fill-none"-->
<!--        stroke-width="2"-->
<!--      />-->
<!--      <path-->
<!--        d={averageLine(averageData)}-->
<!--        class="stroke-plot-accent fill-none"-->
<!--        stroke-width="2"-->
<!--      />-->
<!--      {#each data as item}-->
<!--        {#if item.user_count > 0}-->
<!--          <circle-->
<!--            class="fill-primary stroke-border"-->
<!--            cx={xScale(item.user_score)}-->
<!--            cy={yScale(item.user_count)}-->
<!--            r={hoveredData && hoveredData == item ? "10" : "5"}-->
<!--            on:mouseover={() => {-->
<!--              hoveredData = item;-->
<!--            }}-->
<!--            on:focus={() => {-->
<!--              hoveredData = item;-->
<!--            }}-->
<!--            tabIndex="0"-->
<!--            role="figure"-->
<!--          />-->
<!--        {/if}-->
<!--        {#if item.average_count > 0}-->
<!--          <circle-->
<!--            class="fill-plot-accent stroke-border"-->
<!--            cx={xScale(item.average_score)}-->
<!--            cy={yScale(item.average_count)}-->
<!--            r={hoveredData && hoveredData == item ? "10" : "5"}-->
<!--            on:mouseover={() => {-->
<!--              hoveredData = item;-->
<!--            }}-->
<!--            on:focus={() => {-->
<!--              hoveredData = item;-->
<!--            }}-->
<!--            tabIndex="0"-->
<!--            role="figure"-->
<!--          />-->
<!--        {/if}-->
<!--      {/each}-->
<!--    </g>-->
<!--  </svg>-->
<!--    <Legend {username} />-->
<!--</div>-->
<!---->
<!--<DashboardContainer>-->
<!--  <Card.Root>-->
<!--    <Card.Header>-->
<!--      <Card.Title>Absolute Score Difference</Card.Title>-->
<!--      <Card.Description-->
<!--        >How far your scores are from the average, regardless of whether you-->
<!--        rate higher or lower.</Card.Description-->
<!--      >-->
<!--    </Card.Header>-->
<!--    <Card.Content>-->
<!--      <p>{insights.absScoreDiff}</p>-->
<!--    </Card.Content>-->
<!--  </Card.Root>-->
<!--  <Card.Root>-->
<!--    <Card.Header>-->
<!--      <Card.Title>Average Score Difference</Card.Title>-->
<!--      <Card.Description-->
<!--        >Whether you tend to rate anime higher or lower than average.</Card.Description-->
<!--      >-->
<!--    </Card.Header>-->
<!--    <Card.Content>-->
<!--      <p>{insights.avgScoreDiff}</p>-->
<!--    </Card.Content>-->
<!--  </Card.Root>-->
<!--  <ImageCard-->
<!--    title="Your Coldest Take"-->
<!--    description="The most popular score you've given."-->
<!--    animeTitle={insights.titleMin}-->
<!--    image={insights.imageMin}-->
<!--    userScore={insights.userMinScore}-->
<!--    avgScore={insights.avgMinScore}-->
<!--  ></ImageCard>-->
<!--  <ImageCard-->
<!--    title="Your Hottest Take"-->
<!--    description="The most unpopular score you've given."-->
<!--    animeTitle={insights.titleMax}-->
<!--    image={insights.imageMax}-->
<!--    userScore={insights.userMaxScore}-->
<!--    avgScore={insights.avgMaxScore}-->
<!--  ></ImageCard>-->
<!--  <Button class="col-span-2" on:click={returnHome}>Return Home</Button>-->
<!--</DashboardContainer>-->
