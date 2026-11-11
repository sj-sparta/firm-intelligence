"""Thin wrapper around the firm-intelligence-api HTTP endpoints. No Streamlit here."""

from typing import Iterator

import requests

DEFAULT_TIMEOUT = 30


class ApiError(Exception):
    """A request reached the API but it responded with a failure we don't special-case."""


class IndexNotBuiltError(ApiError):
    """The knowledge index hasn't been built yet (API returns 409 for this specific case)."""


class NotFoundError(ApiError):
    """The API returned 404 - e.g. no firm with that id."""


def _post(base_url: str, path: str, json: dict) -> requests.Response:
    try:
        return requests.post(f"{base_url}{path}", json=json, timeout=DEFAULT_TIMEOUT)
    except requests.exceptions.RequestException as e:
        raise ApiError(f"Could not reach the API at {base_url}: {e}") from e


def ask_agent(base_url: str, question: str) -> dict:
    """POST /agent/ask - the tool-use agent loop. Not guaranteed to exist server-side yet."""
    response = _post(base_url, "/agent/ask", {"question": question})
    if not response.ok:
        raise ApiError(f"Agent request failed ({response.status_code}): {response.text}")
    return response.json()


def search_knowledge(base_url: str, question: str, top_k: int) -> dict:
    """POST /knowledge/search - retrieval only, no generation."""
    response = _post(base_url, "/knowledge/search", {"question": question, "top_k": top_k})
    if response.status_code == 409:
        raise IndexNotBuiltError(response.json().get("detail", "Index is not built yet"))
    if not response.ok:
        raise ApiError(f"Search request failed ({response.status_code}): {response.text}")
    return response.json()


def stream_summary(base_url: str, firm_id: int) -> Iterator[str]:
    """GET /firms/{firm_id}/summary/stream - yields text chunks as they arrive."""
    try:
        response = requests.get(
            f"{base_url}/firms/{firm_id}/summary/stream",
            stream=True,
            timeout=DEFAULT_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        raise ApiError(f"Could not reach the API at {base_url}: {e}") from e

    if response.status_code == 404:
        raise NotFoundError(f"No firm with id {firm_id}")
    if not response.ok:
        raise ApiError(f"Summary request failed ({response.status_code}): {response.text}")

    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            yield chunk
