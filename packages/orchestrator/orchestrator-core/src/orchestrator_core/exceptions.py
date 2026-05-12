class OrchestratorError(Exception):
    """Base class for orchestrator errors"""


class NoWorkerAvailableError(OrchestratorError):
    """Raised when no suitable worker is found"""


class TaskNotFoundError(OrchestratorError):
    """Raised when a task is not found"""
