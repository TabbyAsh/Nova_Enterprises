"""Application configuration using environment variables."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Supported runtime environments for NovaCore."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class TelemetrySettings(BaseModel):
    """Telemetry configuration values."""

    prometheus_metrics_port: int = Field(9000, ge=0, le=65535)
    otel_exporter_otlp_endpoint: str = Field(
        "http://localhost:4317",
        description="Endpoint for OTLP trace exports.",
    )


class BrokerSettings(BaseModel):
    """Broker configuration for Alpaca or other providers."""

    default_broker: str = Field("alpaca", min_length=1)
    alpaca_api_key: str = Field(..., min_length=1)
    alpaca_api_secret: str = Field(..., min_length=1)
    alpaca_base_url: str = Field(..., min_length=1)


class NovaSettings(BaseSettings):
    """Primary application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: Environment = Environment.DEVELOPMENT
    log_level: str = Field("INFO", min_length=1)
    api_host: str = Field("0.0.0.0", min_length=1)
    api_port: int = Field(8000, ge=1, le=65535)

    paper_trade: bool = True
    kill_switch: bool = False

    default_tenant_id: str = Field(
        "00000000-0000-0000-0000-000000000000",
        description="Tenant used for bootstrap operations.",
    )

    telemetry: TelemetrySettings = Field(default_factory=TelemetrySettings)
    brokers: BrokerSettings = Field(
        default_factory=lambda: BrokerSettings(
            alpaca_api_key="demo",
            alpaca_api_secret="demo",
            alpaca_base_url="https://paper-api.alpaca.markets",
        )
    )

    feature_flags: dict[str, bool] = Field(
        default_factory=lambda: {
            "nova_trade": True,
            "nova_store": False,
            "nova_social": False,
        }
    )

    mode: Literal["paper", "live"] = "paper"


settings = NovaSettings()
"""Singleton settings instance used across the application."""
