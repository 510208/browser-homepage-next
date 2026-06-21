import { Octokit } from "octokit";

type GitHubData = {
  name: string;
  followers: number;
  public_repos: number;
  avatar_url: string;
  html_url: string;
  bio: string;
};

async function fetchData() {
  const octokit = new Octokit();
  const response = await octokit.rest.users.getByUsername({
    username: "510208",
  });

  console.log("GitHub API response:", response);
  return response.data;
}

async function parseResponse(): Promise<GitHubData> {
  const data = await fetchData();
  if (!data) {
    throw new Error("Failed to fetch GitHub data");
  }

  return {
    name: data.name || data.login,
    bio: data.bio || "",
    avatar_url: data.avatar_url,
    html_url: data.html_url,
    followers: data.followers,
    public_repos: data.public_repos,
  } as GitHubData;
}

export { type GitHubData, fetchData, parseResponse };