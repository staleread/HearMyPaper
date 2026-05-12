from typing import Protocol
from processing_core.models import AssignmentDTO, ProcessingTaskType


class ResourceBrokerPort(Protocol):
    async def assign_compute_resource(
        self, task_type: ProcessingTaskType
    ) -> AssignmentDTO: ...
