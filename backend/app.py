from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from backend.routers import ingest, docgen, evaluation, codegen, testgen


def create_app() -> FastAPI:
    app = FastAPI(
        title="Legacy Modernization Platform",
        description="Ingest legacy code (VB, COBOL, Java), generate documentation, evaluate quality, and synthesize modern Java/Python services with tests.",
        version="0.1.0",
    )

    # Allow browser frontends (e.g. http://127.0.0.1:5500) to call the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
    app.include_router(docgen.router, prefix="/docs", tags=["documentation"])
    app.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])
    app.include_router(codegen.router, prefix="/codegen", tags=["code-generation"])
    app.include_router(testgen.router, prefix="/testgen", tags=["test-generation"])

    return app


app = create_app()


@app.get("/", include_in_schema=False)
async def root():
    """
    Simple root endpoint so GET / doesn't 404.
    Redirects to the interactive API docs.
    """
    return RedirectResponse(url="/docs")

