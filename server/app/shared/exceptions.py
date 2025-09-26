from typing import Any


class DataSourceNotFoundException(Exception):
    def __init__(self, data_source: Any):
        super().__init__(f"Data source not found {data_source}")
