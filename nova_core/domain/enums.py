"""Enumerations for NovaCore domain objects."""

from __future__ import annotations

from enum import Enum


class StrategyStatus(str, Enum):
    """Lifecycle status for trading strategies."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    DEPRECATED = "deprecated"


class OrderSide(str, Enum):
    """Supported order directions."""

    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    """Supported order types."""

    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(str, Enum):
    """Lifecycle status for orders."""

    NEW = "new"
    PENDING = "pending"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"


class PositionStatus(str, Enum):
    """Status for open positions."""

    OPEN = "open"
    CLOSED = "closed"


class ApprovalState(str, Enum):
    """Approval flow states for signals or orders."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class AccountMode(str, Enum):
    """Trading account mode."""

    PAPER = "paper"
    LIVE = "live"


class BrokerType(str, Enum):
    """Broker identifiers for adapter selection."""

    ALPACA = "alpaca"
    MOCK = "mock"


class SignalSide(str, Enum):
    """Signal directions."""

    LONG = "long"
    SHORT = "short"


class SignalSource(str, Enum):
    """Signal source classification."""

    STRATEGY = "strategy"
    MANUAL = "manual"
    EXTERNAL = "external"
