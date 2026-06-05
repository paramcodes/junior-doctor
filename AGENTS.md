# AGENTS.md

## Project Goal

Build a safe AI-powered discharge summary generation system from scanned patient PDFs.

The system must:

* Ingest scanned and text-based PDFs
* Extract structured clinical evidence
* Reconcile admission vs discharge medications
* Detect conflicting information
* Flag missing information
* Generate a discharge summary draft
* Generate execution traces
* Generate clinician review flags

The system prioritizes safety over completeness.

If information is unavailable:

* Never fabricate
* Never infer
* Never guess

Use "Not Documented" instead.

---

## Core Principle

Unknown > Wrong

The system should prefer reporting uncertainty rather than inventing clinical information.

---

## Architecture

PDF
→ Text Extraction (PyMuPDF)
→ OCR Fallback (Tesseract)
→ Evidence Extraction (Gemini)
→ Evidence Aggregation
→ Agent State

Agent Loop:

1. Medication Reconciliation
2. Conflict Detection
3. Validation
4. Summary Generation
5. Export Results

Outputs:

* summary.md
* trace.md
* review_flags.md

---

## Engineering Constraints

### Do

* Use Pydantic models
* Use typed functions
* Keep modules small
* Keep business logic deterministic where possible
* Add docstrings
* Add logging
* Handle failures gracefully

### Do Not

* Put business logic inside prompts
* Put business logic inside the agent loop
* Use global state
* Silently swallow exceptions
* Hallucinate missing information

---

## Safety Requirements

If evidence is missing:

Return:

"Not Documented"

Do NOT generate plausible values.

If conflicts exist:

Create a ReviewFlag.

Do NOT choose a winner.

---

## LLM Usage

Gemini should only be used for:

1. Evidence Extraction
2. Summary Generation

Everything else should be deterministic Python code whenever possible.

---

## Output Quality

Every extracted fact should preserve provenance.

Every fact should be traceable to:

* page number
* source document
* source text

---

## Development Strategy

Build incrementally.

Sprint 1:

* PDF Extraction
* OCR
* Evidence Extraction

Sprint 2:

* Evidence Aggregation
* Medication Extraction
* Reconciliation

Sprint 3:

* Conflict Detection
* Validation

Sprint 4:

* Agent Loop

Sprint 5:

* Summary Generation
* Exporters

Never start Sprint N until Sprint N-1 works.
