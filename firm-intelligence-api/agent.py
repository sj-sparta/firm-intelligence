"""The tool-use loop... nothing in here knows about FastAPI"""

import knowledge_store as knowledge
from llm import MODEL, client


# agent system prompt
AGENT_SYSTEM_PROMPT = (
    "You are legal market analyst with access to tools to a search tool over a firm "
    "intelligence knowledge base. Use the tool whenever a question needs "
    "information you don't already have - do not guess. Cite document ids in  "
    "your final answer. If the tool returns nothing relevant, say so honestly."
)


# search tool
SEARCH_TOOL = {
    "name": "search_knowledge_base",
    "description": (
        "Search the firm intelligence knowledge base for documents relevant "
        "to a question about firms, jurisdictions, compliance, or market commentary."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query"},
        },
        "required": ["query"],
    },
}


# the loop - one call, check, maybe repeat
MAX_ITERATIONS = 4


def ask_with_tools(question: str) -> dict:
    """Run the tool-use loop until the model answers, orrrr the limit is hit"""
    messages = [{"role": "user", "content": question}]
    total_input_tokens = 0
    total_output_tokens = 0
    tool_calls_made = 0

    # the loop
    for _ in range(MAX_ITERATIONS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=600,
            system=AGENT_SYSTEM_PROMPT,
            tools=[SEARCH_TOOL],
            messages=messages,
        )

        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens

    # checking whether the model is done
        if response.stop_reason != "tool_use":
            final_text = next((b.text for b in response.content if b.type == "text"), "")

            return {
                "answer": final_text,
                "completed": True,
                "tool_calls_made": tool_calls_made,
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "stop_reason": response.stop_reason,
            }

    # response content - when added to messages per round
        tool_blocks = [b for b in response.content if b.type == "tool_use"]
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for tool_block in tool_blocks:
            result_text, is_error = _execute_tool(tool_block.name, tool_block.input)
            if not is_error:
                tool_calls_made += 1

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_block.id,
                "content":result_text,
                "is_error": is_error
            })

        messages.append({"role": "user", "content": tool_results})

    # Loop exhausted MAX_ITERATIONS without the model finishing - return what we have instead of implicitly returning None
    return {
        "answer": "",
        "completed": False,
        "tool_calls_made": tool_calls_made,
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "stop_reason": "max_iterations",
    }



def _execute_tool(name: str, tool_input: dict) -> tuple[str, bool]:
    """Run the requested tool. Returns (result_text, is_error)"""

    # Guard 1 - we only have one real tool, checking it is equal to that
    if name != "search_knowledge_base":
        return f"Unknown tool: {name}", True

    # Guard 2 - even the right tool is useless without its one argument
    if "query" not in tool_input:
        return 'Error: missing required field "query"', True

    try:
        results = knowledge.search(tool_input["query"], top_k=3)
    except RuntimeError as e:
        return f"Error: {e}", True
    # same RuntimeError that knowledge.search has always raised
    # it gets caught here instead of letting it crash the whole agent loop

    if not results:
        return "No relevant documents found", False
    # A search that WORKED, but found nothing.... the is_error is False here
    # This is an honest empty result... nothing went wrong

    formatted = "\n\n".join(
        f"[{r['id']}] {r['title']} (score {r['score']:.2f})\n{r['text']}"
        for r in results
    )
    return formatted, False
    # The real success path - genuine results, formatted for the model to read