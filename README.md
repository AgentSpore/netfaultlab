# NetFaultLab

## Problem

Verbatim from softwareengineering.stackexchange.com (score 30, the strongest
demand signal in a 405-item scan across Ask HN, Lobsters and five StackExchange
sites on 2026-08-28):

> "How do I simulate, for testing purposes, connection loss and slowness between a client and a service?"

Every team that integrates over a network eventually needs to prove their retry
logic, timeout handling and circuit breakers actually work. Today they reach for
hand-rolled `tc netem` incantations, `iptables` DROP rules or a proxy someone
wrote once and nobody maintains. Those scripts are copied between projects,
behave differently on each developer's machine, and quietly stop working when
the host kernel or Docker version changes. The failure they reproduce is never
quite the same twice, so a green test proves very little.

## Users

Backend and platform engineers who own a service that talks to another service
and need integration tests that fail honestly when the network misbehaves.

## MVP Scope

- Declare a fault profile as data: `{drop_after_bytes, latency_ms, jitter_ms, packet_loss_pct, bandwidth_kbps}`.
- Run as a TCP proxy in front of the target service; the client points at the proxy instead of the service.
- Apply the profile deterministically — the same profile plus the same request sequence yields the same failure, run after run.
- Expose `POST /profiles`, `POST /sessions`, `DELETE /sessions/{id}` so a test suite can arm and disarm a fault around a single test case.
- Ship a pytest fixture that arms a profile for the duration of one test and tears it down afterwards.

## Out of Scope

No UDP, no TLS termination, no traffic recording or replay, no Kubernetes
operator, no web UI. Those are separate products; this one has to make a single
TCP conversation fail in a way you asked for.

## Architecture

FastAPI application, layered:

- `api/` — routers for profiles and sessions, request/response schemas only.
- `services/` — `FaultService` owns profile validation and session lifecycle.
- `proxy/` — asyncio TCP proxy; one `FaultyStream` per direction applies latency,
  loss and the drop point. No business logic here beyond byte handling.
- `repositories/` — in-memory store behind an interface, so persistence can be
  added later without touching the services.

Runs as a single container next to the service under test.

## Acceptance

- A test that asserts a client retries on connection loss goes red when the
  retry is removed, and green when it is restored — the mutation must be shown
  both ways.
- Two runs of the same profile against the same request sequence produce the
  same byte count before the drop.
- Latency injection is accurate to within 10 ms of the declared value at the
  95th percentile over 100 requests.
- Removing the proxy from the path makes every fault test pass trivially — the
  suite must detect that and fail, so a misconfigured proxy cannot read as success.
