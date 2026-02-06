import json
from ai_ops_assistant.llm.client import LLMClient

class VerifierAgent:
    def __init__(self):
        self.llm = LLMClient()

    def verify_and_synthesize(self, user_request: str, execution_results: dict):
        system_prompt = """
        You are the Verifier Agent for an AI Ops Assistant.
        Your goal is to validate the execution results against the original user request and produce a final answer.
        
        Input:
        - User Request
        - Execution Results (JSON)
        
        Responsibilities:
        1. Check if the execution results contain the necessary information to answer the request.
        2. If data is missing or errors occurred, note this.
        3. Synthesize the raw data into a clean, human-readable response.
        4. Return a structured JSON response.
        
        Output Format (JSON):
        {
            "status": "success" | "incomplete" | "failure",
            "final_response": "The natural language answer to the user...",
            "verification_notes": "Any notes on data quality or missing info"
        }
        """
        
        context = f"User Request: {user_request}\nExecution Results: {json.dumps(execution_results, indent=2)}"
        
        response = self.llm.generate_response(system_prompt, context, json_mode=True)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
             return {
                 "status": "failure",
                 "final_response": "Failed to generate verification report.",
                 "verification_notes": "JSON parsing error on LLM response."
             }
