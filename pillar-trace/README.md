# pillar-trace

Free, small observability add-on for Pillar products. Spans and logs go to Neon through one ingest endpoint on the Pillar hub. Plain HTML dashboard with SQL filters. Built from the publicly described concept only (spans, logs, filters, alert rules); no third-party code.

## Use in a Python (FastAPI) product
1. Copy `pillar_obs.py` next to your app.
2. Env: `OBS_TOKEN` (ingest token from the hub vault entry for your project), `OBS_PROJECT=<name>`, optional `OBS_URL` (default hub).
3. In your app: `import pillar_obs; pillar_obs.install(app)`. Wrap work with `with pillar_obs.span("name"): ...`, call `pillar_obs.log("msg")`, check `pillar_obs.budget_over()` before paid calls.

## Use in a Node (Express) product
Copy `pillar_obs.js`, `import { install } from './pillar_obs.js'; install(app)`. Same env vars. Zero dependencies.

## Server side
`obs.py` lives in the hub (fizzle89/verticalos, app/obs.py): `POST /api/obs/ingest`, `/api/obs/traces`, `/api/obs/sql` (read-only, obs_ tables), alert rules and budgets. Dashboard: `/obs`.

## Rules
- Never record prompt text, user content or secrets in span attributes.
- Cost per token is an estimate; spans mark `cost_estimated`.
- Retention 7 days, row caps in the hub.
- New products: create an ingest token, add it to the hub `OBS_TOKENS_2` set, add default alert rules in `DEFAULT_RULES`.
