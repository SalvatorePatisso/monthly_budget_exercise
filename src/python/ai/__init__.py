"""AI helpers for the monthly budget application."""

from .azure_gpt import AzureGPT4O

# CrewDocumentProcessor relies on optional third-party packages.  Import it
# lazily so environments without those heavy dependencies can still use the
# rest of the ``python.ai`` helpers (e.g., during testing).
try:  # pragma: no cover - optional dependency
    from .crew_extractor import CrewDocumentProcessor
except ModuleNotFoundError:  # pragma: no cover - package not installed
    CrewDocumentProcessor = None

__all__ = ["AzureGPT4O", "CrewDocumentProcessor"]
