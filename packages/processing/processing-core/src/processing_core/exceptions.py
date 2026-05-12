class ProcessingError(Exception):
    """Base class for processing errors"""


class ConversionNotFoundError(ProcessingError):
    """Raised when a conversion is not found"""


class FileNotUploadedError(ProcessingError):
    """Raised when the source file is missing from storage"""


class InvalidConversionStatusError(ProcessingError):
    """Raised when the conversion is in an invalid state for the operation"""
