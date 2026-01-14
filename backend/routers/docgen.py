import json
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI


router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BASE_OUTPUT = Path("output").resolve()


@router.post("/generate", summary="Generate documentation for a session")
async def generate_documentation(session_id: str):
    """
    Generate system and module-level documentation for the given analysis session.

    Demo implementation:
    - Writes a placeholder JSON document under output/sessions/{session_id}/docs/summary.json
    """
    session_dir = BASE_OUTPUT / "sessions" / session_id / "docs"
    os.makedirs(session_dir, exist_ok=True)

    doc = {
        "session_id": session_id,
        "status": "generated",
        "summary": "High-level system overview and module documentation (placeholder).",
    }

    (session_dir / "summary.json").write_text(json.dumps(doc, indent=2))

    return doc


class LlmDocGenRequest(BaseModel):
    code: str
    language: str | None = None


@router.post(
    "/generate-llm",
    summary="Generate documentation for a small code snippet using an LLM",
    description=(
        "Concrete example of wiring this service to an LLM. "
        "Send a small legacy code snippet and get structured documentation back."
    ),
)
async def generate_documentation_with_llm(payload: LlmDocGenRequest):
    if client is None or os.getenv("OPENAI_API_KEY") is None:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured on the server.",
        )

    language = payload.language or "legacy code"
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that explains legacy enterprise code "
                        "so it can be reimplemented in modern Java/Python services. "
                        "Return a concise JSON document with: "
                        "purpose, inputs, outputs, main_steps, business_rules."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Language: {language}\n\n"
                        "Code:\n"
                        f"{payload.code}\n\n"
                        "Explain the code at a level that would let an engineer "
                        "rebuild it in a microservice, without repeating raw code."
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )
    except Exception as exc:  # pragma: no cover - demo integration
        raise HTTPException(
            status_code=500,
            detail=f"LLM call failed: {exc}",
        ) from exc

    content = completion.choices[0].message.content

    return {"raw_response": content}

