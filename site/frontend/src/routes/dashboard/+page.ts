import type { PageLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageLoad = async ({ fetch, url }) => {
  const username = url.searchParams.get("username") || "";
  const manga = url.searchParams.get("manga");

  // Prod
  const response = await fetch(
    `/api/home/?username=${username}&manga=${manga}`,
  );

  // Dev
  //const response = await fetch(
  //  `http://localhost:8000/home/?username=${username}&manga=${manga}`,
  //);

  if (!response.ok) {
    const errorData = await response.json();
    throw error(response.status, errorData.detail || "An error occurred.");
  }

  return await response.json();
};
