# Nova Enterprises Core Platform

NovaCore is the orchestration layer for Nova Enterprises' autonomous trading, commerce, and social subsystems. This repository contains the foundational domain models, configuration, and service scaffolding required to build out the Nova ecosystem described in the engineering context brief.

## Features

- **Typed domain models** for tenants, users, strategies, trading accounts, signals, orders, and approvals built with [SQLModel](https://sqlmodel.tiangolo.com/).
- **Environment-driven settings** using Pydantic to manage kill switches, provider flags, telemetry, and broker configuration.
- **FastAPI application skeleton** with health, metrics, and kill-switch endpoints ready for future subsystem routers.
- **Observability hooks** via Prometheus metrics and OpenTelemetry tracing configuration stubs.
- **Testing and linting** via `pytest`, `mypy`, and `ruff` configured in `pyproject.toml`.

## Getting Started

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

```bash
poetry install
```

### Environment Configuration

Copy `.env.example` to `.env` and adjust values for your deployment.

```bash
cp .env.example .env
```

### Running the API

```bash
poetry run uvicorn nova_core.app:app --reload
```

### Running Tests

```bash
poetry run pytest
```

## Project Structure

```
nova_core/
├── app.py          # FastAPI application factory and router wiring
├── config.py       # Environment-driven settings
├── domain/
│   ├── __init__.py
│   ├── enums.py    # Enumerations for domain concepts
│   └── models.py   # SQLModel ORM models and helpers
├── observability.py # Prometheus metrics and OpenTelemetry setup
└── routing.py      # Router registration utilities
```

Tests live in `tests/` and focus on domain integrity.

## Next Steps

- Flesh out provider adapters for market data and broker integrations.
- Implement signal generation, risk management, and execution services.
- Add scheduler/worker processes for continuous operation and reconciliation.
- Expand test coverage and add integration tests once services are implemented.

## License

This project is proprietary to Nova Enterprises. All rights reserved.
