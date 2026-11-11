import streamlit as st

import api_client as api

st.set_page_config(page_title="Firm Intelligence", layout="centered")

with st.sidebar:
    base_url = st.text_input("API base URL", value="http://127.0.0.1:8000")

st.title("Firm Intelligence")

ask_tab, search_tab, summary_tab = st.tabs(["Ask", "Search only", "Streaming summary"])

# ---------------------------------------------------------------------------
# Feature 1: Ask - question in, agent decides whether/how to search, answer out
# ---------------------------------------------------------------------------
with ask_tab:
    st.subheader("Ask the agent")
    question = st.text_input("Question", key="ask_question")

    if st.button("Ask", key="ask_button"):
        if not question.strip():
            st.warning("Type a question first.")
        else:
            try:
                with st.spinner("Thinking..."):
                    result = api.ask_agent(base_url, question)
            except api.ApiError as e:
                st.error(str(e))
            else:
                if result.get("completed"):
                    st.success(result.get("answer") or "(empty answer)")
                else:
                    st.warning(
                        "The agent hit its iteration limit before finishing. "
                        + (result.get("answer") or "No answer produced.")
                    )

                st.caption(
                    f"Tool calls: {result.get('tool_calls_made', '?')} | "
                    f"Input tokens: {result.get('input_tokens', '?')} | "
                    f"Output tokens: {result.get('output_tokens', '?')} | "
                    f"Stop reason: {result.get('stop_reason', '?')}"
                )

# ---------------------------------------------------------------------------
# Feature 2: Search only - retrieval, no generation
# ---------------------------------------------------------------------------
with search_tab:
    st.subheader("Search the knowledge base")
    search_query = st.text_input("Query", key="search_query")
    top_k = st.number_input("Top k", min_value=1, max_value=8, value=3, step=1)

    if st.button("Search", key="search_button"):
        if not search_query.strip():
            st.warning("Type a query first.")
        else:
            try:
                with st.spinner("Searching..."):
                    result = api.search_knowledge(base_url, search_query, int(top_k))
            except api.IndexNotBuiltError as e:
                st.warning(f"Index not built yet: {e}. Call POST /knowledge/index first.")
            except api.ApiError as e:
                st.error(f"Search failed: {e}")
            else:
                results = result.get("results", [])
                if not results:
                    st.info("No results returned.")
                for hit in results:
                    st.markdown(f"**{hit['title']}** (score {hit['score']:.3f})")
                    st.caption(f"id: {hit['id']}")
                    st.write(hit["text"])
                    st.divider()

# ---------------------------------------------------------------------------
# Feature 3: Streaming summary - text arrives incrementally
# ---------------------------------------------------------------------------
with summary_tab:
    st.subheader("Streaming firm summary")
    firm_id = st.number_input("Firm id", min_value=1, value=1, step=1)

    if st.button("Get summary", key="summary_button"):
        placeholder = st.empty()
        try:
            text = ""
            for chunk in api.stream_summary(base_url, int(firm_id)):
                text += chunk
                placeholder.markdown(text)
            if not text:
                placeholder.info("No summary text was returned.")
        except api.NotFoundError as e:
            st.error(str(e))
        except api.ApiError as e:
            st.error(f"Summary failed: {e}")
