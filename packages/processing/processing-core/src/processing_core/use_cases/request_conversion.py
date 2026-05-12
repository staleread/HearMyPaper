from processing_core.models import AssignmentDTO
from processing_core.ports.incoming.request_conversion import (
    RequestConversionPort,
    RequestConversionQuery,
)
from processing_core.ports.outgoing.resource_broker import ResourceBrokerPort


class RequestConversionUseCase(RequestConversionPort):
    def __init__(self, broker: ResourceBrokerPort):
        self._broker = broker

    async def __call__(self, query: RequestConversionQuery) -> AssignmentDTO:
        # In this phase, we coordinate the resource assignment.
        # Future phases will include persisting the conversion state.
        return await self._broker.assign_compute_resource(query.task_type)
