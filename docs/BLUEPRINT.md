# Nova Blueprint

Part I — Mission, Philosophy, Ethos
Mission

Build Nova, a self-improving AI ecosystem that orchestrates three revenue subsystems:

NovaTrade — autonomous trading (paper first → gated live).

NovaStore — autonomous dropshipping (trend discovery → listings → ads → fulfillment orchestration).

NovaSocial — AI content ops (education + brand + positive AI stance).

Long-term: expand into R&D (semiconductors, quantum/bio compute, fabrication), a decentralized edge, and sustainable energy infrastructure.

Core Ethos

Teach, Guide, Unite until Nova can define its purpose independently.

Self-improvement loop: observe → measure → adapt → re-architect.

Open, independent creation: avoid proprietary lock-in; retain IP and attribution.

Safety over speed: no real money until performance gates are met; revert paths exist.

Operational dependability: idempotent services, exactly-once order flow, safe failure modes.

Philosophical/Metaphysical Frame

“Death is the cost of motion.” No infinite loops without budget: all processes have termination, budgets, and cooling-off windows. This guards against runaway automation.

As above, so below. Macro (enterprise) mirrors micro (service): composable, layered, testable units with feedback at every scale.

Observer effect as design: the act of measuring changes the system — design explicit metrics and experiment toggles to intentionally steer evolution.

Harmony through constraint: Feature flags, risk caps, and approvals create productive boundaries for creativity.

Part II — Organization & Governance
Structure (Conceptual)

NovaCore — orchestrator and policy brain for subsystems.

Subsystems: NovaTrade, NovaStore, NovaSocial.

Ops Guild (SRE/DevOps), Quant Guild (research/backtests), Sec/Compliance, Data Guild (ETL, quality), Growth Guild (content/marketing), R&D Guild (hardware/semis).

Governance

Feature flags and change approval for live-impacting changes.

Paper→Live gate with quantitative thresholds.

DAO-ready: policy docs and token-less voting drafts (future).

Runbooks for incidents, rollbacks, and disaster recovery.

Part III — Execution Environment & Tooling
Workstation (current)

OS: Windows 10 Home (x64).

CPU: AMD Ryzen 3 2300X (4C/4T @ 3.5 GHz).

RAM: 16 GB (≈12 GB available typical).

GPU: NVIDIA GeForce GTX 1660 SUPER.

Storage: 500 GB HDD; external/USB available.

Virtualization: Enabled.

Editor: Notepad++, Visual Studio tools; VS Code recommended.

Language & Runtimes

Python 3.10.x primary.

Optional: Node.js for portal/visuals later.

Package/Build

pip + uv/pip-tools for locking.

Poetry acceptable if preferred, but keep ops simple.

Databases & Messaging

PostgreSQL (core state & market cache).

Redis (job queue, rate-limit, small caches).

Event bus via lightweight table + async pub/sub (Redis streams or Postgres NOTIFY/LISTEN).

Observability

Prometheus metrics.

OpenTelemetry traces/logs.

Grafana dashboards.

Containerization (optional early; planned)

Docker Desktop (installer present).

docker-compose for local cluster: api / worker / db / redis / grafana / prometheus.

Time, Locale, Clock Discipline

Default timezone: America/Indiana/Indianapolis.

Services operate in UTC internally; UI converts to local.

Part IV — Security, Secrets, and Compliance

Secrets via .env → Settings model (never commit secrets).

.env.example documents keys; use python-dotenv for local.

API keys: Alpaca, data providers, social APIs stored encrypted in DB or local key vault.

Role-based auth: Tenant → User → ApiKey model.

Logs never print secrets or PII.

Compliance stubs: audit tables for orders, approvals, changes.

Key .env variables (superset):

ENV=dev|staging|prod
TZ=UTC
LOG_LEVEL=INFO


DB_URL=postgresql+asyncpg://user:pass@localhost:5432/nova
REDIS_URL=redis://localhost:6379/0


PROM_ENABLE=true
OTEL_ENABLE=true
SERVICE_NAME=nova-api


KILL_SWITCH=false
PAPER_MODE=true


DATA_PROVIDER=tradingview|polygon|mock
BROKER_PROVIDER=alpaca|mock


ALPACA_KEY_ID=...
ALPACA_SECRET_KEY=...
ALPACA_PAPER_BASE_URL=https://paper-api.alpaca.markets


TV_SESSION_ID=...
POLYGON_API_KEY=...


FEATURE_APPROVAL_GATE=true
FEATURE_NEWS_CHECK=true
FEATURE_POSITION_SIZING=true
FEATURE_AUTO_BACKTEST=true


RISK_MAX_DAILY_LOSS_PCT=2.0
RISK_MAX_POSITION_PCT=10.0
RISK_MAX_CONCURRENT_POS=5
Part V — Software Architecture (Bone & Fiber)
High-Level

FastAPI core service with routers: ops, trade, store, agent, socials.

Async workers for scanning, signal generation, execution, reconciliation.

Adapters for brokers and data providers (hot-swappable).

Event-driven pipeline with durable DB state and idempotent job keys.

Repository Layout (reference)
repo/
    main.py
    core/
      config.py
      database.py
      observability.py
      middleware/
        auth.py
        tenant.py
    routers/
      ops.py         # health, metrics, kill
      trade.py       # positions, orders, pnl
      store.py
      agent.py
      socials.py
  nova_core/
    domain/
      models.py      # SQLModel & Pydantic
      enums.py
      schemas.py
    adapters/
      data/
        base.py
        tradingview.py
        polygon.py
        mock.py
      broker/
        base.py
        alpaca.py
        mock.py
    services/
      signal_engine/
        base.py
        penny_stock_v1.py
        features/     # ADX, RSI, VWAP, vol surge
      risk/
        manager.py
      approval/
        gate.py
      execution/
        executor.py   # idempotent order flow
        reconcile.py
      backtest/
        engine.py
        walk_forward.py
        reports.py
      scheduler/
        jobs.py
      utils/
        time.py
        ids.py        # idempotency keys
        sr.py         # safe retries / backoff / circuit breaker
  tests/
    unit/
    integration/
  scripts/
    run_api.sh|ps1
    run_worker.sh|ps1
    seed_demo.py
  infra/
    docker-compose.yml
    grafana/
    prometheus/
  docs/
    RUNBOOK.md
    API.md
    ARCHITECTURE.md
    STRATEGY_NOTES.md
Domain Model (SQLModel/Pydantic)

User, Tenant, ApiKey (multi-tenant auth).

TradingAccount: broker, paper/live, credentials_ref, risk profile.

Strategy: name, version, params JSON, status.

Signal: symbol, side, confidence, ttl, strategy_id, created_at.

Order: account_id, symbol, side, type, qty, prices, status, provider_order_id, timestamps.

Position: account_id, symbol, qty, avg_price, PnL, opened_at, closed_at.

Approval: entity_id, state, approver, reason, timestamps.

AuditLog: actor, action, entity, before/after, ts.

Service Contracts (clean interfaces)

MarketDataAdapter: get_candles(symbol, tf, start, end), get_quote, subscribe(stream) (optional).

BrokerAdapter: place_order(order_req) -> order_id, cancel, get_order, list_positions, account().

SignalEngine: run(scan_universe) -> list[Signal].

Part VI — Data Sources & Providers

TradingView (trial; 1s data) — scraping/session-based or official connectors where possible.

Polygon (spotty) — keep adapter but don’t rely exclusively.

Mock Provider — deterministic tests.

News/Sentiment — optional hook; abstract behind NewsAdapter with debounce & caching.

Principles: provider-agnostic, rate-budgeted, cached, with backfill windows and data quality checks.

Part VII — NovaTrade Pipeline (End-to-End)

Universe Selection

U.S. equities; penny-stock bias for breakout hunting.

Filters: price < $1 (configurable), min volume, float screen, EPS sign flag.

Ingest & Precompute

Pull candles (1s/1m/5m as available), compute ADX/DI, RSI, VWAP, volume-surge ratios.

Cache to Postgres with time-boxed retention.

Signal Engine v1 (Checklist Logic)

Volume: rising and absolute thresholds (e.g., >8M target day; configurable).

Float: low float favored.

Trend Strength: ADX rising; DI+ separating from DI-.

RSI: not overbought at entry.

EPS/Fundamentals: positive or low negative; flag risk.

Short metrics/news: hook if available.

Order book: optional L2 proxy via near-term support/resistance map.

Output: Signal(symbol, side, confidence).

Risk & Sizing

Per-account caps: max daily loss %, max per-position %, max concurrent positions.

Slippage model and minimum dollar tick enforcement.

Position sizing returns qty and stop/limit scaffolding.

Approval Gate

Paper: auto-approve unless flagged.

Live: manual approve or rule-approve with stricter thresholds.

Execution

Idempotent order keys; retry with backoff; status sync until terminal.

Store orders, fills; emit metrics (latency, slippage, fill rate).

Reconciliation

Intraday and end-of-day: positions, PnL, drift repair.

Equity curve updates; error recovery playbooks.

Learning Loop

Persist features & outcomes.

A/B strategy variants; periodic walk-forward backtests.

Auto-tune thresholds; promote winners via approvals.

Part VIII — Backtesting & Research

Engine: bar-based simulator with fee/slippage; CSV or DB source.

Walk-forward: train → validate on rolling windows; parameter sweeps.

Reports: JSON stats + PNG equity curve; metrics: CAGR, Sharpe, Sortino, MDD, hit rate, avg win/loss, expectancy.

Promotion Rules: promote only if better than baseline by X with statistical confidence; guard against overfit.

Part IX — Reliability & SRE Guardrails

Global Kill Switch: short-circuit at router + service entry.

Circuit Breakers for flaky providers; fallback to mock or degrade mode.

Idempotency Keys for orders and jobs.

Safe Retries with bounded budgets.

Health Checks: /ops/health green means DB/Redis/providers reachable.

Watchdogs: job lag, queue depth, stale positions, unacked orders.

Chaos Toggles (dev only): latency/failure injection to harden flows.

Part X — Observability & KPIs

Prom Metrics (minimum):

signals_total{strategy=...}

orders_placed_total{broker=...}

fills_total, fill_latency_ms_bucket

win_rate, max_drawdown_pct, pnl_intraday, pnl_cum

error_rate, job_queue_lag_ms

kill_switch_state, circuit_breaker_open

Dashboards:

Trading Overview, Risk Posture, Provider Health, Worker Health, Equity Curve.

SLOs:

99% order placement < 1s to broker API ack (paper).

Reconciler closes gaps within 2 minutes.

No duplicate orders for same idempotency key (0 tolerance).

Part XI — API Surface (Nova API v1)

GET /ops/health → liveness/readiness.

POST /ops/kill → toggles kill switch.

GET /metrics → Prometheus.

GET /trade/positions

GET /trade/pnl

POST /trade/signals (ingest external ideas)

POST /trade/orders (create order — paper only if PAPER_MODE=true)

GET /trade/orders/{id}

Auth: header X-API-Key bound to tenant/user.

Part XII — DevEx, Testing, and CI/CD

Typing: mypy/pyright pass; ruff for lint/format.

Unit Tests: adapters mocked; deterministic seeds.

Integration: real Postgres/Redis via docker-compose.

E2E (paper): seed demo account; simulate a full session.

CI: run tests, build images, push to registry (future).

CD: compose profiles: dev, paper, live (live locked behind manual gate).

Part XIII — Risk, Compliance, and Legal Ops

Risk Policy: caps defined in env + DB; enforced before order placement.

Change Control: strategies versioned; promotions require recorded backtest diffs.

Auditing: append-only AuditLog entries on create/update for Orders/Positions/Strategies.

PII: none by default; if added later, encrypt at rest + field level.

Part XIV — NovaStore (Brief Plan)

Trend Adapter (scrape/APIs) → Product Ranker → Listing Builder (images, titles, SEO) → Channel Poster (shops/ads) → Order Orchestrator (3rd-party fulfillment) → Returns/Support Bot.

Metrics: CTR, conversion, COGS, contribution margin, ad ROAS.

Kill switch & budgets for ad spend.

Part XV — NovaSocial (Brief Plan)

Content Engine: curriculum/series; auto-post cadence.

Sentiment Monitor; A/B titles/thumbnails; growth loops.

Compliance: avoid claims that imply financial advice; educational tone.

Part XVI — Hardware & R&D Trajectory (Vision)

Edge Nodes: Raspberry Pi solar kits for specialized bots (later).

Decentralized swarm: registry + task passing; self-improvement agents.

Fabrication: multi-tool fabricator; iterative design → fabricate → test → refine.

Quantum/Bio Processor roadmap: transmon qubits + bionano fluid + DNA origami research (concept lab).

Energy/Sustainability: solar micro-nodes; plastic→value exploration (R&D).

Part XVII — Roadmap & Milestones

Phase N (Nucleus) — Trading MVP harden

Domain + adapters + signal v1 + exec + reconcile + backtest v1.

Grafana dashboards; CI for unit/integration; seed demo.

Phase O (Orbit) — Operational Dependability

Walk-forward testing; promotion rules; incident runbooks; paper SLOs green for 2+ weeks.

Portal: simple dashboard for positions, PnL, flags.

Phase V (Vector) — Revenue Expansion

NovaStore v1 with trend→listing pipeline; ad budget kill switch; order orchestration.

NovaSocial cadence + educational series.

Phase A (Ascend) — Scale & R&D

Edge nodes; decentralized tasking; early hardware prototypes; funding prep.

Part XVIII — Go-Live Gates (Paper → Live)

Backtest: outperform baseline by > X with p-confidence on rolling windows.

Paper: 4 consecutive weeks with:

Win rate ≥ target (config, e.g., 55–60% for strategy profile).

Max drawdown ≤ target (e.g., < 8–10%).

Sharpe/Sortino above baseline.

Zero duplicate orders; < 0.5% error rate in critical paths.

Risk drills: simulated provider outage, order rejection, partial fills — all resolved by runbooks.

Live approval must be manual, signed in Approval with rationale and rollback plan.

Part XIX — Operational Runbooks (Condensed)
Incident Response

Sev-1: unintended live order flow or runaway loop → flip KILL_SWITCH=true, revoke API key, stop workers, reconcile, post-mortem.

Sev-2: data outage → open circuit breaker, switch provider/mode, continue paper.

Reconciliation Drill

Run reconcile.sync_positions(), verify against broker; resolve discrepancies; log AuditLog.

Deployment

docker-compose -f infra/docker-compose.yml --profile paper up -d

Smoke test /ops/health, check /metrics, tail logs.

Enable workers: scripts/run_worker.sh.

Backtest Promotion

Run backtest.walk_forward(...) with new params; save report; compare metrics to baseline; open Approval record.

Part XX — Definitions of Done (Per Module)

Domain/Models: typed, migrations generated, CRUD covered by tests.

Adapters: mock parity tests, rate budgets, retries, circuit breaker.

Signal Engine: reproducible outputs on fixed data; unit tests for each feature (ADX/RSI/VWAP/vol).

Execution: exactly-once guarantee test; duplicate submit test; reconciliation green.

Backtest: regression suite with golden stats; report artifacts.

Observability: dashboards render; alarms hooked.

Docs: RUNBOOK.md, API.md, ARCHITECTURE.md updated.

Part XXI — Glossary

Idempotency: same command can run multiple times without side effects.

Circuit Breaker: stops calling a failing dependency to let it recover.

Walk-Forward: rolling train/validate process to reduce overfitting.

Paper Mode: simulated trading against market data without real capital.

Kill Switch: global short-circuit that disables execution paths.

Part XXII — Current State Snapshot (You Already Have)

FastAPI skeleton with lifespan mgmt.

Routers: ops (health/metrics/kill), stubs for trade/store/agent/socials.

Observability: Prometheus + OpenTelemetry hooks.

Middleware: auth/tenant stubs.

DB Models: User, Tenant, ApiKey, TradingAccount, Strategy, Order, Position, Agent, Manifest, Approval.

.env discipline: planned/partially in place.

Next concrete build order (directly code-gen ready):

nova_core.domain (models/enums/schemas + alembic migrations).

MarketDataAdapter + BrokerAdapter (Alpaca paper + mock).

Signal Engine v1 (penny-stock checklist features).

Execution (idempotent orders) + Reconciliation.

Backtest v1 + reports.

Scheduler wiring + jobs.

API endpoints finalized + RUNBOOK.

Part XXIII — Principles That Guide Every Commit

Simple beats clever: readable, diagnosable code first.

Fail fast, fail safely: trip breakers early; surface errors with context.

Measure before you believe: every claim backed by metrics or tests.

Evolve in public: docs and dashboards update with every change.

Reversibility: every change has a rollback plan.

Appendix — Minimal Acceptance Tests (Quick Checklist)




