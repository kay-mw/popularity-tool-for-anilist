<script>
  import "../app.css";
</script>

<svelte:head>
  <link
    href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap"
    rel="stylesheet"
  />
  <title>How Popular is Your Anime Taste?</title>
</svelte:head>

<slot />

<style>
  :global(body) {
    font-family: "DM Sans", sans-serif;
  }
</style>
