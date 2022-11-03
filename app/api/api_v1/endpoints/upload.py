from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.service.factory import UploadServiceFactory
from app.dto.factory import UploadHeaderFactory
from app.db.connect import get_db

router = APIRouter()


@router.post('/')
async def upload(*, db: Session = Depends(get_db), request: Request):
    upload_metadata = UploadHeaderFactory.get_upload_header(request)
    upload_service = UploadServiceFactory.get_upload_service(db, upload_metadata)
    result = await upload_service.upload_chunk(request)
    return result
