"""Runtime state management for NovaCore."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RuntimeState:
    """Mutable state shared across services."""

    kill_switch: bool = False
    kill_switch_updated_at: datetime | None = None

    def engage_kill_switch(self) -> None:
        """Enable the global kill switch."""

        self.kill_switch = True
        self.kill_switch_updated_at = datetime.utcnow()

    def disengage_kill_switch(self) -> None:
        """Disable the global kill switch."""

        self.kill_switch = False
        self.kill_switch_updated_at = datetime.utcnow()


state = RuntimeState()
"""Singleton runtime state object."""
