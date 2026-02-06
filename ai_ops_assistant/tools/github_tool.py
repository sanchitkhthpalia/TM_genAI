import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GitHubTool:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def search_repositories(self, query: str, sort: str = "stars", order: str = "desc", per_page: int = 5):
        """
        Searches for repositories on GitHub.
        """
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except requests.exceptions.RequestException as e:
            return {"error": f"GitHub API Error: {str(e)}"}

    def get_repository(self, owner: str, repo: str):
        """
        Gets details of a specific repository.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"GitHub API Error: {str(e)}"}
