from fastapi import FastAPI
from routers import ingest, docgen, evaluation, codegen, testgen


def create_app() -> FastAPI:
    app = FastAPI(
        title="Legacy Modernization Platform",
        description="Ingest legacy code (VB, COBOL, Java), generate documentation, evaluate quality, and synthesize modern Java/Python services with tests.",
        version="0.1.0",
    )

    app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
    app.include_router(docgen.router, prefix="/docs", tags=["documentation"])
    app.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])
    app.include_router(codegen.router, prefix="/codegen", tags=["code-generation"])
    app.include_router(testgen.router, prefix="/testgen", tags=["test-generation"])

    return app


app = create_app()

