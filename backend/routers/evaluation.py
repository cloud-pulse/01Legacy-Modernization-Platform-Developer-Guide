import json
import os
from pathlib import Path

from fastapi import APIRouter


router = APIRouter()
BASE_OUTPUT = Path("output").resolve()


@router.get("/metrics", summary="Get documentation quality metrics")
async def get_documentation_metrics(session_id: str):
    """
    Return coverage and confidence metrics for the generated documentation,
    suitable for powering a dashboard.

    Demo implementation:
    - Returns static metrics
    - Writes them under output/sessions/{session_id}/docs/metrics.json
    """
    metrics = {
        "session_id": session_id,
        "coverage": {
            "modules": 0.75,
            "data_elements": 0.6,
            "interfaces": 0.5,
        },
        "confidence": {
            "overall": 0.7,
            "by_module": [],
        },
        "hotspots": [],
    }

    session_dir = BASE_OUTPUT / "sessions" / session_id / "docs"
    os.makedirs(session_dir, exist_ok=True)
    (session_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))

    return metrics
