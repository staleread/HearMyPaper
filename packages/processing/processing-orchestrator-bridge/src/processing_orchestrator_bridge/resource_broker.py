from uuid import uuid4
from datetime import datetime, timedelta, UTC
from typing import override
from processing_core.models import WorkerAssignment, ProcessingTaskType
from processing_core.ports.outgoing.resource_broker import ResourceBrokerPort
from orchestrator_core.ports.incoming.acquire_worker import (
    AcquireWorkerPort,
    AcquireWorkerQuery,
)


class OrchestratorResourceBrokerAdapter(ResourceBrokerPort):
    RESERVATION_TTL_MINUTES = 15

    # Mapping from Processing domain types to Orchestrator capabilities
    _TASK_CAPABILITY_MAP = {
        ProcessingTaskType.PDF_TO_AUDIO: "pdf-to-audio",
        ProcessingTaskType.UKRAINIAN_TTS: "ukrainian-tts",
    }

    def __init__(self, orchestrator: AcquireWorkerPort):
        self._orchestrator = orchestrator

    @override
    async def assign_compute_resource(
        self, task_type: ProcessingTaskType
    ) -> WorkerAssignment:
        capability = self._TASK_CAPABILITY_MAP.get(task_type)
        if not capability:
            raise ValueError(
                f"No orchestrator capability mapped for task type: {task_type}"
            )

        worker = await self._orchestrator(
            AcquireWorkerQuery(required_capability=capability)
        )

        return WorkerAssignment(
            assignment_id=uuid4(),
            worker_id=worker.worker_id,
            worker_public_key=worker.public_key,
            expires_at=datetime.now(UTC)
            + timedelta(minutes=self.RESERVATION_TTL_MINUTES),
        )
