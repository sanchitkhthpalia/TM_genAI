# AI Ops Assistant

A local, runnable AI Ops Assistant that accepts natural language tasks, plans execution steps, calls real third-party APIs (GitHub, OpenWeather, NewsAPI), and verifies the results.

## 🧠 Architecture

The system uses a **Multi-Agent Architecture**:

1.  **Planner Agent**: Breakdowns the user's request into a sequence of tool calls. It understands the capabilities of available tools and provides a JSON plan.
2.  **Executor Agent**: Iterates through the plan, executing each tool call strictly. It handles real API interactions and captures raw outputs.
3.  **Verifier Agent**: Analyzes the execution results against the original user query. It synthesizes a final natural language response and flags any missing or incomplete data.

## 🔌 Integrated APIs

-   **GitHub API**: Search and retrieve repository details.
-   **OpenWeather API**: Get current weather data for any city.
-   **NewsAPI**: Retrieve top headlines (Technology, etc.).

## 🚀 Setup Instructions

1.  **Clone/Open the Repository**
2.  **Create Virtual Environment (Optional but recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables**
    Copy `.env.example` to `.env` and fill in your keys:
    ```bash
    cp .env.example .env
    ```
    - `OPENAI_API_KEY`: Required for Agents.
    - `OPENWEATHER_API_KEY`: Required for Weather tasks.
    - `NEWS_API_KEY`: Required for News tasks (optional, free tier available).
    - `GITHUB_TOKEN`: Optional, but recommended to avoid rate limits.

5.  **Run the Application**
    ```bash
    streamlit run ai_ops_assistant/main.py
    ```

## 🧪 Example Prompts

1.  **GitHub Research**
    > "Find the top 3 Python GitHub repos created this year and show their star counts."
    
2.  **Multi-Tool Information**
    > "What’s the current weather in Delhi and today’s top tech headline?"
    
3.  **Comparison & Trending**
    > "Compare weather in Mumbai and Bangalore and list trending GitHub repos."

## ⚠️ Limitations & Tradeoffs

-   **Sequential Execution**: The Executor runs steps one by one. Parallel execution could improve performance for independent tasks.
-   **Error Handling**: Basic retry logic is implemented via the Verifier's ability to report issues, but complex auto-recovery loops are simplified for this scope.
-   **Context Window**: Extremely large API responses (e.g., massive GitHub searches) might be truncated to fit the LLM context window during verification.
