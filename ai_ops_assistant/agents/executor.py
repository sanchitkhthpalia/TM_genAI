from ai_ops_assistant.tools.github_tool import GitHubTool
from ai_ops_assistant.tools.weather_tool import WeatherTool
from ai_ops_assistant.tools.news_tool import NewsTool

class ExecutorAgent:
    def __init__(self):
        self.github_tool = GitHubTool()
        self.weather_tool = WeatherTool()
        self.news_tool = NewsTool()
        
        self.tool_map = {
            "github_search_repositories": self.github_tool.search_repositories,
            "github_get_repository": self.github_tool.get_repository,
            "get_current_weather": self.weather_tool.get_current_weather,
            "get_top_headlines": self.news_tool.get_top_headlines
        }

    def execute_plan(self, plan: dict):
        results = {}
        steps = plan.get("steps", [])
        
        for step in steps:
            step_id = step.get("step_id")
            tool_name = step.get("tool")
            params = step.get("parameters", {})
            
            if tool_name in self.tool_map:
                try:
                    print(f"Executing step {step_id}: {tool_name} with {params}")
                    result = self.tool_map[tool_name](**params)
                    results[step_id] = {
                        "description": step.get("description"),
                        "status": "success",
                        "output": result
                    }
                except Exception as e:
                    results[step_id] = {
                        "description": step.get("description"),
                        "status": "error",
                        "error": str(e)
                    }
            else:
                 results[step_id] = {
                        "description": step.get("description"),
                        "status": "error",
                        "error": f"Tool {tool_name} not found"
                    }
        
        return results
