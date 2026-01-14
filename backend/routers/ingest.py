import os
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File


router = APIRouter()

BASE_OUTPUT = Path("output").resolve()


@router.post("/legacy-code", summary="Ingest legacy codebase")
async def ingest_legacy_code(files: List[UploadFile] = File(...)):
    """
    Ingest a set of legacy code files (VB, COBOL, Java, etc.) and return
    an identifier for the analysis session.

    This demo implementation:
    - Stores uploaded files under output/sessions/{session_id}/input/
    - Returns the session id and saved paths
    """
    session_id = str(uuid.uuid4())
    session_dir = BASE_OUTPUT / "sessions" / session_id / "input"
    os.makedirs(session_dir, exist_ok=True)

    saved_files: list[str] = []
    for f in files:
        target_path = session_dir / (f.filename or "uploaded-file")
        content = await f.read()
        target_path.write_bytes(content)
        saved_files.append(str(target_path))

    return {"session_id": session_id, "files": saved_files}

