#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pprint import pprint

# Import the agent implementation (adjust import if you placed the module elsewhere)
from maneuver_agent_adk import run_multi_llm_negotiation


def parse_args():
    p = argparse.ArgumentParser(
        description="Run the multi-LLM negotiation agent to propose and finalize a satellite maneuver."
    )
    p.add_argument("sat_a", nargs="?", help="Name/ID of satellite A")
    p.add_argument("sat_b", nargs="?", help="Name/ID of satellite B")
    p.add_argument(
        "--distance-km",
        type=float,
        help="Closest approach distance in kilometers (float)",
    )
    p.add_argument(
        "--max-attempts",
        type=int,
        default=3,
        help="Maximum number of propose/critique attempts (default: 3)",
    )
    p.add_argument(
        "--out",
        "-o",
        help="Optional path to write the full result JSON",
    )
    p.add_argument(
        "--start-web",
        action="store_true",
        help="Start the agent as a FastAPI web server",
    )
    p.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind the web server to (default: 0.0.0.0)",
    )
    p.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the web server to (default: 8000)",
    )
    return p.parse_args()


def main():
    args = parse_args()

    if args.start_web:
        import uvicorn
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel

        app = FastAPI(title="Maneuver Agent", description="Multi-LLM Negotiation Agent")

        class NegotiationRequest(BaseModel):
            sat_a: str
            sat_b: str
            distance_km: float
            max_attempts: int = 3

        @app.post("/negotiate")
        def negotiate(req: NegotiationRequest):
            print(f"Received negotiation request: {req}")
            try:
                result = run_multi_llm_negotiation(
                    req.sat_a, req.sat_b, req.distance_km, max_attempts=req.max_attempts
                )
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        print(f"Starting web server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
        return

    # If not web server, ensure required args are present
    if not args.sat_a or not args.sat_b or args.distance_km is None:
        p.print_help()
        sys.exit(1)

    # Basic sanity checks (can be extended)
    if args.distance_km < 0:
        raise SystemExit("distance-km must be non-negative")

    print(f"Running negotiation for {args.sat_a} vs {args.sat_b} (closest approach {args.distance_km:.2f} km)")
    print(f"Max attempts: {args.max_attempts}")
    print("----")

    result = run_multi_llm_negotiation(args.sat_a, args.sat_b, args.distance_km, max_attempts=args.max_attempts)

    print("\n==== Summary ====")
    print(f"Attempts performed: {result.get('attempts')}")
    print(f"Best confidence: {result.get('confidence')}%")
    print("\nFinal approved maneuver (3 lines):")
    print(result.get("final_decision") or "(no final decision)")

    print("\nLast critique:")
    print(result.get("critique") or "(no critique)")

    # Pretty-print all attempts if present
    all_attempts = result.get("all_attempts")
    if all_attempts:
        print("\nAll attempts detail:")
        pprint(all_attempts)

    # Optionally write JSON output
    if args.out:
        out_path = os.path.expanduser(args.out)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nFull result written to {out_path}")


if __name__ == "__main__":
    main()