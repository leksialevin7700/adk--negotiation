# Maneuver Agent

An **agentic satellite maneuver proposal system** that uses a Large Language Model (LLM) to propose, self‑critique, iterate, and finalize collision‑avoidance maneuvers for spacecraft conjunctions.

The system is **LLM‑agnostic** via a thin adapter (`call_adk_model`), allowing easy integration with different ADK / LLM providers (e.g., Google Gemini).

This component is part of the larger project `@leksialevin7700/space-debris-multi-llm` and corresponds to the "model C" portion of that repository.

Inject secrets at runtime (never commit keys or bake them into images).

---

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

## Docker

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

## Docker Compose (Local Dev)

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

---

## Kubernetes 

Create secret:

```bash
kubectl create secret generic maneuver-secret \
  --from-literal=GEMINI_API_KEY=sk-...
```

Deploy your container image and expose port `8000`. Add readiness/liveness probes and resource limits before production use.

---

## License

MIT License.

---
