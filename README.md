# Maneuver Agent
This uses a Large Language Model (LLM) to propose, self‑critique, iterate, and finalize collision‑avoidance maneuvers for spacecraft conjunctions.

The system is **LLM‑agnostic** via a thin adapter (`call_adk_model`), allowing easy integration with different ADK / LLM providers (e.g., Google Gemini).

This component is part of the larger project `@leksialevin7700/space-debris-multi-llm` and corresponds to the **Model‑C (Maneuver Agent)** portion of that repository.

> **Security note**: Inject secrets at runtime only (environment variables or secret managers). Never commit API keys or bake them into images.

---

##  Key Capabilities

* Agentic workflow: **Propose → Self‑Critique → Decide → Finalize**
* Confidence‑based retry loop for improved decision quality
* Provider‑agnostic LLM integration via `call_adk_model`
* Supports **CLI**, **Web API**, and **scheduled** execution
* Structured outputs suitable for logs, files, or downstream pipelines

---

##  Workflow

<img
  src="https://github.com/user-attachments/assets/9a380b6f-31e6-4d0b-b08b-321919f91d66"
  alt="Maneuver Agent Workflow"
  width="200"
/>





**Decision logic:**

* If confidence ≥ threshold (default **80%**): finalize
* If confidence < threshold and attempts remain: retry
* Otherwise: finalize best available proposal

---

##  Output Schema

Each execution returns a structured result:

```json
{
  "final_decision": "Concise approved maneuver (≤ 3 lines)",
  "proposal": "Initial maneuver proposal",
  "critique": "Self‑critique with CONFIDENCE score",
  "confidence": 87,
  "attempts": 2,
  "all_attempts": [
    {"proposal": "...", "confidence": 62},
    {"proposal": "...", "confidence": 87}
  ]
}
```

## Usage

### CLI

```bash
python main.py SAT-A SAT-B --distance-km 0.12 --format yaml -o out.yaml
```

### Web API

```bash
python main.py --start-web --host 0.0.0.0 --port 8000
```

Example request:

```bash
curl -X POST http://localhost:8000/negotiate \
  -H "Content-Type: application/json" \
  -d '{"sat_a":"SAT-A","sat_b":"SAT-B","distance_km":0.12}'
```

---

## 🐳 Docker

### Build

```bash
docker build -t maneuver-agent:latest .
```

### Run (CLI)

```bash
docker run --rm --env-file .env \
  -v "$(pwd)/out:/out" \
  maneuver-agent:latest \
  python main.py SAT-A SAT-B --distance-km 0.12 -o /out/out.yaml
```

### Run (Web)

```bash
docker run --rm --env-file .env -p 8000:8000 \
  maneuver-agent:latest \
  python main.py --start-web --host 0.0.0.0 --port 8000
```

---

## 🧩 Docker Compose (Local Development)

```yaml
version: "3.8"
services:
  maneuver-agent:
    build: .
    env_file: .env
    ports:
      - "8000:8000"
    command: ["python","main.py","--start-web","--host","0.0.0.0","--port","8000"]
```

Start:

```bash
docker compose up --build
```

Deploy the container image and expose port **8000**.
---

## 📄 License

MIT License
