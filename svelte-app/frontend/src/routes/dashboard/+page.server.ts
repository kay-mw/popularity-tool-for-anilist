import type { Actions } from "./$types";

export const actions = {
  default: async ({ request }) => {
    try {
      const formData = await request.formData();
      const username = formData.get("username");
      const isChecked = !!formData.get("manga")
      const response = await fetch("http://localhost:8000/api/home", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ manga_checked: isChecked, username: username }),
      });

      if (!response.ok) {
        //throw new Error("Network response was not ok");

      }

      const data = await response.json() 
      console.log(data)
      return { data }


    } catch (error) {
      //console.error("Error:", error);
    }
  }
} satisfies Actions
