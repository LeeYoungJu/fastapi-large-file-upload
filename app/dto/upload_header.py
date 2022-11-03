from dataclasses import dataclass
from fastapi import Request


@dataclass
class UploadHeader:
    def __init__(self, request: Request):
        self.data_type = request.headers.get('dataType')
        self.file_name = request.headers.get('fileName')
        self.file_uuid = request.headers.get('fileUuid')
        self.file_size = request.headers.get('size')
        self.cur_chunk_idx = request.headers.get('curChunkIdx')
        self.total_chunks = request.headers.get('totalChunks')
        self.cur_row_idx = request.headers.get('curRowIdx')


@dataclass
class TabularUploadHeader(UploadHeader):
    def __init__(self, request: Request):
        super().__init__(request)
        self.first_col_names = request.headers.get('firstColNames')

