import streamlit as st
import json
import os
import sys
from dotenv import load_dotenv

# Add the project root to sys.path to allow imports from ai_ops_assistant
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_ops_assistant.agents.planner import PlannerAgent
from ai_ops_assistant.agents.executor import ExecutorAgent
from ai_ops_assistant.agents.verifier import VerifierAgent

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Ops Assistant", page_icon="🤖")

st.title("🤖 AI Ops Assistant")
st.markdown("### Your Agentic AI operations partner")

# Sidebar for configuration or info
with st.sidebar:
    st.header("About")
    st.info("This assistant uses a multi-agent architecture (Planner -> Executor -> Verifier) to solve tasks using real APIs.")
    st.markdown("---")
    st.markdown("**Core Agents:**")
    st.markdown("1. **Planner**: Breaks down requests.")
    st.markdown("2. **Executor**: Calls tools (GitHub, Weather, News).")
    st.markdown("3. **Verifier**: Validates and synthesizes answers.")

# Check for API Keys
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY is missing in .env file.")
    st.stop()

# User Input
user_query = st.text_area("Enter your request:", placeholder="e.g., Find the top 3 Python GitHub repos created this year and show their star counts.", height=100)

if st.button("Execute Task"):
    if not user_query:
        st.warning("Please enter a request.")
    else:
        st.markdown("---")
        
        # 1. Planning Phase
        st.subheader("1️⃣ Planning")
        with st.status("Generating Plan...", expanded=True) as status:
            planner = PlannerAgent()
            plan = planner.create_plan(user_query)
            
            if "error" in plan:
                status.update(label="Planning Failed", state="error")
                st.error(f"Error: {plan['error']}")
                st.stop()
            
            st.json(plan)
            status.update(label="Plan Created", state="complete")

        # 2. Execution Phase
        st.subheader("2️⃣ Execution")
        with st.status("Executing Tools...", expanded=True) as status:
            executor = ExecutorAgent()
            execution_results = executor.execute_plan(plan)
            
            # Check for execution errors
            has_errors = any(res.get("status") == "error" for res in execution_results.values())
            
            for step_id, result in execution_results.items():
                if result.get("status") == "error":
                    st.error(f"Step {step_id} Failed: {result.get('error')}")
                else:
                    st.success(f"Step {step_id} ({result.get('description')}): Success")
                    with st.expander(f"Step {step_id} Output"):
                        st.json(result.get("output"))
            
            if has_errors:
                status.update(label="Execution Completed with Errors", state="warning")
            else:
                status.update(label="Execution Completed", state="complete")

        # 3. Verification Phase
        st.subheader("3️⃣ Verification & Final Output")
        with st.status("Verifying Results...", expanded=True) as status:
            verifier = VerifierAgent()
            final_output = verifier.verify_and_synthesize(user_query, execution_results)
            
            if final_output.get("status") == "failure":
                 status.update(label="Verification Failed", state="error")
                 st.error(final_output.get("final_response"))
            else:
                status.update(label="Verification Complete", state="complete")
                st.markdown("### Answer")
                st.write(final_output.get("final_response"))
                
                if final_output.get("verification_notes"):
                    st.info(f"Notes: {final_output.get('verification_notes')}")
