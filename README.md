## Legacy Modernization Platform (VB / COBOL → Java & Python)

This project is a skeleton implementation of an end‑to‑end platform that:

- **Ingests legacy code** (VB, COBOL, legacy Java)
- **Generates system and module documentation**
- **Evaluates documentation quality** and exposes metrics for a **dashboard**
- **Generates modern target code** (Java/Python) following a service architecture
- **Generates unit tests** corresponding to the new code

All "intelligent" behavior (parsing, LLM calls, IR construction, etc.) is modeled as **clear extension points** so you can plug in your own models and tools.

---

### Project Structure

- `backend/`
  - `app.py` — FastAPI app wiring all routers.
  - `routers/ingest.py` — Ingest legacy code files and create an analysis session.
  - `routers/docgen.py` — Stub endpoint for documentation generation.
  - `routers/evaluation.py` — Stub endpoint exposing coverage/confidence metrics.
  - `routers/codegen.py` — Stub endpoint for target code generation.
  - `routers/testgen.py` — Stub endpoint for unit test generation.
- `frontend/`
  - `index.html` — Minimal, modern dashboard UI calling the backend APIs.
- `requirements.txt` — Python backend dependencies.

---

### Running the Backend

Create and activate a virtual environment (recommended), then install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI app with Uvicorn:

```bash
uvicorn backend.app:app --reload
```

The OpenAPI docs will be available at:

- `http://127.0.0.1:8000/docs`

---

### Using the Frontend Dashboard

You can serve the static `frontend/index.html` with any static file server, or simply open it in a browser while the backend is running.

- The **Run pipeline** button will:
  - Upload selected legacy files to `/ingest/legacy-code`
  - Trigger documentation generation at `/docs/generate`
  - Fetch metrics from `/evaluation/metrics`
  - Request target code and unit-test generation from `/codegen/generate` and `/testgen/generate`
- The **metrics card** visualizes coverage and confidence (currently placeholder values).

In a production setup, you would:

- Host the frontend behind the same domain as the backend (or add CORS settings).
- Extend the backend routers to:
  - Parse VB/COBOL/Java into an intermediate representation.
  - Call your LLM(s) with retrieval-augmented prompts for documentation and code-gen.
  - Store artifacts and metrics in a database / object storage.

---

### Next Steps / Extension Points

- **Ingest & IR**
  - Replace the placeholder ingest implementation with real parsing and storage.
  - Design a language-agnostic intermediate representation for control flow and data.
- **Documentation Generation**
  - Plug in an LLM (via API) and a vector store to do RAG over parsed code.
  - Persist generated docs and map them back to code modules and data fields.
- **Evaluation & Dashboard**
  - Implement true coverage metrics and LLM-based self-critique for documentation.
  - Store metrics in a DB and enhance the dashboard with module-level drill-downs.
- **Code & Test Generation**
  - Implement mappings from the IR + docs to Java/Python templates.
  - Generate and run unit tests, feeding failures back into an improvement loop.

This skeleton is intended as a **starting point** you can evolve into a full legacy‑to‑modern conversion solution.

