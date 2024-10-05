import type { PageLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageLoad = async ({ fetch, url }) => {
  const username = url.searchParams.get("username") || "";
  const manga = url.searchParams.get("manga");

  const response = await fetch(
    `http://backend:8000/api/home/?username=${username}&manga=${manga}`,
  );

  if (!response.ok) {
    const errorData = await response.json();
    console.log(errorData);
    throw error(response.status, errorData.detail || "An error occurred.");
  }

  return await response.json();
};
