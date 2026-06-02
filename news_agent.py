"""
LangChain / LangGraph Agentic AI Demo — NewsDigestBot
──────────────────────────────────────────────────────
Agent: NewsDigestBot (LangChain 1.x / LangGraph)
- Tool 1: fetch_headlines  → GNews public API (free, no credit card)
- Tool 2: summarize_text   → distilgpt2 via text-generation pipeline
                             (Transformers 5.x compatible, ~350 MB)
- LLM backbone: GPT-3.5-turbo via langchain-openai
- Agent loop: LangGraph create_react_agent

Setup:
    pip install langchain langchain-openai langgraph transformers torch requests
    set OPENAI_API_KEY=sk-...
    set GNEWS_API_KEY=your_key_from_gnews.io
    python news_agent.py
"""

import os

try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
    GNEWS_API_KEY = st.secrets.get("GNEWS_API_KEY", os.environ.get("GNEWS_API_KEY", ""))
except Exception:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    GNEWS_API_KEY = os.environ.get("GNEWS_API_KEY", "")

import requests
from transformers import pipeline

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ---------------------------------------------------------------------------
# 1.  ML Model — distilgpt2 text-generation (Transformers 5.x compatible)
# ---------------------------------------------------------------------------
print("⏳  Loading distilgpt2 model (first run downloads ~350 MB)…")
_generator = pipeline(
    "text-generation",
    model="distilgpt2",
    truncation=True,
)
print("✅  distilgpt2 ready.\n")

GNEWS_KEY = GNEWS_API_KEY

# ---------------------------------------------------------------------------
# 2.  Tool definitions
# ---------------------------------------------------------------------------

@tool
def fetch_headlines(topic: str, max_articles: int = 5) -> str:
    """
    Fetch the latest news headlines for a given topic using the GNews API.
    Returns up to max_articles headlines with title, source, and description.
    Requires GNEWS_API_KEY environment variable (free at https://gnews.io).
    """
    if not GNEWS_KEY:
        return "Error: GNEWS_API_KEY environment variable not set."

    url = "https://gnews.io/api/v4/search"
    params = {
        "q":      topic,
        "lang":   "en",
        "max":    max_articles,
        "apikey": GNEWS_KEY,
        "sortby": "publishedAt",
    }

    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    articles = data.get("articles", [])
    if not articles:
        return f"No articles found for topic: '{topic}'."

    lines = [f"Top {len(articles)} headlines for '{topic}':\n"]
    for i, a in enumerate(articles, 1):
        lines.append(
            f"{i}. [{a['source']['name']}] {a['title']}\n"
            f"   {a.get('description', 'No description available.')}"
        )
    return "\n".join(lines)


@tool
def summarize_text(text: str) -> str:
    """
    Generate a short continuation/summary of the provided news headlines
    using distilgpt2 running locally via HuggingFace Transformers.
    Works with Transformers 5.x text-generation pipeline.
    """
    # Build a prompt that steers GPT-2 toward summarization behaviour
    prompt = (
        "The following are today's top news headlines:\n\n"
        + " ".join(text.split()[:200])   # stay within GPT-2's 1024 token limit
        + "\n\nIn summary:"
    )

    from transformers import GenerationConfig
    gen_config = GenerationConfig(max_new_tokens=80, do_sample=False, pad_token_id=50256)
    result = _generator(prompt, generation_config=gen_config)

    # Strip the prompt from the output, return only the generated part
    generated = result[0]["generated_text"]
    summary = generated[len(prompt):].strip()
    return summary if summary else generated.strip()


# ---------------------------------------------------------------------------
# 3.  LLM + LangGraph agent
# ---------------------------------------------------------------------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    groq_api_key=GROQ_API_KEY,
)

tools = [fetch_headlines, summarize_text]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=(
        "You are NewsDigestBot, a sharp news assistant. "
        "When asked about a topic: FIRST call fetch_headlines to get live articles, "
        "THEN call summarize_text on the combined headlines and descriptions, "
        "THEN present a clean digest with a one-line takeaway at the end."
    ),
)

# ---------------------------------------------------------------------------
# 4.  Run
# ---------------------------------------------------------------------------

def run(query: str) -> str:
    print(f"\n{'─'*60}")
    print(f"USER: {query}")
    print("─"*60)

    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    answer = result["messages"][-1].content
    print(f"\nAGENT:\n{answer}\n")
    return answer


if __name__ == "__main__":
    queries = [
        "What's happening with artificial intelligence today?",
        "Give me a digest on the latest climate news.",
    ]
    for q in queries:
        run(q)