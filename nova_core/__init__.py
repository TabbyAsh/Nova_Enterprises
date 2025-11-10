"""NovaCore package initialization."""

from importlib import metadata

__all__ = ["__version__"]


def __getattr__(name: str) -> str:
    if name == "__version__":
        try:
            return metadata.version("nova-enterprises")
        except metadata.PackageNotFoundError:
            return "0.0.0"
    raise AttributeError(name)
