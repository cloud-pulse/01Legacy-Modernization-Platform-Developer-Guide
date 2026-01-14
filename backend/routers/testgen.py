import os
from pathlib import Path

from fastapi import APIRouter


router = APIRouter()
BASE_OUTPUT = Path("output").resolve()


@router.post("/generate", summary="Generate unit tests for target code")
async def generate_unit_tests(session_id: str, target_lang: str = "java"):
    """
    Generate unit test suites corresponding to the generated target code.

    Demo implementation:
    - Writes a placeholder test file under output/sessions/{session_id}/tests/{target_lang}/
    """
    session_dir = BASE_OUTPUT / "sessions" / session_id / "tests" / target_lang
    os.makedirs(session_dir, exist_ok=True)

    test_path = session_dir / ("SampleServiceTest.java" if target_lang == "java" else "test_sample_service.py")
    if target_lang == "java":
        test_code = (
            "public class SampleServiceTest {\n"
            "    // TODO: generated unit tests will go here\n"
            "}\n"
        )
    else:
        test_code = (
            "def test_sample_service():\n"
            "    # TODO: generated unit tests will go here\n"
            "    assert True\n"
        )
    test_path.write_text(test_code)

    return {
        "session_id": session_id,
        "target_lang": target_lang,
        "status": "generated",
        "test_suite_location": str(session_dir),
    }

