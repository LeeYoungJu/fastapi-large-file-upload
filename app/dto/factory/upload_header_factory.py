from fastapi import Request

from app.consts import DATA_TYPE
from app.dto import TabularUploadHeader


class UploadHeaderFactory:

    @staticmethod
    def get_upload_header(request: Request):
        data_type = request.headers.get('dataType')

        if data_type == DATA_TYPE.TABULAR:
            upload_header = TabularUploadHeader
        # elif data_type == DATA_TYPE.IMAGE:
        # elif data_type == DATA_TYPE.AUDIO:

        return upload_header(request)
