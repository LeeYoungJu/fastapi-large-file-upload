from sqlalchemy.orm import Session

from app.dto import UploadHeader
from app.consts import DATA_TYPE
from app.service.upload_by_data_type import UploadTabularService


class UploadServiceFactory:

    @staticmethod
    def get_upload_service(db: Session, upload_header: UploadHeader):
        data_type = upload_header.data_type
        if data_type == DATA_TYPE.TABULAR:
            upload_stream_service = UploadTabularService
        # elif data_type == DATA_TYPE.IMAGE:
        # elif data_type == DATA_TYPE.AUDIO:

        return upload_stream_service(db, upload_header)
