<script lang="ts">
  import { goto } from "$app/navigation";
  import { Button } from "$lib/components/ui/button";
  import { toggleMode } from "mode-watcher";

  let isChecked = false;
  let username = "";
  let isLoading = false;

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    isLoading = true;

    try {
      const response = await fetch("http://localhost:8000/api/home", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ manga_checked: isChecked, username: username }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      sessionStorage.setItem("insights", JSON.stringify(data.insights));

      goto("/dashboard");
    } catch (error) {
      console.error("Error:", error);
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="flex items-start justify-end p-1">
  <Button on:click={toggleMode} variant="outline" size="sm">
    <span class="hidden dark:block">Dark</span>
    <span class="dark:hidden">Light</span>
  </Button>
</div>
<div class="container">
  <h1 class="scroll-m-20 font-extrabold tracking-tight text-4xl lg:text-5xl">
    Have you ever wondered how controversial your anime taste is?
  </h1>
</div>
