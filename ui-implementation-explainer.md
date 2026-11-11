# UI implementation explainer

Companion to `challenge-build-the-ui.md`. Walks through what each button in
`firm-intelligence-ui/app.py` actually does, end to end, against the real API. Code lives in
two files: `app.py` (Streamlit widgets and rendering) and `api_client.py` (the only place that
talks HTTP, via `requests`).

All three features read `base_url` from the sidebar text input (default
`http://127.0.0.1:8000`) and build the request against that.

---

## Feature 1: Ask

**Widgets:** a text input (`ask_question`) and an "Ask" button.

**On click:**
1. `app.py` guards against an empty question, then calls `api.ask_agent(base_url, question)`.
2. `ask_agent` (`api_client.py`) does `requests.post(f"{base_url}/agent/ask", json={"question": question})`.
3. If the request never reaches the server (connection refused, DNS failure, timeout), `_post`
   catches `requests.exceptions.RequestException` and re-raises it as `ApiError` with a message
   naming the base URL — this is the "request fails, don't crash silently" path.
4. If the server responds but not with a 2xx, `ask_agent` raises `ApiError` with the status code
   and body.
5. On success, the JSON body is expected to have the same shape as `agent.py`'s
   `ask_with_tools()` return value: `answer`, `completed`, `tool_calls_made`, `input_tokens`,
   `output_tokens`, `stop_reason`.
6. Back in `app.py`: if `completed` is `True`, the answer renders as a success box. If `completed`
   is `False` (the agent hit `MAX_ITERATIONS` without finishing), it renders as a warning instead,
   prefixed with an explicit "hit its iteration limit" message — a different visual state, not the
   same green box with different words.
7. Tool call count and both token counts are always shown in a caption underneath, regardless of
   which branch above fired.

**Known gap:** `POST /agent/ask` is not currently wired up in the API (`agent.py` has the loop
logic but no router exposes it) — by design, per an earlier decision not to touch the API. Until
that endpoint exists, step 4 above is the one that fires: a 404 rendered as a clear `st.error`,
not a crash.

## Feature 2: Search only

**Widgets:** a text input (`search_query`), a number input for `top_k` (1-8, default 3), and a
"Search" button.

**On click:**
1. `app.py` guards against an empty query, then calls
   `api.search_knowledge(base_url, search_query, top_k)`.
2. `search_knowledge` does `requests.post(f"{base_url}/knowledge/search", json={"question": ..., "top_k": ...})`,
   matching the `Question` model in `routers/knowledge.py`.
3. Three distinct outcomes are handled differently, matching the brief's requirement to not
   collapse "index not built" into a generic failure:
   - **HTTP 409** → the API's specific signal that `knowledge_store.search` raised `RuntimeError`
     because `build_index()` hasn't run yet. `search_knowledge` raises `IndexNotBuiltError`, and
     `app.py` renders this as a `st.warning` telling the user to call `POST /knowledge/index`
     first.
   - **Any other non-2xx** (5xx, malformed request, etc.) → `search_knowledge` raises the plain
     `ApiError`, rendered as `st.error` with a generic "search failed" message.
   - **Success** → the JSON's `results` list is rendered one entry per hit: title (bold) with its
     score to 3 decimal places, the document id as a caption, and the retrieved text body, with a
     divider between hits. If `results` is empty, an info box says so explicitly rather than
     rendering nothing.

No generation happens here — this only exercises retrieval, so nothing is sent to the LLM and no
`answer` field exists in the response.

## Feature 3: Streaming summary

**Widgets:** a number input for `firm_id` (default 1) and a "Get summary" button.

**On click:**
1. `app.py` creates an empty placeholder (`st.empty()`) and calls
   `api.stream_summary(base_url, firm_id)`, which is a generator, not a one-shot call.
2. `stream_summary` opens `requests.get(f"{base_url}/firms/{firm_id}/summary/stream", stream=True)`
   — `stream=True` is what stops `requests` from buffering the whole response before returning,
   which is what makes incremental rendering possible.
3. Before yielding anything, it checks the status: a **404** (no firm with that id, raised by
   `get_firm_or_404` in the API) becomes `NotFoundError`, rendered by `app.py` as `st.error`. Any
   other non-2xx becomes the generic `ApiError`.
4. On success, it iterates `response.iter_content(chunk_size=None, decode_unicode=True)`, yielding
   each chunk of text as it arrives from the server (the API side is itself streaming from
   `llm.stream_firm_summary`, which yields chunks from the Anthropic streaming call).
5. `app.py`'s loop appends each chunk to a running `text` string and calls
   `placeholder.markdown(text)` on every iteration — so the same on-screen element is rewritten
   with progressively more text, rather than the page waiting for the full summary before showing
   anything.
6. If the stream completes with no text at all, the placeholder shows an info message instead of
   staying blank.

Because `firm_id` is a free-entry number input (not a hardcoded dropdown of the five seed firms),
this works for any firm id that exists in `data.py` at the time of the call, including ones added
later via `POST /firms`.

---

## What's deliberately out of scope

- The API itself was not modified for this challenge (aside from an earlier, separate fix to a
  missing `return` in `agent.py`'s iteration-limit path). `POST /agent/ask` is not implemented
  server-side; the UI is built to call it correctly and fail cleanly, not to fake its response.
- No caching, retries, or session state beyond what Streamlit gives you for free — each button
  press is a fresh request.
</content>
