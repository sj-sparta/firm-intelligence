from anthropic import APIStatusError, APITimeoutError, RateLimitError
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import agent

router = APIRouter(prefix="/agent", tags=["agent"])


class AgentQuestion(BaseModel):
    question: str = Field(min_length=3)


@router.post("/ask")
def ask(q: AgentQuestion):
    """The model decides for itself whether it needs to search."""
    try:
        return agent.ask_with_tools(q.question)
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="Agent provider timed out")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Agent provider rate limited")
    except APIStatusError:
        raise HTTPException(status_code=502, detail="Agent provider unavailable")
