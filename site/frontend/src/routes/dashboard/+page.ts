import type { PageLoad } from "./$types";
import { error } from "@sveltejs/kit";

const API_URL = import.meta.env.DEV ? "http://localhost:8000" : "/api";

export const load: PageLoad = async ({ fetch, url }) => {
  const username = url.searchParams.get("username") || "";
  const manga = url.searchParams.get("manga");

  const response = await fetch(
    `${API_URL}/home/?username=${username}&manga=${manga}`,
  );

  if (!response.ok) {
    const errorData = await response.json();
    throw error(response.status, errorData.detail || "An error occurred.");
  }

  return await response.json();
};
