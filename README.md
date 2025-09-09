# Gophish Auto-Context Plugin (MVP Scaffold)

A sidecar CLI that talks to the Gophish REST API to bootstrap realistic phishing campaigns.
This MVP focuses on the **plumbing** (create group, template, landing page, campaign) so we can
add enrichment and validation layers next.

## Quick start

1) Install:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Prepare a recipients CSV with headers: `first_name,last_name,email,role`
See `examples/recipients.csv`.

3) Run (dry-run by default):
```bash
python -m gacp.cli       --gophish-url http://127.0.0.1:3333       --api-key YOUR_API_KEY       init-campaign       --campaign-name "MVP Demo"       --domain example.com       --recipients examples/recipients.csv       --send-start "2025-09-12T09:00:00"
```

The MVP will:
- Create a Group (from CSV)
- Create an Email Template (generic placeholder for now)
- Create a Landing Page (generic placeholder for now)
- Create a Campaign (scheduled start)

Use `--execute` to actually call the Gophish API (default is dry-run).

## Next steps (planned)
- Enrichment: logo/brand color fetch, DNS hints (MX/SPF), timezone inference
- Confidence scoring + validation with safe fallbacks
- Role-aware lure selection (via YAML lures)
- Report generator (HTML/PDF) explaining auto-choices
