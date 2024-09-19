import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, url }) => {
  const username = url.searchParams.get("username") || "";
  const manga = !!url.searchParams.get("manga");

  const response = await fetch(
    `http://localhost:8000/api/home/?username=${username}&manga=${manga}`,
  ).then((insights) => insights.json());

  return response;
};
