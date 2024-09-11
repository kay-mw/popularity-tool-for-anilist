<script lang="ts">
  import { onMount } from "svelte";
  import * as Card from "$lib/components/ui/card";

  import Container from "$lib/components/Container.svelte";

  let insights = {} as {
    absScoreDiff: number;
  };

  onMount(() => {
    const storedInsights = sessionStorage.getItem("insights");
    if (storedInsights) {
      insights = JSON.parse(storedInsights);
    }
  });
</script>

<Container>
  <Card.Root>
    <Card.Header>
      <Card.Title>{insights.absScoreDiff}</Card.Title>
      <Card.Description>Card Description</Card.Description>
    </Card.Header>
    <Card.Content>
      <p>Card Content</p>
    </Card.Content>
    <Card.Footer>
      <p>Card Footer</p>
    </Card.Footer>
  </Card.Root>
</Container>
