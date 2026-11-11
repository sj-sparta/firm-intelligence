"""
The LangChain chat model.... we will build it with the same limits as llm.py's native client.
Our decisions in llm.py
- sets a 30 second timeout
- 3 retries
"""

from functools import lru_cache

from langchain_anthropic import ChatAnthropic

import llm

@lru_cache
def chat_model(max_tokens: int = 500) -> ChatAnthropic:
    return ChatAnthropic(llm.MODEL, max_tokens=max_tokens, timeout=30.0, max_retries=3)

