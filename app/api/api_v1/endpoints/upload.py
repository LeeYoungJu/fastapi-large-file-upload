from fastapi import APIRouter, Request

from app.service.factory import UploadServiceFactory
from app.dao import ResponseData
from app.dao.factory import UploadHeaderFactory

router = APIRouter()


@router.post('/', response_model=ResponseData)
async def upload(request: Request):
    upload_metadata = UploadHeaderFactory.get_upload_header(request)
    upload_service = UploadServiceFactory.get_upload_service(upload_metadata)
    updated_row_idx = await upload_service.upload_chunk(request)
    return ResponseData.ok(
        data={"updated_row_idx": updated_row_idx}
    )
