from uuid import UUID
from typing import override
from processing_core.ports.outgoing.resource_broker import (
    ResourceBrokerPort,
    TaskAssignment as ProcessingTaskAssignment,
)

from orchestrator_core.ports.incoming.acquire_worker import (
    AcquireWorkerPort,
    AcquireWorkerQuery,
)
from orchestrator_core.ports.incoming.dispatch_task import (
    DispatchTaskPort,
    DispatchTaskCommand,
)


class OrchestratorResourceBrokerAdapter(ResourceBrokerPort):
    def __init__(self, orchestrator: AcquireWorkerPort, dispatcher: DispatchTaskPort):
        self._orchestrator = orchestrator
        self._dispatcher = dispatcher

    @override
    async def acquire_task(self, task_type: str) -> ProcessingTaskAssignment:
        assignment = await self._orchestrator(AcquireWorkerQuery(task_type=task_type))
        return ProcessingTaskAssignment(
            task_id=assignment.task_id,
            sealing_key=assignment.sealing_key,
        )

    @override
    async def start_task(
        self,
        task_id: UUID,
        source_download_url: str,
        result_upload_url: str,
        sealing_key: bytes,
    ) -> None:
        print(
            f"[DEBUG] OrchestratorResourceBrokerAdapter.start_task: task_id={task_id}"
        )
        await self._dispatcher(
            DispatchTaskCommand(
                task_id=task_id,
                source_download_url=source_download_url,
                result_upload_url=result_upload_url,
                sealing_key=sealing_key,
            )
        )
