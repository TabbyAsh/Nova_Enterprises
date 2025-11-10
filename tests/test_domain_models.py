"""Unit tests for NovaCore domain models."""

from __future__ import annotations

from datetime import datetime

from sqlmodel import Session, SQLModel, create_engine

from nova_core.domain.models import (
    Approval,
    Order,
    Signal,
    Strategy,
    Tenant,
    TradingAccount,
)
from nova_core.domain.enums import (
    AccountMode,
    ApprovalState,
    BrokerType,
    OrderSide,
    OrderStatus,
    OrderType,
    SignalSide,
    SignalSource,
)


def test_signal_compute_expiry_sets_timestamp() -> None:
    signal = Signal(ttl_seconds=60)
    expiry = signal.compute_expiry()
    assert signal.expires_at is not None
    assert isinstance(expiry, datetime)
    assert expiry == signal.expires_at


def test_models_persist_to_in_memory_sqlite() -> None:
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    tenant = Tenant(name="Test Tenant", slug="test-tenant")
    strategy = Strategy(tenant_id=tenant.id, name="Test Strategy")
    account = TradingAccount(
        tenant_id=tenant.id,
        name="Primary Account",
        broker=BrokerType.ALPACA,
        mode=AccountMode.PAPER,
        credentials_ref="vault://accounts/demo",
    )
    signal = Signal(
        tenant_id=tenant.id,
        strategy_id=strategy.id,
        symbol="AAPL",
        side=SignalSide.LONG,
        source=SignalSource.STRATEGY,
    )
    order = Order(
        tenant_id=tenant.id,
        account_id=account.id,
        signal_id=signal.id,
        symbol="AAPL",
        side=OrderSide.BUY,
        type=OrderType.MARKET,
        status=OrderStatus.NEW,
        quantity=10,
    )
    approval = Approval(
        tenant_id=tenant.id,
        signal_id=signal.id,
        state=ApprovalState.APPROVED,
        approver="Auto",
    )

    with Session(engine) as session:
        session.add(tenant)
        session.add(strategy)
        session.add(account)
        session.add(signal)
        session.add(order)
        session.add(approval)
        session.commit()

        persisted_order = session.get(Order, order.id)
        assert persisted_order is not None
        assert persisted_order.symbol == "AAPL"
        assert persisted_order.status is OrderStatus.NEW
