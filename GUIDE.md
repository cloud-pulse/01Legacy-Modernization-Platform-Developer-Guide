## Legacy Modernization Platform – Developer Guide

This app is a **prototype platform** for modernizing legacy applications (VB, COBOL, old Java) into **documented, testable Java/Python services**.  
It provides:

- **Ingestion** of legacy source files.
- **Documentation generation** (LLM-ready hooks, plus stub implementation).
- **Documentation quality metrics** for a dashboard.
- **Target code generation** (Java/Python) – stubbed but writing real files.
- **Unit test generation** – stubbed but writing real files.
- A **web UI dashboard** to drive the pipeline and see metrics.

---

## 1. Project Layout

- **`backend/`**
  - `app.py` – FastAPI app; wires all routes and enables CORS.
  - `routers/ingest.py` – uploads files, creates a `session_id`, writes input under `output/`.
  - `routers/docgen.py` – docs generation:
    - `/docs/generate` → stub, writes JSON docs to `output/`.
    - `/docs/generate-llm` → real LLM example for a single code snippet.
  - `routers/evaluation.py` – documentation metrics (stub), writes metrics JSON to `output/`.
  - `routers/codegen.py` – generates **placeholder target code** files into `output/`.
  - `routers/testgen.py` – generates **placeholder unit tests** into `output/`.
- **`frontend/`**
  - `index.html` – dark-mode dashboard that talks to the backend.
- **`output/`** (created at runtime)
  - `sessions/{session_id}/input/` – uploaded legacy source.
  - `sessions/{session_id}/docs/` – docs + metrics.
  - `sessions/{session_id}/code/{target_lang}/` – generated code.
  - `sessions/{session_id}/tests/{target_lang}/` – generated tests.
- **`requirements.txt`** – Python dependencies.
- **`README.md`** – original high-level readme.

---

## 2. One‑Time Setup

### 2.1. Create and activate a Python virtual environment (Windows)

From the project root `C:\workspace\AI-code-gen`:

```powershell
# Create venv (if not already present)
py -m venv .venv

# Activate it
.\.venv\Scripts\activate
```

You should now see `(.venv)` at the start of your PowerShell prompt.

### 2.2. Install dependencies

Still in the venv:

```powershell
pip install -r requirements.txt
```

This installs:

- `fastapi`, `uvicorn`, `python-multipart`
- `openai` (for the LLM example endpoint)

---

## 3. Running the Backend

### 3.1. Set your OpenAI API key (optional but needed for the LLM example)

If you want to use `/docs/generate-llm`:

```powershell
$env:OPENAI_API_KEY = "sk-...your-key..."
```

(Use `export OPENAI_API_KEY="..."` instead if you are in Git Bash.)

### 3.2. Start the FastAPI server

In the same terminal (venv still active):

```powershell
python -m uvicorn backend.app:app --reload
```

What you get:

- API base URL: `http://127.0.0.1:8000`
- Interactive docs (Swagger): `http://127.0.0.1:8000/docs`
- Root `/` redirects to `/docs`.

---

## 4. Running the Frontend (UI Dashboard)

Open a **second terminal**:

```powershell
cd C:\workspace\AI-code-gen\frontend

# Simple static server on port 5500
python -m http.server 5500
```

Then open in your browser:

- `http://127.0.0.1:5500/index.html`

The UI expects the backend on `http://127.0.0.1:8000` (already wired in JS and allowed by CORS).

---

## 5. Using the App – End‑to‑End Flow

### 5.1. Upload and run steps from the UI

In the browser (frontend):

1. **Choose Files** – select your legacy source files (VB, COBOL, Java, etc.).
2. Pick a **target language** (Java or Python).
3. Choose what you want:
   - **Run pipeline** – does all steps in sequence:
     - Uploads files and creates a `session_id`.
     - Generates docs (stub) and metrics.
     - Generates placeholder target code.
     - Generates placeholder tests.
   - **Docs only** – runs documentation + metrics only.
   - **Code only** – runs code generation only.
   - **Tests only** – runs test generation only.

As you run steps, the **status text** at the bottom of the left card updates, and the right card displays coverage/confidence metrics (currently static stub values).

The session label (e.g., `Session: 0cab...`) shows which folder under `output/` corresponds to this run.

### 5.2. Where to find outputs

Given a `session_id` (shown in the UI), all artifacts live under:

```text
output/
  sessions/
    {session_id}/
      input/         # Uploaded legacy source files
      docs/
        summary.json # Stub documentation from /docs/generate
        metrics.json # Stub metrics from /evaluation/metrics
      code/
        java/ or python/
          SampleService.java or sample_service.py
      tests/
        java/ or python/
          SampleServiceTest.java or test_sample_service.py
```

Over time, as you replace stubs with real logic, these paths remain the same but files will contain **real docs, code, and tests**.

---

## 6. LLM Example: Generating Docs for a Single Snippet

To see real LLM behavior (not stubs):

1. Ensure `OPENAI_API_KEY` is set and backend is running.
2. Go to `http://127.0.0.1:8000/docs`.
3. Find **POST `/docs/generate-llm`**.
4. Use a body like:

```json
{
  "code": "IF ACCOUNT-BALANCE < 0 THEN ...",
  "language": "COBOL"
}
```

5. Click **Execute**.

You’ll get a JSON document with fields like `purpose`, `inputs`, `outputs`, `main_steps`, `business_rules`.  
This endpoint demonstrates how LLMs will be plugged into full session‑level documentation later.

---

## 7. Architecture Overview (Text Diagrams)

### 7.1. High‑level components

```text
+-----------------+           +----------------+           +------------------+
|  Browser UI     |  HTTP     |  FastAPI App   |   FS      |   output/ folder |
| (index.html)    +----------->  backend.app   +-----------> sessions/{id}/   |
+-----------------+           +----------------+           +------------------+
       |                               |
       | calls REST endpoints          |
       v                               v
  /ingest/legacy-code          routers/ingest.py
  /docs/generate               routers/docgen.py
  /evaluation/metrics          routers/evaluation.py
  /codegen/generate            routers/codegen.py
  /testgen/generate            routers/testgen.py
```

### 7.2. Per‑session artifact structure

```text
output/
  sessions/
    {session_id}/
      input/          <- raw uploaded legacy source files
      docs/
        summary.json  <- generated documentation (stub or LLM-backed)
        metrics.json  <- coverage/confidence metrics
      code/
        java/         <- generated Java code (placeholder)
        python/       <- generated Python code (placeholder)
      tests/
        java/         <- generated Java tests (placeholder)
        python/       <- generated Python tests (placeholder)
```

### 7.3. Logical data flow

```text
[Legacy files] --upload--> /ingest/legacy-code
      |                          |
      |                      write files to
      |                      output/sessions/{id}/input
      v                          |
  session_id  <------------------+
      |
      +--> /docs/generate        -> write docs JSON under docs/
      |
      +--> /evaluation/metrics   -> write metrics JSON under docs/
      |
      +--> /codegen/generate     -> write sample code under code/{lang}/
      |
      +--> /testgen/generate     -> write sample tests under tests/{lang}/
```

---

## 8. What You Need to Do Next (as a Developer)

- **To run the prototype**:
  - Follow sections 2–5 (create venv, install dependencies, run backend + frontend, use UI).
- **To turn it into a real modernization tool**:
  - In `ingest.py`: parse VB/COBOL/Java into a proper intermediate representation (IR).
  - In `docgen.py`: replace `/docs/generate` stub with LLM‑based, IR‑aware documentation generation.
  - In `evaluation.py`: compute real coverage/confidence metrics.
  - In `codegen.py` and `testgen.py`: call LLMs to write **real** Java/Python services and tests into the `output/sessions/{id}` trees.

Reading this guide should give you:

- **What this app is for** → legacy‑to‑modern conversion prototype.
- **How to get it running** → venv, backend, frontend.
- **Where to find artifacts** → `output/sessions/{session_id}/...`.
- **Where to extend it** → specific router files for ingest, docs, evaluation, codegen, and testgen.

