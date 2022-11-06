from fastapi import APIRouter, Request, Depends, UploadFile
from sqlalchemy.orm import Session

from app.service.factory import UploadServiceFactory
from app.dto.factory import UploadHeaderFactory
from app.db.connect import get_db
from app.service import UploadByMultipartService
from app.service.upload_to_cloud import TabularToCloudService

router = APIRouter()


@router.post('/')
async def upload(*, db: Session = Depends(get_db), request: Request):
    upload_metadata = UploadHeaderFactory.get_upload_header(request)
    upload_service = UploadServiceFactory.get_upload_service(db, upload_metadata)
    result = await upload_service.upload_chunk(request)
    return result


# @router.post('/dataset/')
# async def upload_dataset(*, db: Session = Depends(get_db), file: UploadFile):
#     upload_multipart_service = UploadByMultipartService()
#     folder_path = await upload_multipart_service.upload(file)
#     tabular_cloud_service = TabularToCloudService(file.filename, folder_path)
#     tabular_cloud_service.upload_to_cloud()
#
#     return 'ok'
