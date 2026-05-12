class OrchestratorError(Exception):
    """Base class for orchestrator errors"""


class NoWorkerAvailableError(OrchestratorError):
    """Raised when no suitable worker is found"""
