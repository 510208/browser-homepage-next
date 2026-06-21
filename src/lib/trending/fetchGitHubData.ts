import { Octokit } from "octokit";

export async function fetchData() {
  const octokit = new Octokit();
  const response = await octokit.rest.users.getByUsername({
    username: "510208",
  });
  return response.data;
}