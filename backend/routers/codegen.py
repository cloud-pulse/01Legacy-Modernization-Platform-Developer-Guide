import os
from pathlib import Path

from fastapi import APIRouter


router = APIRouter()
BASE_OUTPUT = Path("output").resolve()


@router.post("/generate", summary="Generate target code for a session")
async def generate_target_code(session_id: str, target_lang: str = "java"):
    """
    Generate modern target code (Java or Python) for the given session.

    Demo implementation:
    - Writes a placeholder code file under output/sessions/{session_id}/code/{target_lang}/
    """
    session_dir = BASE_OUTPUT / "sessions" / session_id / "code" / target_lang
    os.makedirs(session_dir, exist_ok=True)

    sample_path = session_dir / ("SampleService.java" if target_lang == "java" else "sample_service.py")
    if target_lang == "java":
        sample_code = (
            "public class SampleService {\n"
            "    // TODO: generated code will go here\n"
            "}\n"
        )
    else:
        sample_code = (
            "def sample_service():\n"
            "    # TODO: generated code will go here\n"
            "    pass\n"
        )
    sample_path.write_text(sample_code)

    return {
        "session_id": session_id,
        "target_lang": target_lang,
        "status": "generated",
        "artifact_location": str(session_dir),
    }

