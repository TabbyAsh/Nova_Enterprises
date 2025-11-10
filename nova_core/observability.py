"""Observability helpers for metrics and tracing."""

from __future__ import annotations

import logging

try:  # pragma: no cover - optional dependency handling
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
except ImportError:  # pragma: no cover
    trace = None  # type: ignore[assignment]
    OTLPSpanExporter = None  # type: ignore[assignment]
    Resource = None  # type: ignore[assignment]
    TracerProvider = None  # type: ignore[assignment]
    BatchSpanProcessor = None  # type: ignore[assignment]

from prometheus_client import Counter, Gauge, Histogram

from .config import settings

LOGGER = logging.getLogger(__name__)

signals_emitted = Counter(
    "nova_signals_emitted_total",
    "Total number of signals emitted by the system.",
)
orders_submitted = Counter(
    "nova_orders_submitted_total",
    "Total number of orders submitted to brokers.",
)
open_positions = Gauge(
    "nova_open_positions",
    "Current number of open positions across all accounts.",
)
signal_confidence = Histogram(
    "nova_signal_confidence",
    "Distribution of generated signal confidence scores.",
    buckets=(0.1, 0.25, 0.5, 0.75, 0.9, 1.0),
)


def configure_tracing() -> None:
    """Configure OpenTelemetry tracing with OTLP exporter."""

    if trace is None or OTLPSpanExporter is None:
        LOGGER.warning("OpenTelemetry dependencies not installed; tracing disabled")
        return

    resource = Resource.create({"service.name": "nova-core"})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=settings.telemetry.otel_exporter_otlp_endpoint)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    LOGGER.info("OpenTelemetry tracing configured for NovaCore")


def increment_signal_metrics(confidence: float) -> None:
    """Record metrics for a generated signal."""

    signals_emitted.inc()
    signal_confidence.observe(confidence)


__all__ = [
    "configure_tracing",
    "increment_signal_metrics",
    "signals_emitted",
    "orders_submitted",
    "open_positions",
    "signal_confidence",
]
