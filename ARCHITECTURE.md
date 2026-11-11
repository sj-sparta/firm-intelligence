# Firm Intelligence – Architecture

A prototype with three parts: a Streamlit UI, a FastAPI backend and an embedded Chroma vector database. Claude (LLM) and Voyage AI (embeddings) are external services.

## Component diagram

```mermaid
flowchart LR
    User([User / browser])

    subgraph UI["firm-intelligence-ui (Streamlit)"]
        APP["app.py<br/>tabs: Ask | Search | Summary"]
        CLIENT["api_client.py<br/>requests + ApiError types"]
        APP --> CLIENT
    end

    subgraph API["firm-intelligence-api (FastAPI, :8000)"]
        direction TB
        R_AGENT["routers/agent.py<br/>POST /agent/ask"]
        R_KNOW["routers/knowledge.py<br/>POST /knowledge/index | search | ask"]
        R_INS["routers/insights.py<br/>POST /firms/{id}/summary | analyse<br/>GET /firms/{id}/summary/stream | estimate"]
        R_CRUD["routers/firms.py, people.py<br/>CRUD, benchmarks"]

        AGENT["agent.py<br/>tool-use loop, max 4 iterations"]
        LLM["llm.py<br/>Claude client, 30s timeout, 3 retries"]
        KNOW["knowledge.py<br/>embed_texts (Voyage)"]
        STORE["knowledge_store.py<br/>Chroma wrapper"]
        DATA[("data.py / documents.py<br/>in-memory firms, people, 8 docs")]

        R_AGENT --> AGENT
        AGENT --> STORE
        R_KNOW --> STORE
        R_KNOW --> LLM
        R_INS --> LLM
        R_INS --> DATA
        R_CRUD --> DATA
        R_KNOW --> DATA
        STORE --> KNOW
    end

    subgraph VDB["Vector DB (embedded ChromaDB)"]
        CHROMA[("collection: firm_documents<br/>./chroma_store<br/>8 vectors, 512-d, cosine HNSW")]
    end

    subgraph EXT["External services"]
        ANTHROPIC["Anthropic API<br/>claude-haiku-4-5"]
        VOYAGE["Voyage AI<br/>voyage-3-lite"]
    end

    User --> APP
    CLIENT -- "HTTP / JSON, streaming text" --> R_AGENT
    CLIENT --> R_KNOW
    CLIENT --> R_INS

    STORE -- "add / query" --> CHROMA
    KNOW -- "embed" --> VOYAGE
    AGENT -- "messages + tools" --> ANTHROPIC
    LLM --> ANTHROPIC
```

Chroma runs inside the API process. There is no separate server, so uvicorn must be launched from `firm-intelligence-api/` for the relative `./chroma_store` path to resolve.

## Flows

### Ask (agent with tool use)

```mermaid
sequenceDiagram
    actor U as User
    participant UI as Streamlit
    participant API as FastAPI /agent/ask
    participant C as Claude
    participant V as Voyage
    participant DB as Chroma

    U->>UI: question
    UI->>API: POST /agent/ask
    loop up to 4 iterations
        API->>C: messages + search_knowledge_base tool
        C-->>API: tool_use(query)
        API->>V: embed query
        V-->>API: vector
        API->>DB: query top_k=3
        DB-->>API: docs + scores
        API->>C: tool_result
    end
    C-->>API: final answer
    API-->>UI: answer, completed, tool calls, tokens
    UI-->>U: success / warning box
```

### Search only

```mermaid
sequenceDiagram
    participant UI as Streamlit
    participant API as FastAPI /knowledge/search
    participant V as Voyage
    participant DB as Chroma

    UI->>API: POST {question, top_k}
    API->>V: embed query (input_type=query)
    V-->>API: vector
    API->>DB: collection.query
    DB-->>API: hits (score = 1 - distance)
    API-->>UI: results
```

### Streaming summary

```mermaid
sequenceDiagram
    participant UI as Streamlit
    participant API as FastAPI /firms/{id}/summary/stream
    participant C as Claude

    UI->>API: GET (stream=True)
    API->>API: get_firm_or_404
    API->>C: streaming request
    loop chunks
        C-->>API: text delta
        API-->>UI: text/plain chunk
    end
```

### Indexing (manual)

`POST /knowledge/index` reads `DOCUMENTS` from `documents.py`, embeds each one with Voyage (`input_type="document"`) and upserts it into Chroma by id. There is no chunking, so each document is one vector.

## Components

| Part | Tech | Location |
|---|---|---|
| UI | Streamlit, requests | `firm-intelligence-ui/` |
| API | FastAPI 0.115, uvicorn | `firm-intelligence-api/` |
| Vector DB | ChromaDB 1.5 (persistent, embedded) | `firm-intelligence-api/chroma_store/` |
| LLM | Anthropic, `claude-haiku-4-5-20251001` | needs `ANTHROPIC_API_KEY` |
| Embeddings | Voyage AI, `voyage-3-lite` | needs `VOYAGE_API_KEY` |

## Current status

- The end-to-end demo works on paper: all three UI features map to live endpoints, and Chroma holds 8 indexed documents. This was read from the code, not run.
- `ui-implementation-explainer.md` is stale. `/agent/ask` is now wired.
- The UI's "index not built" (409) path is probably dead, because the Chroma store returns an empty list instead of raising.
- `test_agent.py` is unfinished, and its fake tool-use block has trailing commas that stop it working.
- Missing: an API `requirements.txt`, `.env.example`, a real README, and Docker or CI.
- The UI does not use `/knowledge/ask`, `/analyse`, or the firms and people CRUD.
