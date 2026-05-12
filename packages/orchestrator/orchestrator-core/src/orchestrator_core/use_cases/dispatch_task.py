from orchestrator_core.ports.incoming.acquire_worker import (
    DispatchTaskPort,
    DispatchTaskCommand,
)
from orchestrator_core.ports.outgoing.task_repository import TaskRepositoryPort
from orchestrator_core.ports.outgoing.event_publisher import EventPublisherPort
from orchestrator_core.exceptions import TaskNotFoundError


class DispatchTaskUseCase(DispatchTaskPort):
    def __init__(self, tasks: TaskRepositoryPort, publisher: EventPublisherPort):
        self._tasks = tasks
        self._publisher = publisher

    async def __call__(self, cmd: DispatchTaskCommand) -> None:
        task = await self._tasks.get_task(cmd.task_id)
        if not task:
            raise TaskNotFoundError(f"Task {cmd.task_id} not found")

        await self._publisher.publish_task_dispatched(
            worker_id=task.worker_id,
            task_id=task.task_id,
            task_type=task.task_type,
            source_download_url=cmd.source_download_url,
            result_upload_url=cmd.result_upload_url,
            sealing_key=cmd.sealing_key,
        )
