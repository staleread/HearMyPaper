class ProcessingError(Exception):
    """Base class for processing errors"""


class WorkerBusyException(ProcessingError):
    """Raised when all suitable workers are over capacity"""
