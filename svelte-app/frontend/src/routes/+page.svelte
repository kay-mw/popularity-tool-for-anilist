<script lang="ts">
  import { goto } from "$app/navigation";

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

<div
  class="bg-base-100 flex items-center justify-center h-screen font-dm-sans font-medium"
>
  {#if isLoading}
    <div class="loading loading-infinity loading-lg"></div>
  {:else}
    <div class="text-center w-full max-w-xl fade-in content">
      <h1 class="text-primary text-2xl sm:text-3xl md:text-4xl font-bold mb-6">
        Have you ever wondered how controversial your anime taste is?
      </h1>
      <div class="divider divider-primary mb-6"></div>
      <h3 class="text-white text-lg sm:text-xl md:text-2xl mb-6">
        Find out by entering your AniList username below...
      </h3>
      <div class="mb-1 text-secondary text-left text-sm">
        Hint: If you don't have an AniList profile, just type in "bob" instead!
      </div>
      <form
        class="flex flex-col justify-center items-center space-y-4"
        on:submit={handleSubmit}
      >
        <input
          class="input input-secondary input-bordered w-full text-white text-lg"
          type="text"
          bind:value={username}
          placeholder="Your AniList username"
          required
        />
        <button
          class="w-full btn btn-outline btn-secondary text-lg"
          type="submit">Submit</button
        >
        <div class="flex items-end w-full form-control">
          <label class="label cursor-pointer">
            <input
              class="checkbox checkbox-info checked:checkbox-secondary peer"
              type="checkbox"
              bind:checked={isChecked}
            />
            <span class="px-2 transition peer-checked:text-secondary"
              >I want manga insights instead.</span
            >
          </label>
        </div>
      </form>
    </div>
  {/if}
</div>
