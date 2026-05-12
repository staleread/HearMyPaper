from uuid import UUID
from processing_core.ports.outgoing.path_resolver import FilePathResolverPort


class ProcessingFilePathResolver(FilePathResolverPort):
    def get_source_path(self, conversion_id: UUID) -> str:
        return f"conversions/{conversion_id}/source.pdf.bin"

    def get_result_path(self, conversion_id: UUID) -> str:
        return f"conversions/{conversion_id}/result.mp3.bin"
