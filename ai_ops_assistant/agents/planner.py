import json
from ai_ops_assistant.llm.client import LLMClient

class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def create_plan(self, user_request: str):
        system_prompt = """
        You are the Planner Agent for an AI Ops Assistant.
        Your goal is to break down a user request into a sequence of execution steps.
        
        Available Tools:
        1. github_search_repositories(query: str, sort: str = 'stars', order: str = 'desc') - Search GitHub repos.
        2. github_get_repository(owner: str, repo: str) - Get details for a specific repo.
        3. get_current_weather(city: str) - Get current weather for a city.
        4. get_top_headlines(country: str, category: str) - Get top news headlines.
        
        Output Format (JSON):
        {
            "steps": [
                {
                    "step_id": 1,
                    "description": "Search for Python repos",
                    "tool": "github_search_repositories",
                    "parameters": {
                        "query": "language:python",
                        "sort": "stars"
                    }
                }
            ]
        }
        
        Rules:
        - Only use the provided tools.
        - If the request requires multiple steps, list them in order.
        - If no tool matches, return an empty steps list or best effort.
        - Your output MUST be valid JSON.
        """
        
        response = self.llm.generate_response(system_prompt, user_request, json_mode=True)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse Planner plan", "raw": response}
