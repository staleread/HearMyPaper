from ..ports.incoming.get_my_conversions import GetMyConversionsPort
from ..ports.outgoing.processing import ProcessingPort
from ..models import Conversion


class GetMyConversionsUseCase(GetMyConversionsPort):
    def __init__(self, processing: ProcessingPort):
        self.processing = processing

    async def __call__(self) -> list[Conversion]:
        return await self.processing.get_my_conversions()
