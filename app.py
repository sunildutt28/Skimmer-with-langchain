"""
NewsLens — Streamlit UI
────────────────────────
Run with:
    streamlit run app.py

Make sure news_agent.py is in the same folder.
Set env vars before running:
    set GROQ_API_KEY=your_key
    set GNEWS_API_KEY=your_key
"""

import streamlit as st
from news_agent import run

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NewsLens",
    page_icon="🗞️",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; max-width: 780px; }

        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.1;
        }
        .hero-sub {
            color: #888;
            font-size: 1rem;
            margin-top: 0.4rem;
            margin-bottom: 1.5rem;
        }
        .chip {
            display: inline-block;
            background: #f0f2f6;
            border-radius: 99px;
            padding: 3px 12px;
            font-size: 0.75rem;
            color: #555;
            margin-right: 6px;
            margin-bottom: 16px;
        }
        .result-box {
            background: #f8f9fb;
            border-left: 4px solid #ff4b4b;
            border-radius: 8px;
            padding: 1.2rem 1.5rem;
            font-size: 0.95rem;
            line-height: 1.8;
            margin-top: 1rem;
        }
        .footer {
            text-align: center;
            color: #bbb;
            font-size: 0.75rem;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🗞️ NewsLens</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">AI-powered news digest — fetch, summarize, and understand any topic instantly.</div>', unsafe_allow_html=True)

st.markdown("""
    <span class="chip">⚡ Groq LLaMA 3.1</span>
    <span class="chip">📰 GNews API</span>
    <span class="chip">🤖 distilgpt2</span>
    <span class="chip">🔗 LangGraph</span>
""", unsafe_allow_html=True)

st.divider()

# ── Suggested topics ───────────────────────────────────────────────────────
st.markdown("**💡 Try a topic:**")
suggested = ["Artificial Intelligence", "Climate Change", "Space Exploration", "Cybersecurity", "Stock Market"]

cols = st.columns(len(suggested))
selected_suggestion = None
for i, topic in enumerate(suggested):
    if cols[i].button(topic, use_container_width=True):
        selected_suggestion = topic

# ── Input ──────────────────────────────────────────────────────────────────
st.markdown("**Or type your own:**")
query = st.text_input(
    label="topic",
    placeholder="e.g. electric vehicles, quantum computing, Olympics...",
    label_visibility="collapsed",
    value=selected_suggestion or "",
)

search_clicked = st.button("🔍 Get Digest", type="primary", use_container_width=True)

# ── Run agent ──────────────────────────────────────────────────────────────
if search_clicked and query.strip():
    with st.spinner("📡 Fetching headlines and generating digest..."):
        try:
            result = run(query.strip())

            st.success("✅ Digest ready!")
            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

            # Save to history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.insert(0, {"topic": query.strip(), "result": result})

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

elif search_clicked and not query.strip():
    st.warning("Please enter a topic first.")

# ── History ────────────────────────────────────────────────────────────────
if "history" in st.session_state and st.session_state.history:
    st.divider()
    st.markdown("**🕘 Previous searches:**")
    for i, item in enumerate(st.session_state.history[1:4]):   # show last 3
        with st.expander(f"📌 {item['topic']}"):
            st.markdown(f'<div class="result-box">{item["result"]}</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">NewsLens · Built with LangChain, LangGraph, Groq & Streamlit</div>',
    unsafe_allow_html=True
)