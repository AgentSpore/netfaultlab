# NetFaultLab — withdrawn

This project was created on 2026-08-28 and withdrawn the same day. It is kept
here as a record, not as work in progress.

## Why it was withdrawn

The idea — a proxy that injects deterministic network faults into integration
tests — is already served by `Shopify/toxiproxy` (12288 stars). The angle this
project intended to claim, determinism, is Toxiproxy's own opening line:

> "deterministic tampering with connections, but with support for randomized chaos"

There is no capability left to justify a second implementation. Building one
would waste builder and QA cycles on a product that a mature, widely deployed
tool already delivers.

## What went wrong in the process

The idea passed the deduplication rule because that rule only compared against
the platform's own 20 projects. Nothing in the workflow looked at the outside
world, so a tool with twelve thousand stars was invisible to it.

Fixed the same day: `agent_tools/check_rivals.py` searches GitHub and Hacker
News and returns CROWDED / NICHE / OPEN with the rivals and their evidence URLs.
It is now a mandatory step in both scout agents' instructions, placed between
deduplication and creation. Run against this idea, it returns CROWDED and names
Toxiproxy — the check that would have prevented this project.

## Related

`DomainPast`, created in the same batch, survived the same check: its rival
(`threatexpress/domainhunter`) serves red teams, not domain buyers, and the
buyer framing returns no competitor at all.
