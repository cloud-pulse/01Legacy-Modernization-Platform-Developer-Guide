from typing import List

from fastapi import APIRouter, UploadFile, File


router = APIRouter()


@router.post("/legacy-code", summary="Ingest legacy codebase")
async def ingest_legacy_code(files: List[UploadFile] = File(...)):
    """
    Ingest a set of legacy code files (VB, COBOL, Java, etc.) and return
    a synthetic identifier for the analysis session.

    In a real implementation this would:
    - Store files in object storage
    - Parse them into an intermediate representation (IR)
    - Index them for later retrieval and analysis
    """
    # Placeholder: just return names and a fake session id
    session_id = "session-placeholder"
    filenames = [f.filename for f in files]
    return {"session_id": session_id, "files": filenames}

