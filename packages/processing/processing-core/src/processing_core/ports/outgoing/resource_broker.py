from typing import Protocol
from processing_core.models import WorkerAssignment, ProcessingTaskType


class ResourceBrokerPort(Protocol):
    async def assign_compute_resource(
        self, task_type: ProcessingTaskType
    ) -> WorkerAssignment: ...
