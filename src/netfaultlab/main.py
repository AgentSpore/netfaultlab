"""NetFaultLab — FastAPI entrypoint (thin shell).

G1 establishes the importable app, permissive CORS, and a /health probe.
Domain routers (api/faults.py, api/proxies.py, api/scenarios.py) are added
in later groups. Keep this file small on purpose so G3 wiring stays simple.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__

app = FastAPI(
    title="NetFaultLab",
    version=__version__,
    description=(
        "A sandbox for deterministic network-fault injection in integration tests. "
        "Configure proxies, apply fault rules, and exercise error paths in CI."
    ),
)

# Permissive CORS — the fault injector is an internal test-tool endpoint.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
async def health() -> dict:
    """Liveness probe. Always 200 if the process is up."""
    return {"status": "ok", "version": __version__}
